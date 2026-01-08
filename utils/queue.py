
import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils.logger import logger

class AsyncTaskQueue:
    """基于asyncio的异步任务队列，支持同步(线程执行)和异步(协程执行)任务，队列跟随应用生命周期，不具备持久化"""

    def __init__(self):
        self.queue = asyncio.Queue()
        self._executor = ThreadPoolExecutor(max_workers=4)
        self._worker_task = None
        self._shutdown_event = asyncio.Event()
        self._active_tasks = 0
        self._shutdown_timeout = 300  # 关闭队列时等待剩余任务执行的超时时间
        self._loop = None  # 存储事件循环引用

    async def _worker(self):
        """异步工作协程"""
        while not self._shutdown_event.is_set() or not self.queue.empty():
            try:
                # 非阻塞获取任务
                try:
                    task, args, kwargs = self.queue.get_nowait()
                except asyncio.QueueEmpty:
                    if self._shutdown_event.is_set():
                        break
                    await asyncio.sleep(0.1)
                    continue

                self._active_tasks += 1
                try:
                    # 执行任务
                    func_name = getattr(task, '__name__', str(task))
                    logger.info(f"开始执行队列任务: {func_name}, args={args}, kwargs={kwargs}")
                    if asyncio.iscoroutinefunction(task):
                        await task(*args, **kwargs)
                    elif callable(task):
                        # 同步函数在线程池中执行
                        loop = asyncio.get_running_loop()
                        await loop.run_in_executor(
                            self._executor, 
                            lambda: task(*args, **kwargs)
                        )
                except Exception as e:
                    logger.error(f"队列任务执行失败, task={func_name}, args={args}, kwargs={kwargs}, error: {e}", exc_info=True)
                finally:
                    self.queue.task_done()
                    self._active_tasks -= 1
                    logger.info(f"队列任务执行完成: {func_name}, args={args}, kwargs={kwargs}")
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"队列任务工作协程异常: {e}", exc_info=True)

    async def start(self):
        """启动队列处理器"""
        if not self._worker_task or self._worker_task.done():
            self._loop = asyncio.get_running_loop()
            self._shutdown_event.clear()
            self._worker_task = asyncio.create_task(self._worker())
            # logger.info("异步任务队列已启动")

    async def graceful_shutdown(self):
        """优雅关闭，等待任务完成"""
        logger.info("开始优雅关闭任务队列...")
        self._shutdown_event.set()
        
        start_time = asyncio.get_event_loop().time()
        while not self.queue.empty() or self._active_tasks > 0:
            await asyncio.sleep(0.1)
            elapsed = asyncio.get_event_loop().time() - start_time
            if elapsed > self._shutdown_timeout:
                logger.warning(f"关闭超时，剩余任务: {self.queue.qsize()}, 活跃任务: {self._active_tasks}")
                break
        
        if self._worker_task and not self._worker_task.done():
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
        
        self._executor.shutdown(wait=True)
        logger.info("任务队列已完全关闭")

    def add_task(self, task, *args, **kwargs):
        """线程安全的添加任务"""
        if self._shutdown_event.is_set():
            raise RuntimeError("任务队列已关闭，不能再添加新任务")
        
        if self._loop is None:
            raise RuntimeError("任务队列未启动")
        
        # 同步函数包装
        # if not asyncio.iscoroutinefunction(task):
        #     orig_task = task
        #     task = lambda *a, **kw: orig_task(*a, **kw)
        
        # 确保协程被正确调度
        self._loop.call_soon_threadsafe(
            lambda: self._loop.create_task(
                self._put_task(task, args, kwargs)
            )
        )

    async def _put_task(self, task, args, kwargs):
        """实际放入队列的协程"""
        await self.queue.put((task, args, kwargs))

# 全局实例
task_queue = AsyncTaskQueue()
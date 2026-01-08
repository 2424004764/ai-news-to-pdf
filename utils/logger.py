import os
import logging
from logging.handlers import TimedRotatingFileHandler


_logger_client = None


def setup_logger(name='app', log_dir='logs'):
    """
    设置日志记录器
    :param name: 日志记录器名称
    :param log_dir: 日志文件存储目录
    :return: 配置好的日志记录器
    """

    global _logger_client

    if _logger_client is not None:
        return _logger_client

    # 创建日志目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 创建基本日志文件名
    log_file = os.path.join(log_dir, 'app.log')

    # 创建日志记录器
    logger = logging.getLogger(name)

    # 如果logger已经有handlers，先清除它们，防止重复添加
    if logger.handlers:
        logger.handlers = []

    logger.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 使用TimedRotatingFileHandler按日期轮转
    file_handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',  # 每天午夜轮转
        interval=1,       # 轮转间隔为1天
        backupCount=30,   # 保留30天的日志
        encoding='utf-8',
        delay=True
    )
    # 设置后缀格式为 .%Y-%m-%d
    file_handler.suffix = "%Y-%m-%d"
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    _logger_client = logger
    return logger


# 创建默认日志记录器实例
logger = setup_logger()


def configure_agno_logging(level=logging.DEBUG, log_dir='logs', log_file='agno.log', preserve_console_handler=True):
    """
    将agno日志系统连接到单独的日志文件

    Args:
        level: 日志级别，默认为DEBUG
        log_dir: 日志目录，默认为'logs'
        log_file: agno日志文件名，默认为'agno.log'
        preserve_console_handler: 是否保留原始的控制台处理器，默认为True
    """
    try:
        from agno.utils.log import LOGGER_NAME, TEAM_LOGGER_NAME, set_log_level_to_debug
        from rich.logging import RichHandler

        # 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 创建agno专用的日志文件路径
        agno_log_path = os.path.join(log_dir, log_file)

        # 为agno的日志添加专用文件处理器
        for logger_name in [LOGGER_NAME, TEAM_LOGGER_NAME]:
            agno_logger = logging.getLogger(logger_name)

            # 处理控制台处理器
            if preserve_console_handler:
                # 识别并保留Rich处理器
                rich_handlers = []
                handlers_to_remove = []

                for handler in agno_logger.handlers:
                    # 检查是否为Rich处理器
                    if isinstance(handler, RichHandler):
                        rich_handlers.append(handler)
                        # 更新Rich处理器的级别
                        handler.setLevel(level)
                    else:
                        handlers_to_remove.append(handler)

                # 移除非Rich处理器
                for handler in handlers_to_remove:
                    agno_logger.removeHandler(handler)
            else:
                # 移除所有处理器
                for handler in list(agno_logger.handlers):
                    agno_logger.removeHandler(handler)

            # 创建文件处理器 - 使用与应用相同的轮转方式
            file_handler = TimedRotatingFileHandler(
                agno_log_path,
                when='midnight',  # 每天午夜轮转
                interval=1,       # 轮转间隔为1天
                backupCount=30,   # 保留30天的日志
                encoding='utf-8',
                delay=True
            )
            file_handler.suffix = "%Y-%m-%d"
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            file_handler.setLevel(level)
            agno_logger.addHandler(file_handler)

            # 设置日志级别
            agno_logger.setLevel(level)

        # 显式开启agno的debug模式
        set_log_level_to_debug()

        # 确保debug_on标志设置为True (如果使用DEBUG级别)
        if level <= logging.DEBUG:
            import agno.utils.log
            agno.utils.log.debug_on = True

        print(
            f"agno日志配置完成，日志将输出到：{agno_log_path}，日志级别：{logging.getLevelName(level)}")
        return True
    except ImportError as e:
        print(f"未找到agno模块，无法配置日志: {e}")
        return False
    except Exception as e:
        print(f"配置agno日志时出错: {e}")
        return False

def uvicorn_log_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": "%(asctime)s - %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s",
                "use_colors": None,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
        },
    }
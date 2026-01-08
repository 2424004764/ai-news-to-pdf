def singleton(cls):
    """
    单例模式的装饰器实现。

    它将创建并存储被装饰类的一个实例，
    之后对该类的任何调用都返回这个存储的实例。
    """
    _instance = {}  # 用于存储类的实例

    def get_instance(*args, **kwargs):
        """
        每次调用类名时，实际执行的是这个函数。
        """
        if cls not in _instance:
            # 如果实例不存在，则创建一个，并存储
            _instance[cls] = cls(*args, **kwargs)
        # 否则，返回已存在的实例
        return _instance[cls]

    return get_instance

import sys
import atexit  # 和 atexcp 放在同一模块


class _AtExceptionHook:
    _callbacks = dict()

    @staticmethod
    def register(func, args=None, kwargs=None):
        func_name = func.__name__
        if _AtExceptionHook._callbacks.get(func_name):
            raise Exception("已经注册了同名的 exception 函数")
        _AtExceptionHook._callbacks[func_name] = (func, args or tuple(), kwargs or dict())
        return func

    @staticmethod
    def unregister(func):
        func_name = func.__name__
        _AtExceptionHook._callbacks.pop(func_name, None)
        return func

    @staticmethod
    def call_callbacks():
        for callback in _AtExceptionHook._callbacks.values():
            try:
                func, args, kwargs = callback
                func(*args, **kwargs)
            except BaseException:
                pass


atexcp = _AtExceptionHook()


def exception_hook(exception_type, value, trace_back):
    atexcp.call_callbacks()
    sys.__excepthook__(exception_type, value, trace_back)


sys.excepthook = exception_hook

atexit = atexit

__all__ = ["atexit",
           "atexcp"]

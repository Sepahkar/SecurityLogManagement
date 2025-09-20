"""
پیاده‌سازی الگوی Singleton در Python
این فایل شامل چندین روش مختلف برای پیاده‌سازی Singleton است
"""

def singleton(cls):
    """
    Decorator برای پیاده‌سازی Singleton
    این روش thread-safe است و ساده‌ترین راه برای پیاده‌سازی Singleton است
    """
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


class SingletonMeta(type):
    """
    MetaClass برای پیاده‌سازی Singleton
    این روش thread-safe است و کنترل بیشتری روی رفتار کلاس فراهم می‌کند
    """
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonBase:
    """
    کلاس پایه برای پیاده‌سازی Singleton
    این روش ساده‌تر است اما thread-safe نیست
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonBase, cls).__new__(cls)
        return cls._instance


# مثال استفاده از Decorator
@singleton
class FormManagerSingleton:
    """
    مثال استفاده از Singleton با Decorator
    """
    def __init__(self, request_id=None):
        self.request_id = request_id
        self.data = {}
    
    def set_data(self, key, value):
        self.data[key] = value
    
    def get_data(self, key):
        return self.data.get(key)


# مثال استفاده از MetaClass
class FormManagerMeta(metaclass=SingletonMeta):
    """
    مثال استفاده از Singleton با MetaClass
    """
    def __init__(self, request_id=None):
        self.request_id = request_id
        self.data = {}
    
    def set_data(self, key, value):
        self.data[key] = value
    
    def get_data(self, key):
        return self.data.get(key)


# مثال استفاده از کلاس پایه
class FormManagerBase(SingletonBase):
    """
    مثال استفاده از Singleton با کلاس پایه
    """
    def __init__(self, request_id=None):
        self.request_id = request_id
        self.data = {}
    
    def set_data(self, key, value):
        self.data[key] = value
    
    def get_data(self, key):
        return self.data.get(key)

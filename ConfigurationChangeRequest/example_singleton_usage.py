"""
مثال کامل استفاده از Singleton در Django
این فایل نشان می‌دهد که چگونه از Singleton در پروژه استفاده کنیم
"""

from .business import FormManager
from .singleton import FormManagerSingleton, FormManagerMeta, FormManagerBase


def example_usage():
    """
    مثال استفاده از Singleton در Django
    """
    
    # روش 1: استفاده از FormManager که به Singleton تبدیل شده
    print("=== استفاده از FormManager Singleton ===")
    
    # اولین بار ایجاد می‌شود
    manager1 = FormManager(request_id=123)
    print(f"Manager 1 ID: {id(manager1)}")
    print(f"Manager 1 Request ID: {manager1.request_id}")
    
    # دومین بار همان نمونه قبلی را برمی‌گرداند
    manager2 = FormManager(request_id=456)  # request_id نادیده گرفته می‌شود
    print(f"Manager 2 ID: {id(manager2)}")
    print(f"Manager 2 Request ID: {manager2.request_id}")
    
    # بررسی اینکه آیا همان نمونه هستند
    print(f"Same instance: {manager1 is manager2}")
    
    print("\n=== استفاده از Decorator Singleton ===")
    
    # استفاده از Decorator
    singleton1 = FormManagerSingleton(request_id=789)
    singleton2 = FormManagerSingleton(request_id=101112)
    
    print(f"Singleton 1 ID: {id(singleton1)}")
    print(f"Singleton 2 ID: {id(singleton2)}")
    print(f"Same instance: {singleton1 is singleton2}")
    
    # تنظیم داده
    singleton1.set_data('test_key', 'test_value')
    print(f"Data from singleton2: {singleton2.get_data('test_key')}")


def django_view_example(request):
    """
    مثال استفاده در Django View
    """
    from django.http import JsonResponse
    
    # در هر view می‌توانید از همان نمونه استفاده کنید
    form_manager = FormManager(request_id=1)
    
    # انجام عملیات
    result = form_manager.some_method()
    
    return JsonResponse({'result': result})


class ServiceClass:
    """
    مثال استفاده از Singleton در یک کلاس سرویس
    """
    
    def __init__(self):
        # در هر نمونه از این کلاس، همان FormManager استفاده می‌شود
        self.form_manager = FormManager()
    
    def process_request(self, request_id):
        """
        پردازش درخواست با استفاده از FormManager Singleton
        """
        # تنظیم request_id جدید
        self.form_manager.request_id = request_id
        
        # انجام عملیات
        return self.form_manager.some_method()


# مثال استفاده در middleware
class FormManagerMiddleware:
    """
    مثال استفاده از Singleton در Middleware
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # FormManager در سطح middleware ایجاد می‌شود
        self.form_manager = FormManager()
    
    def __call__(self, request):
        # در هر درخواست، همان FormManager استفاده می‌شود
        request.form_manager = self.form_manager
        
        response = self.get_response(request)
        return response


# مثال استفاده در Django Signals
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='ConfigurationChangeRequest.Request')
def handle_request_save(sender, instance, created, **kwargs):
    """
    مثال استفاده از Singleton در Django Signals
    """
    # در signal هم می‌توانید از همان FormManager استفاده کنید
    form_manager = FormManager(request_id=instance.id)
    
    # انجام عملیات پس از ذخیره
    form_manager.process_after_save(instance)

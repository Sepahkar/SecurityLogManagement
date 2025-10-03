from django.urls import path
from . import views

app_name = 'ConfigurationChangeRequest'

urlpatterns = [
    # ایجاد درخواست جدید
    path('', views.request_create, name='request_create'),
    
    # درخواست در مراحل مختلف
    path('<int:request_id>/', views.request_view, name='request_view'),

    # اضافه/حذف کردن مجری به/از یک درخواست
    path('Task/<int:request_task_id>/', views.request_task_user_management, name='request_task_user_management'),

    # لیست انواع درخواست
    path('change_type/list/', views.change_type_list, name='change_type_list'),
    
    #ویرایش  یک نوع درخواست با شناسه ارسال شده
    path('change_type/<int:change_type_id>/',views.change_type_edit, name='change_type_edit'),
        
    # ایجاد یک نوع درخواست
    path('change_type/', views.change_type_create, name='change_type'),
    
    # اضافه/حذف کردن مجری به/از یک نوع درخواست
    path('change_type/Task/<int:task_id>/', views.change_type_user_management, name='change_type_user_managment'),
    
    # انتخاب تسک (برای مجری/تستر)
    path('task/select/<int:request_id>/<int:task_id>/', views.task_select_view, name='task_select'),
    
    # گزارش تسک (برای مجری/تستر)
    path('task/report/<int:request_id>/<int:task_id>/', views.task_report_view, name='task_report'),
    
    # عملیات روی درخواست (تایید/رد/بازگشت)
    path('request/action/<int:request_id>/<str:action>/', views.request_action_view, name='request_action'),
    
    # عملیات روی تسک (تایید/رد/بازگشت)
    path('task/action/<int:request_id>/<int:task_id>/<str:action>/', views.task_action_view, name='task_action'),
    
    # مشاهده درخواست (فقط خواندنی)
    path('request/view/<int:request_id>/', views.request_view_view, name='request_view'),
    
    # تست پیام‌ها
    path('test/messages/', views.test_messages_view, name='test_messages'),
]

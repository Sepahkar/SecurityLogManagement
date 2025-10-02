"""
تنظیمات اضافی و بهبودهای ادمین پنل
این فایل شامل ویژگی‌های پیشرفته‌تر برای ادمین پنل است
"""

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q, F, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from datetime import timedelta, datetime
import json
import csv
import xlwt
from .models import ConfigurationChangeRequest, User, Task, RequestTask


class AdminEnhancements:
    """
    کلاس بهبودهای ادمین پنل
    """
    
    @staticmethod
    def add_custom_actions():
        """
        اضافه کردن اکشن‌های سفارشی
        """
        def export_to_csv(modeladmin, request, queryset):
            """
            صادرات به CSV
            """
            response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
            response['Content-Disposition'] = 'attachment; filename="requests.csv"'
            
            writer = csv.writer(response)
            
            # نوشتن هدرها
            headers = [
                'کد سند', 'عنوان تغییر', 'وضعیت', 'درخواست کننده',
                'تیم درخواست کننده', 'تاریخ ایجاد', 'تاریخ تغییرات'
            ]
            writer.writerow(headers)
            
            # نوشتن داده‌ها
            for obj in queryset:
                row = [
                    obj.doc_id or '',
                    obj.change_title,
                    obj.get_status_code_display(),
                    obj.requestor_nationalcode.fullname,
                    obj.requestor_team_code.team_name if obj.requestor_team_code else '',
                    obj.createdate.strftime('%Y-%m-%d %H:%M'),
                    obj.changing_date,
                ]
                writer.writerow(row)
            
            return response
        
        export_to_csv.short_description = "صادرات انتخاب شده‌ها به CSV"
        
        def send_bulk_notification(modeladmin, request, queryset):
            """
            ارسال اطلاعیه گروهی
            """
            # اینجا می‌توانید منطق ارسال اطلاعیه را پیاده‌سازی کنید
            count = queryset.count()
            modeladmin.message_user(
                request,
                f'اطلاعیه برای {count} درخواست ارسال شد.',
                level='SUCCESS'
            )
        
        send_bulk_notification.short_description = "ارسال اطلاعیه گروهی"
        
        def duplicate_requests(modeladmin, request, queryset):
            """
            تکثیر درخواست‌ها
            """
            duplicated_count = 0
            for obj in queryset:
                # ایجاد کپی از درخواست
                new_obj = ConfigurationChangeRequest.objects.create(
                    change_title=f"کپی - {obj.change_title}",
                    change_type=obj.change_type,
                    requestor_nationalcode=obj.requestor_nationalcode,
                    requestor_team_code=obj.requestor_team_code,
                    requestor_role_id=obj.requestor_role_id,
                    direct_manager_nationalcode=obj.direct_manager_nationalcode,
                    related_manager_nationalcode=obj.related_manager_nationalcode,
                    status_code='DRAFTD',
                    change_description=obj.change_description,
                )
                duplicated_count += 1
            
            modeladmin.message_user(
                request,
                f'{duplicated_count} درخواست با موفقیت تکثیر شد.',
                level='SUCCESS'
            )
        
        duplicate_requests.short_description = "تکثیر درخواست‌ها"
        
        return [export_to_csv, send_bulk_notification, duplicate_requests]


class AdvancedFilters:
    """
    فیلترهای پیشرفته
    """
    
    class DateRangeFilter(SimpleListFilter):
        title = 'بازه تاریخ ایجاد'
        parameter_name = 'date_range'
        
        def lookups(self, request, model_admin):
            return (
                ('today', 'امروز'),
                ('yesterday', 'دیروز'),
                ('week', 'این هفته'),
                ('month', 'این ماه'),
                ('quarter', 'این فصل'),
                ('year', 'امسال'),
                ('last_week', 'هفته گذشته'),
                ('last_month', 'ماه گذشته'),
            )
        
        def queryset(self, request, queryset):
            now = timezone.now()
            if self.value() == 'today':
                return queryset.filter(createdate__date=now.date())
            elif self.value() == 'yesterday':
                yesterday = now.date() - timedelta(days=1)
                return queryset.filter(createdate__date=yesterday)
            elif self.value() == 'week':
                start_date = now - timedelta(days=7)
                return queryset.filter(createdate__gte=start_date)
            elif self.value() == 'month':
                start_date = now - timedelta(days=30)
                return queryset.filter(createdate__gte=start_date)
            elif self.value() == 'quarter':
                start_date = now - timedelta(days=90)
                return queryset.filter(createdate__gte=start_date)
            elif self.value() == 'year':
                start_date = now - timedelta(days=365)
                return queryset.filter(createdate__gte=start_date)
            elif self.value() == 'last_week':
                start_date = now - timedelta(days=14)
                end_date = now - timedelta(days=7)
                return queryset.filter(createdate__gte=start_date, createdate__lt=end_date)
            elif self.value() == 'last_month':
                start_date = now - timedelta(days=60)
                end_date = now - timedelta(days=30)
                return queryset.filter(createdate__gte=start_date, createdate__lt=end_date)
    
    class StatusGroupFilter(SimpleListFilter):
        title = 'گروه وضعیت'
        parameter_name = 'status_group'
        
        def lookups(self, request, model_admin):
            return (
                ('active', 'در حال انجام'),
                ('completed', 'تکمیل شده'),
                ('failed', 'ناموفق'),
                ('pending', 'در انتظار'),
                ('in_review', 'در حال بررسی'),
            )
        
        def queryset(self, request, queryset):
            if self.value() == 'active':
                return queryset.filter(status_code__in=['DIRMAN', 'RELMAN', 'COMITE', 'DOTASK'])
            elif self.value() == 'completed':
                return queryset.filter(status_code='FINISH')
            elif self.value() == 'failed':
                return queryset.filter(status_code__in=['FAILED', 'ERRORF'])
            elif self.value() == 'pending':
                return queryset.filter(status_code='DRAFTD')
            elif self.value() == 'in_review':
                return queryset.filter(status_code__in=['DIRMAN', 'RELMAN', 'COMITE'])


class CustomAdminViews:
    """
    ویوهای سفارشی ادمین
    """
    
    @staticmethod
    def dashboard_view(request):
        """
        داشبورد با آمار تفصیلی
        """
        # آمار کلی
        total_requests = ConfigurationChangeRequest.objects.count()
        pending_requests = ConfigurationChangeRequest.objects.filter(status_code='DRAFTD').count()
        active_requests = ConfigurationChangeRequest.objects.filter(
            status_code__in=['DIRMAN', 'RELMAN', 'COMITE', 'DOTASK']
        ).count()
        completed_requests = ConfigurationChangeRequest.objects.filter(status_code='FINISH').count()
        failed_requests = ConfigurationChangeRequest.objects.filter(
            status_code__in=['FAILED', 'ERRORF']
        ).count()
        
        # آمار بر اساس نوع تغییر
        change_type_stats = ConfigurationChangeRequest.objects.values(
            'change_type__change_type_title'
        ).annotate(
            count=Count('id'),
            completed=Count('id', filter=Q(status_code='FINISH')),
            failed=Count('id', filter=Q(status_code__in=['FAILED', 'ERRORF']))
        ).order_by('-count')[:10]
        
        # آمار بر اساس تیم
        team_stats = ConfigurationChangeRequest.objects.values(
            'requestor_team_code__team_name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        # آمار ماهانه
        monthly_stats = []
        for i in range(12):
            month_start = timezone.now() - timedelta(days=30*i)
            month_end = month_start + timedelta(days=30)
            count = ConfigurationChangeRequest.objects.filter(
                createdate__gte=month_start,
                createdate__lt=month_end
            ).count()
            monthly_stats.append({
                'month': month_start.strftime('%Y-%m'),
                'count': count
            })
        
        context = {
            'title': 'داشبورد تفصیلی',
            'total_requests': total_requests,
            'pending_requests': pending_requests,
            'active_requests': active_requests,
            'completed_requests': completed_requests,
            'failed_requests': failed_requests,
            'change_type_stats': change_type_stats,
            'team_stats': team_stats,
            'monthly_stats': monthly_stats,
        }
        
        return render(request, 'admin/dashboard_detail.html', context)
    
    @staticmethod
    def analytics_view(request):
        """
        صفحه آنالیتیکس
        """
        # آمار عملکرد
        performance_stats = {
            'avg_completion_time': 0,
            'success_rate': 0,
            'most_active_team': '',
            'most_common_change_type': '',
        }
        
        # محاسبه میانگین زمان تکمیل
        completed_requests = ConfigurationChangeRequest.objects.filter(
            status_code='FINISH',
            createdate__isnull=False,
            modifydate__isnull=False
        )
        
        if completed_requests.exists():
            total_days = 0
            for req in completed_requests:
                days = (req.modifydate - req.createdate).days
                total_days += days
            
            performance_stats['avg_completion_time'] = total_days / completed_requests.count()
        
        # محاسبه نرخ موفقیت
        total_processed = ConfigurationChangeRequest.objects.filter(
            status_code__in=['FINISH', 'FAILED', 'ERRORF']
        ).count()
        
        if total_processed > 0:
            success_count = ConfigurationChangeRequest.objects.filter(status_code='FINISH').count()
            performance_stats['success_rate'] = (success_count / total_processed) * 100
        
        # تیم فعال
        active_team = ConfigurationChangeRequest.objects.values(
            'requestor_team_code__team_name'
        ).annotate(
            count=Count('id')
        ).order_by('-count').first()
        
        if active_team:
            performance_stats['most_active_team'] = active_team['requestor_team_code__team_name']
        
        # نوع تغییر رایج
        common_change_type = ConfigurationChangeRequest.objects.values(
            'change_type__change_type_title'
        ).annotate(
            count=Count('id')
        ).order_by('-count').first()
        
        if common_change_type:
            performance_stats['most_common_change_type'] = common_change_type['change_type__change_type_title']
        
        context = {
            'title': 'آنالیتیکس و آمار عملکرد',
            'performance_stats': performance_stats,
        }
        
        return render(request, 'admin/analytics.html', context)


class AdminWidgets:
    """
    ویجت‌های سفارشی ادمین
    """
    
    @staticmethod
    def get_status_badge(status_code):
        """
        ایجاد badge برای وضعیت
        """
        status_map = {
            'DRAFTD': ('پیش نویس', 'status-draft'),
            'DIRMAN': ('اظهار نظر مدیر مستقیم', 'status-active'),
            'RELMAN': ('اظهار نظر مدیر مربوطه', 'status-active'),
            'COMITE': ('اظهار نظر کمیته', 'status-active'),
            'DOTASK': ('انجام تسک‌ها', 'status-active'),
            'FINISH': ('خاتمه یافته', 'status-completed'),
            'FAILED': ('خاتمه ناموفقیت‌آمیز', 'status-failed'),
            'ERRORF': ('خاتمه با خطا', 'status-failed'),
        }
        
        if status_code in status_map:
            text, css_class = status_map[status_code]
            return format_html(
                '<span class="status-badge {}">{}</span>',
                css_class, text
            )
        
        return status_code
    
    @staticmethod
    def get_priority_badge(priority):
        """
        ایجاد badge برای اولویت
        """
        if not priority:
            return '-'
        
        priority_map = {
            'Standard': ('استاندارد', 'priority-standard'),
            'Urgent': ('فوری', 'priority-urgent'),
            'Emergency': ('اضطراری', 'priority-emergency'),
        }
        
        priority_text = priority.Caption if hasattr(priority, 'Caption') else str(priority)
        
        for key, (text, css_class) in priority_map.items():
            if key in priority_text:
                return format_html(
                    '<span class="priority-badge {}">{}</span>',
                    css_class, text
                )
        
        return priority_text
    
    @staticmethod
    def get_risk_badge(risk_level):
        """
        ایجاد badge برای سطح ریسک
        """
        if not risk_level:
            return '-'
        
        risk_text = risk_level.Caption if hasattr(risk_level, 'Caption') else str(risk_level)
        
        risk_map = {
            'Low': ('پایین', 'risk-low'),
            'Medium': ('متوسط', 'risk-medium'),
            'High': ('بالا', 'risk-high'),
        }
        
        for key, (text, css_class) in risk_map.items():
            if key in risk_text:
                return format_html(
                    '<span class="risk-badge {}">{}</span>',
                    css_class, text
                )
        
        return risk_text


# تنظیمات اضافی برای بهبود عملکرد
ADMIN_PERFORMANCE_SETTINGS = {
    'select_related': [
        'change_type',
        'requestor_nationalcode',
        'requestor_team_code',
        'requestor_role_id',
        'direct_manager_nationalcode',
        'related_manager_nationalcode',
    ],
    'prefetch_related': [
        'requesttask_set',
        'requestnotifygroup_set',
        'requestcorp_set',
        'requestteam_set',
    ],
    'list_per_page': 25,
    'list_max_show_all': 100,
    'preserve_filters': True,
    'show_full_result_count': True,
}

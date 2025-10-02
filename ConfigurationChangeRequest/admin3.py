from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import TextInput, Textarea, CheckboxInput, ModelChoiceField
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from .admin_filters import (
    ClassificationFilter, PriorityFilter, RiskLevelFilter, 
    ChangeLevelFilter, ChangeDomainFilter, ActiveTeamFilter, CorpFilter, ParentIdFilter, GenderFilter, WorkflowStatusFilter
)
#from .models import (
    User, UserTeamRole, ConstValue, Corp, Team, Role, Committee,
    ChangeType, NotifyGroup, NotifyGroupUser, ConfigurationChangeRequest,
    Task, TaskUser, RequestTask, TaskUserSelected, RequestTask_ChangeType,
    RequestTaskUser, RequestFlow, RequestNotifyGroup, RequestNotifyGroup_ChangeType,
    RequestCorp_ChangeType, RequestTeam_ChangeType, RequestExtraInformation_ChangeType,
    RequestCorp, RequestTeam, RequestExtraInformation
)


# تنظیمات کلی ادمین
admin.site.site_header = "مدیریت سیستم درخواست تغییرات"
admin.site.site_title = "مدیریت درخواست تغییرات"
admin.site.index_title = "پنل مدیریت"


# فیلدهای سفارشی برای کمبو باکس‌ها
class ActiveTeamChoiceField(ModelChoiceField):
    """فیلد انتخاب تیم‌های فعال"""
    def __init__(self, **kwargs):
        kwargs['queryset'] = Team.objects.filter(is_active=True)
        kwargs['empty_label'] = "انتخاب تیم..."
        super().__init__(**kwargs)


class ClassificationChoiceField(ModelChoiceField):
    """فیلد انتخاب طبقه‌بندی"""
    def __init__(self, **kwargs):
        # ابتدا والدین را پیدا کن
        parent_classification = ConstValue.objects.filter(
            Code__startswith='Classification_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_classification:
            # فرزندان والد را نمایش بده
            kwargs['queryset'] = ConstValue.objects.filter(
                Parent=parent_classification,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            kwargs['queryset'] = ConstValue.objects.filter(
                Code__startswith='Classification_',
                IsActive=True
            ).order_by('OrderNumber')
        
        kwargs['empty_label'] = "انتخاب طبقه‌بندی..."
        super().__init__(**kwargs)
    
    def label_from_instance(self, obj):
        """نمایش بهتر برچسب‌ها با نشان دادن والد"""
        if obj.Parent:
            return f"  └─ {obj.Caption}"
        return obj.Caption


class PriorityChoiceField(ModelChoiceField):
    """فیلد انتخاب اولویت"""
    def __init__(self, **kwargs):
        # ابتدا والدین را پیدا کن
        parent_priority = ConstValue.objects.filter(
            Code__startswith='Priority_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_priority:
            # فرزندان والد را نمایش بده
            kwargs['queryset'] = ConstValue.objects.filter(
                Parent=parent_priority,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            kwargs['queryset'] = ConstValue.objects.filter(
                Code__startswith='Priority_',
                IsActive=True
            ).order_by('OrderNumber')
        
        kwargs['empty_label'] = "انتخاب اولویت..."
        super().__init__(**kwargs)
    
    def label_from_instance(self, obj):
        """نمایش بهتر برچسب‌ها با نشان دادن والد"""
        if obj.Parent:
            return f"  └─ {obj.Caption}"
        return obj.Caption


class RiskLevelChoiceField(ModelChoiceField):
    """فیلد انتخاب سطح ریسک"""
    def __init__(self, **kwargs):
        # ابتدا والدین را پیدا کن
        parent_risk = ConstValue.objects.filter(
            Code__startswith='Risk_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_risk:
            # فرزندان والد را نمایش بده
            kwargs['queryset'] = ConstValue.objects.filter(
                Parent=parent_risk,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            kwargs['queryset'] = ConstValue.objects.filter(
                Code__startswith='Risk_',
                IsActive=True
            ).order_by('OrderNumber')
        
        kwargs['empty_label'] = "انتخاب سطح ریسک..."
        super().__init__(**kwargs)
    
    def label_from_instance(self, obj):
        """نمایش بهتر برچسب‌ها با نشان دادن والد"""
        if obj.Parent:
            return f"  └─ {obj.Caption}"
        return obj.Caption


class ChangeLevelChoiceField(ModelChoiceField):
    """فیلد انتخاب گستردگی تغییرات"""
    def __init__(self, **kwargs):
        # ابتدا والدین را پیدا کن
        parent_level = ConstValue.objects.filter(
            Code__startswith='ChangeLevel_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_level:
            # فرزندان والد را نمایش بده
            kwargs['queryset'] = ConstValue.objects.filter(
                Parent=parent_level,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            kwargs['queryset'] = ConstValue.objects.filter(
                Code__startswith='ChangeLevel_',
                IsActive=True
            ).order_by('OrderNumber')
        
        kwargs['empty_label'] = "انتخاب گستردگی تغییرات..."
        super().__init__(**kwargs)
    
    def label_from_instance(self, obj):
        """نمایش بهتر برچسب‌ها با نشان دادن والد"""
        if obj.Parent:
            return f"  └─ {obj.Caption}"
        return obj.Caption


class ChangeDomainChoiceField(ModelChoiceField):
    """فیلد انتخاب دامنه تغییر"""
    def __init__(self, **kwargs):
        # ابتدا والدین را پیدا کن
        parent_domain = ConstValue.objects.filter(
            Code__startswith='ChangeDomain_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_domain:
            # فرزندان والد را نمایش بده
            kwargs['queryset'] = ConstValue.objects.filter(
                Parent=parent_domain,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            kwargs['queryset'] = ConstValue.objects.filter(
                Code__startswith='ChangeDomain_',
                IsActive=True
            ).order_by('OrderNumber')
        
        kwargs['empty_label'] = "انتخاب دامنه تغییر..."
        super().__init__(**kwargs)
    
    def label_from_instance(self, obj):
        """نمایش بهتر برچسب‌ها با نشان دادن والد"""
        if obj.Parent:
            return f"  └─ {obj.Caption}"
        return obj.Caption


class SearchableCorpChoiceField(ModelChoiceField):
    """فیلد انتخاب شرکت با قابلیت جستجو"""
    def __init__(self, **kwargs):
        kwargs['queryset'] = Corp.objects.all().order_by('corp_name')
        kwargs['empty_label'] = "انتخاب شرکت..."
        super().__init__(**kwargs)


class SearchableTeamChoiceField(ModelChoiceField):
    """فیلد انتخاب تیم با قابلیت جستجو"""
    def __init__(self, **kwargs):
        kwargs['queryset'] = Team.objects.filter(is_active=True).order_by('team_name')
        kwargs['empty_label'] = "انتخاب تیم..."
        super().__init__(**kwargs)


# کلاس‌های Inline برای جدول‌های مستر-دیتیل
class UserTeamRoleInline(admin.TabularInline):
    model = UserTeamRole
    extra = 0
    fields = ['role_id', 'team_code', 'manager_national_code']
    autocomplete_fields = ['team_code', 'manager_national_code']
    fk_name = 'national_code'


class NotifyGroupInline(admin.TabularInline):
    model = NotifyGroup
    extra = 0
    fields = ['code', 'title', 'role_id', 'team_code']
    fk_name = 'parent_group'


class NotifyGroupUserInline(admin.TabularInline):
    model = NotifyGroupUser
    extra = 0
    fields = ['user_nationalcode', 'user_role_id', 'user_team_code', 'user_role_code']
    autocomplete_fields = ['user_nationalcode', 'user_role_id', 'user_team_code']


class RequestTaskInline(admin.TabularInline):
    model = RequestTask
    extra = 0
    fields = ['task', 'status_code']
    readonly_fields = ['status_code']


class RequestNotifyGroupInline(admin.TabularInline):
    model = RequestNotifyGroup
    extra = 0
    fields = ['notify_group', 'by_email', 'by_sms', 'by_phone']


class RequestCorpInline(admin.TabularInline):
    model = RequestCorp
    extra = 0
    fields = ['corp_code']


class RequestTeamInline(admin.TabularInline):
    model = RequestTeam
    extra = 0
    fields = ['team_code']


class RequestExtraInformationInline(admin.TabularInline):
    model = RequestExtraInformation
    extra = 0
    fields = ['extra_info']


class TaskUserInline(admin.TabularInline):
    model = TaskUser
    extra = 0
    fields = ['user_nationalcode', 'user_role_id', 'user_team_code', 'user_role_code']
    autocomplete_fields = ['user_nationalcode', 'user_role_id', 'user_team_code']


class RequestTask_ChangeTypeInline(admin.TabularInline):
    model = RequestTask_ChangeType
    extra = 0
    fields = ['task']


class RequestNotifyGroup_ChangeTypeInline(admin.TabularInline):
    model = RequestNotifyGroup_ChangeType
    extra = 0
    fields = ['notify_group', 'by_email', 'by_sms', 'by_phone']


class RequestCorp_ChangeTypeInline(admin.TabularInline):
    model = RequestCorp_ChangeType
    extra = 0
    fields = ['corp_code']


class RequestTeam_ChangeTypeInline(admin.TabularInline):
    model = RequestTeam_ChangeType
    extra = 0
    fields = ['team_code']


class RequestExtraInformation_ChangeTypeInline(admin.TabularInline):
    model = RequestExtraInformation_ChangeType
    extra = 0
    fields = ['extra_info']


class RequestTaskUserInline(admin.TabularInline):
    model = RequestTaskUser
    extra = 0
    fields = ['user_nationalcode', 'user_role_id', 'user_team_code', 'user_role_code']
    autocomplete_fields = ['user_nationalcode', 'user_role_id', 'user_team_code']


class TaskUserSelectedInline(admin.TabularInline):
    model = TaskUserSelected
    extra = 0
    fields = ['task_user', 'pickup_date', 'user_report_result', 'user_report_date', 'user_done_date']
    readonly_fields = ['pickup_date']


class RequestFlowInline(admin.TabularInline):
    model = RequestFlow
    extra = 0
    fields = ['user_nationalcode', 'user_role_code', 'user_opinion', 'receiver_date', 'send_date']
    readonly_fields = ['receiver_date']


# فرم‌های سفارشی
class ChangeTypeForm(ModelForm):
    class Meta:
        model = ChangeType
        fields = '__all__'
        widgets = {
            'change_description': Textarea(attrs={'rows': 4, 'cols': 80}),
            'role_back_plan_description': Textarea(attrs={'rows': 3, 'cols': 80}),
            'reason_other_description': Textarea(attrs={'rows': 3, 'cols': 80}),
            'change_location_other_description': Textarea(attrs={'rows': 3, 'cols': 80}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # استفاده از فیلدهای سفارشی
        self.fields['change_level'] = ChangeLevelChoiceField()
        self.fields['classification'] = ClassificationChoiceField()
        self.fields['priority'] = PriorityChoiceField()
        self.fields['risk_level'] = RiskLevelChoiceField()
        self.fields['change_domain'] = ChangeDomainChoiceField()

    def clean(self):
        cleaned_data = super().clean()
        # اعتبارسنجی سفارشی
        if cleaned_data.get('change_location_other') and not cleaned_data.get('change_location_other_description'):
            raise ValidationError('در صورت انتخاب "محل تغییر: سایر"، توضیحات الزامی است.')
        return cleaned_data


class ConfigurationChangeRequestForm(ModelForm):
    class Meta:
        model = ConfigurationChangeRequest
        fields = '__all__'
        widgets = {
            'change_description': Textarea(attrs={'rows': 4, 'cols': 80}),
            'role_back_plan_description': Textarea(attrs={'rows': 3, 'cols': 80}),
            'reason_other_description': Textarea(attrs={'rows': 3, 'cols': 80}),
            'change_location_other_description': Textarea(attrs={'rows': 3, 'cols': 80}),
            'changing_date': TextInput(attrs={'placeholder': '1403/01/01'}),
            'changing_time': TextInput(attrs={'placeholder': '14:30'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # استفاده از فیلدهای سفارشی
        self.fields['requestor_team_code'] = SearchableTeamChoiceField()
        self.fields['change_level'] = ChangeLevelChoiceField()
        self.fields['classification'] = ClassificationChoiceField()
        self.fields['priority'] = PriorityChoiceField()
        self.fields['risk_level'] = RiskLevelChoiceField()
        self.fields['change_domain'] = ChangeDomainChoiceField()


# کلاس‌های Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['national_code', 'fullname', 'username', 'gender_display', 'created_count']
    list_filter = [GenderFilter]
    search_fields = ['national_code', 'first_name', 'last_name', 'username']
    ordering = ['last_name', 'first_name']
    readonly_fields = ['national_code']
    inlines = [UserTeamRoleInline]
    
    fieldsets = (
        ('اطلاعات شخصی', {
            'fields': ('national_code', 'first_name', 'last_name', 'username', 'gender')
        }),
    )
    
    def gender_display(self, obj):
        return "مرد" if obj.gender else "زن"
    gender_display.short_description = 'جنسیت'
    
    def created_count(self, obj):
        return obj.created_configurationchangerequests.count()
    created_count.short_description = 'تعداد درخواست‌های ایجاد شده'


@admin.register(UserTeamRole)
class UserTeamRoleAdmin(admin.ModelAdmin):
    list_display = ['national_code', 'role_id', 'team_code', 'manager_national_code']
    list_filter = ['team_code', 'role_id']
    search_fields = ['national_code__first_name', 'national_code__last_name', 'team_code__team_name']
    autocomplete_fields = ['national_code', 'team_code', 'manager_national_code']


@admin.register(ConstValue)
class ConstValueAdmin(admin.ModelAdmin):
    list_display = ['Caption', 'Code', 'Parent', 'IsActive', 'OrderNumber', 'ConstValue', 'display_with_parent']
    list_filter = ['IsActive', 'Parent', ParentIdFilter]
    search_fields = ['Caption', 'Code']
    ordering = ['Parent', 'OrderNumber']
    
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': ('Caption', 'Code', 'Parent', 'IsActive', 'OrderNumber', 'ConstValue')
        }),
    )
    
    def display_with_parent(self, obj):
        """نمایش عنوان با شناسه پدر برای فرزندان"""
        if obj.Parent:
            return f"[{obj.Parent.Caption}] {obj.Caption}"
        return obj.Caption
    display_with_parent.short_description = 'عنوان با والد'
    
    def get_queryset(self, request):
        """فیلتر کردن بر اساس پیشوند"""
        qs = super().get_queryset(request)
        # اگر در URL پارامتر prefix وجود دارد، فیلتر کن
        prefix = request.GET.get('prefix')
        if prefix:
            qs = qs.filter(Code__startswith=prefix)
        return qs.filter(IsActive=True)


@admin.register(Corp)
class CorpAdmin(admin.ModelAdmin):
    list_display = ['corp_code', 'corp_name']
    search_fields = ['corp_code', 'corp_name']
    ordering = ['corp_name']
    
    def get_queryset(self, request):
        """بهینه‌سازی کوئری برای جستجو"""
        return super().get_queryset(request).order_by('corp_name')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['team_code', 'team_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['team_code', 'team_name']
    ordering = ['team_name']
    
    def get_queryset(self, request):
        """نمایش همه تیم‌ها در لیست ادمین"""
        return super().get_queryset(request)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['role_id', 'role_title']
    search_fields = ['role_title']
    ordering = ['role_title']


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ['title', 'administrator_nationalCode', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'administrator_nationalCode__first_name', 'administrator_nationalCode__last_name']
    autocomplete_fields = ['administrator_nationalCode']


@admin.register(ChangeType)
class ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'change_type_title', 'related_manager', 'need_committee', 'priority']
    list_filter = ['need_committee', 'priority', 'risk_level', 'change_level', 'classification']
    search_fields = ['code', 'change_type_title', 'change_title', 'related_manager__first_name']
    autocomplete_fields = ['related_manager', 'committee', 'change_level', 'classification', 'priority', 'risk_level', 'change_domain']
    form = ChangeTypeForm
    inlines = [
        RequestTask_ChangeTypeInline,
        RequestNotifyGroup_ChangeTypeInline,
        RequestCorp_ChangeTypeInline,
        RequestTeam_ChangeTypeInline,
        RequestExtraInformation_ChangeTypeInline
    ]
    
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': ('code', 'change_type_title', 'change_title', 'change_description', 'related_manager')
        }),
        ('محل تغییر', {
            'fields': ('change_location_data_center', 'change_location_database', 'change_location_systems', 
                      'change_location_other', 'change_location_other_description'),
            'classes': ('collapse',)
        }),
        ('کمیته', {
            'fields': ('need_committee', 'committee'),
            'classes': ('collapse',)
        }),
        ('ویژگی‌های تغییر', {
            'fields': ('change_level', 'classification', 'priority', 'risk_level', 'change_domain'),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('changing_duration', 'downtime_duration', 'downtime_duration_worstcase'),
            'classes': ('collapse',)
        }),
        ('تأثیرات خدمات', {
            'fields': ('stop_critical_service', 'critical_service_title', 'stop_sensitive_service', 
                      'stop_service_title', 'not_stop_any_service'),
            'classes': ('collapse',)
        }),
        ('برنامه بازگشت', {
            'fields': ('has_role_back_plan', 'role_back_plan_description'),
            'classes': ('collapse',)
        }),
        ('الزامات', {
            'fields': ('reason_regulatory', 'reason_technical', 'reason_security', 'reason_business', 
                      'reason_other', 'reason_other_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConfigurationChangeRequest)
class ConfigurationChangeRequestAdmin(admin.ModelAdmin):
    list_display = ['doc_id', 'change_title', 'status_code', 'requestor_nationalcode', 'change_type', 'changing_date', 'create_date']
    list_filter = [
        'status_code', 'change_type', 'priority', 'risk_level', 'change_level', 
        'classification', 'create_date', ClassificationFilter, PriorityFilter, 
        RiskLevelFilter, ChangeLevelFilter, ChangeDomainFilter, ActiveTeamFilter, CorpFilter
    ]
    search_fields = ['doc_id', 'change_title', 'requestor_nationalcode__first_name', 'requestor_nationalcode__last_name']
    autocomplete_fields = [
        'change_type', 'requestor_nationalcode', 'requestor_team_code', 'requestor_role_id',
        'direct_manager_nationalcode', 'related_manager_nationalcode', 'committee_user_nationalcode',
        'committee', 'change_level', 'classification', 'priority', 'risk_level', 'change_domain'
    ]
    form = ConfigurationChangeRequestForm
    inlines = [
        RequestTaskInline,
        RequestNotifyGroupInline,
        RequestCorpInline,
        RequestTeamInline,
        RequestExtraInformationInline,
        RequestFlowInline
    ]
    readonly_fields = ['create_date', 'modify_date']
    date_hierarchy = 'create_date'
    
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': ('doc_id', 'status_code', 'change_type', 'change_title', 'change_description')
        }),
        ('اطلاعات درخواست کننده', {
            'fields': ('requestor_nationalcode', 'requestor_team_code', 'requestor_role_id'),
        }),
        ('اطلاعات مدیران', {
            'fields': ('direct_manager_nationalcode', 'related_manager_nationalcode', 'committee_user_nationalcode'),
        }),
        ('کمیته', {
            'fields': ('need_committee', 'committee'),
            'classes': ('collapse',)
        }),
        ('ویژگی‌های تغییر', {
            'fields': ('change_level', 'classification', 'priority', 'risk_level', 'change_domain'),
            'classes': ('collapse',)
        }),
        ('محل تغییر', {
            'fields': ('change_location_data_center', 'change_location_database', 'change_location_systems', 
                      'change_location_other', 'change_location_other_description'),
            'classes': ('collapse',)
        }),
        ('زمان‌بندی', {
            'fields': ('changing_date', 'changing_time', 'changing_date_actual', 'changing_time_actual',
                      'changing_duration', 'changing_duration_actual', 'downtime_duration', 
                      'downtime_duration_worstcase', 'downtime_duration_actual'),
            'classes': ('collapse',)
        }),
        ('تأثیرات خدمات', {
            'fields': ('stop_critical_service', 'critical_service_title', 'stop_sensitive_service', 
                      'stop_service_title', 'not_stop_any_service'),
            'classes': ('collapse',)
        }),
        ('برنامه بازگشت', {
            'fields': ('has_role_back_plan', 'role_back_plan_description'),
            'classes': ('collapse',)
        }),
        ('الزامات', {
            'fields': ('reason_regulatory', 'reason_technical', 'reason_security', 'reason_business', 
                      'reason_other', 'reason_other_description'),
            'classes': ('collapse',)
        }),
        ('اطلاعات سیستم', {
            'fields': ('create_date', 'modify_date', 'creator_user', 'last_modifier_user'),
            'classes': ('collapse',)
        }),
    )


@admin.register(NotifyGroup)
class NotifyGroupAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'role_id', 'team_code', 'parent_group', 'has_children']
    list_filter = ['role_id', 'team_code', 'parent_group']
    search_fields = ['code', 'title', 'role_id__role_title', 'team_code__team_name']
    autocomplete_fields = ['role_id', 'team_code', 'parent_group']
    inlines = [NotifyGroupInline, NotifyGroupUserInline]
    
    fieldsets = (
        ('اطلاعات کلی', {
            'fields': ('code', 'title', 'parent_group')
        }),
        ('تعریف گروه', {
            'fields': ('role_id', 'team_code'),
            'description': 'گروه می‌تواند بر اساس سمت، تیم یا هر دو تعریف شود'
        }),
    )
    
    def has_children(self, obj):
        """نمایش وجود زیرگروه‌ها"""
        return obj.child_groups.exists()
    has_children.boolean = True
    has_children.short_description = 'دارای زیرگروه'


@admin.register(NotifyGroupUser)
class NotifyGroupUserAdmin(admin.ModelAdmin):
    list_display = ['notify_group_code', 'user_nationalcode', 'user_role_id', 'user_team_code']
    list_filter = ['notify_group_code', 'user_role_id', 'user_team_code']
    search_fields = ['user_nationalcode__first_name', 'user_nationalcode__last_name']
    autocomplete_fields = ['notify_group_code', 'user_nationalcode', 'user_role_id', 'user_team_code']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'test_required', 'order_number']
    list_filter = ['test_required']
    search_fields = ['title']
    ordering = ['order_number', 'title']
    inlines = [TaskUserInline]


@admin.register(TaskUser)
class TaskUserAdmin(admin.ModelAdmin):
    list_display = ['task', 'user_nationalcode', 'user_role_id', 'user_team_code', 'user_role_code']
    list_filter = ['task', 'user_role_code', 'user_role_id', 'user_team_code']
    search_fields = ['task__title', 'user_nationalcode__first_name', 'user_nationalcode__last_name']
    autocomplete_fields = ['task', 'user_nationalcode', 'user_role_id', 'user_team_code']


@admin.register(RequestTask)
class RequestTaskAdmin(admin.ModelAdmin):
    list_display = ['request', 'task', 'status_code']
    list_filter = ['status_code', 'task', 'request__change_type']
    search_fields = ['request__change_title', 'task__title']
    autocomplete_fields = ['request', 'task']
    inlines = [RequestTaskUserInline, TaskUserSelectedInline]


@admin.register(TaskUserSelected)
class TaskUserSelectedAdmin(admin.ModelAdmin):
    list_display = ['task_user', 'request_task', 'pickup_date', 'user_report_result', 'user_report_date']
    list_filter = ['user_report_result', 'pickup_date', 'request_task__status_code']
    search_fields = ['task_user__user_nationalcode__first_name', 'request_task__request__change_title']
    readonly_fields = ['pickup_date']
    autocomplete_fields = ['task_user', 'request_task']


@admin.register(RequestTask_ChangeType)
class RequestTask_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ['changetype', 'task']
    list_filter = ['changetype', 'task']
    search_fields = ['changetype__change_type_title', 'task__title']
    autocomplete_fields = ['changetype', 'task']


@admin.register(RequestTaskUser)
class RequestTaskUserAdmin(admin.ModelAdmin):
    list_display = ['request_task', 'user_nationalcode', 'user_role_code']
    list_filter = ['user_role_code', 'request_task__status_code']
    search_fields = ['request_task__request__change_title', 'user_nationalcode__first_name']
    autocomplete_fields = ['request_task', 'user_nationalcode', 'user_role_id', 'user_team_code']


@admin.register(RequestFlow)
class RequestFlowAdmin(admin.ModelAdmin):
    list_display = ['request', 'user_nationalcode', 'user_opinion', 'receiver_date', 'send_date', 'workflow_status_display']
    list_filter = [WorkflowStatusFilter, 'user_opinion', 'receiver_date', 'user_role_code']
    search_fields = ['request__change_title', 'user_nationalcode__first_name']
    readonly_fields = ['receiver_date']
    autocomplete_fields = ['request', 'user_nationalcode', 'user_role_id', 'user_team_code', 'user_role_code', 'user_opinion']
    
    def workflow_status_display(self, obj):
        """نمایش وضعیت گردش"""
        if obj.send_date is None:
            return "در انتظار"
        elif obj.user_opinion and 'تایید' in obj.user_opinion.Caption:
            return "تکمیل شده"
        elif obj.user_opinion and 'رد' in obj.user_opinion.Caption:
            return "رد شده"
        elif obj.user_opinion and 'بازگشت' in obj.user_opinion.Caption:
            return "بازگشت داده شده"
        return "نامشخص"
    workflow_status_display.short_description = 'وضعیت گردش'


@admin.register(RequestNotifyGroup)
class RequestNotifyGroupAdmin(admin.ModelAdmin):
    list_display = ['request', 'notify_group', 'by_email', 'by_sms', 'by_phone']
    list_filter = ['by_email', 'by_sms', 'by_phone', 'notify_group']
    search_fields = ['request__change_title', 'notify_group__title']
    autocomplete_fields = ['request', 'notify_group']


@admin.register(RequestNotifyGroup_ChangeType)
class RequestNotifyGroup_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ['changetype', 'notify_group', 'by_email', 'by_sms', 'by_phone']
    list_filter = ['by_email', 'by_sms', 'by_phone', 'notify_group']
    search_fields = ['changetype__change_type_title', 'notify_group__title']
    autocomplete_fields = ['changetype', 'notify_group']


@admin.register(RequestCorp_ChangeType)
class RequestCorp_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ['changetype', 'corp_code']
    list_filter = ['changetype', 'corp_code']
    search_fields = ['changetype__change_type_title', 'corp_code__corp_name']
    autocomplete_fields = ['changetype', 'corp_code']


@admin.register(RequestTeam_ChangeType)
class RequestTeam_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ['changetype', 'team_code']
    list_filter = ['changetype', 'team_code']
    search_fields = ['changetype__change_type_title', 'team_code__team_name']
    autocomplete_fields = ['changetype', 'team_code']


@admin.register(RequestExtraInformation_ChangeType)
class RequestExtraInformation_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ['extra_info', 'change_type']
    list_filter = ['change_type', 'extra_info']
    search_fields = ['change_type__change_type_title', 'extra_info__Caption']
    autocomplete_fields = ['extra_info', 'change_type']


@admin.register(RequestCorp)
class RequestCorpAdmin(admin.ModelAdmin):
    list_display = ['request', 'corp_code']
    list_filter = ['corp_code', 'request__change_type']
    search_fields = ['request__change_title', 'corp_code__corp_name']
    autocomplete_fields = ['request', 'corp_code']


@admin.register(RequestTeam)
class RequestTeamAdmin(admin.ModelAdmin):
    list_display = ['request', 'team_code']
    list_filter = ['team_code', 'request__change_type']
    search_fields = ['request__change_title', 'team_code__team_name']
    autocomplete_fields = ['request', 'team_code']


@admin.register(RequestExtraInformation)
class RequestExtraInformationAdmin(admin.ModelAdmin):
    list_display = ['extra_info', 'request']
    list_filter = ['extra_info', 'request__change_type']
    search_fields = ['request__change_title', 'extra_info__Caption']
    autocomplete_fields = ['extra_info', 'request']

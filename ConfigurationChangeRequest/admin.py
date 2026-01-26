from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.forms import ModelForm
from .models import (
    User, Team, Role, UserTeamRole, ConstValue, Corp, Committee, ChangeType,
    NotifyGroup, NotifyGroupUser, ConfigurationChangeRequest, Task, TaskUser,
    RequestTask, RequestTask_ChangeType, RequestTaskUser, RequestTaskUserSelected,
    RequestFlow, RequestNotifyGroup, RequestNotifyGroup_ChangeType,
    RequestCorp_ChangeType, RequestTeam_ChangeType, RequestExtraInformation_ChangeType,
    RequestCorp, RequestTeam, RequestExtraInformation, NotificationLog, DataHistory
)
from .admin_views import ConfigurationChangeRequestChangeList, UserChangeList, TeamChangeList, RequestExtraInformationChangeList
from .admin_widgets import (
    RTLCheckboxSelectMultiple, RTLCheckboxInput, RTLRadioSelect,
    RTLSelect, RTLTextInput, RTLTextarea
)

# =======================
# Filters
# =======================
class TeamActiveFilter(SimpleListFilter):
    title = _('وضعیت تیم')
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (('active', _('فعال')), ('inactive', _('غیرفعال')))

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        elif self.value() == 'inactive':
            return queryset.filter(is_active=False)
        return queryset


class GenderFilter(SimpleListFilter):
    title = _('جنسیت')
    parameter_name = 'gender'

    def lookups(self, request, model_admin):
        return (('male', _('مرد')), ('female', _('زن')))

    def queryset(self, request, queryset):
        if self.value() == 'male':
            return queryset.filter(gender=True)
        elif self.value() == 'female':
            return queryset.filter(gender=False)
        return queryset


class ParentConstValueFilter(SimpleListFilter):
    title = _('شناسه پدر')
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        parents = ConstValue.objects.filter(Parent__isnull=True).order_by('Caption')
        return [(p.id, p.Caption) for p in parents]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Parent_id=self.value())
        return queryset


class PriorityFilter(SimpleListFilter):
    title = _('اولویت')
    parameter_name = 'priority'

    def lookups(self, request, model_admin):
        parent = ConstValue.objects.filter(Code__startswith='Priority').first()
        if parent:
            return [(p.id, p.Caption) for p in ConstValue.objects.filter(Parent=parent)]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(priority_id=self.value())
        return queryset


class TeamFilter(SimpleListFilter):
    title = _('تیم')
    parameter_name = 'team'

    def lookups(self, request, model_admin):
        teams = Team.objects.filter(is_active=True).order_by('team_name')
        return [(t.team_code, t.team_name) for t in teams]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(team_code=self.value())
        return queryset


class ExtraInfoParentFilter(SimpleListFilter):
    title = _('گروه اطلاعات تکمیلی')
    parameter_name = 'extra_info_parent'

    def lookups(self, request, model_admin):
        parents = ConstValue.objects.filter(Parent__isnull=True, Code__icontains='extra').order_by('Caption')
        return [(p.id, p.Caption) for p in parents]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(extra_info__Parent_id=self.value())
        return queryset

# =======================
# Forms
# =======================
class UserAdminForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'gender': RTLRadioSelect(choices=[(True, 'مرد'), (False, 'زن')]),
            'first_name': RTLTextInput,
            'last_name': RTLTextInput,
            'username': RTLTextInput,
            'national_code': RTLTextInput,
        }


class TeamAdminForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        widgets = {
            'is_active': RTLRadioSelect(choices=[(True, 'فعال'), (False, 'غیرفعال')]),
            'team_code': RTLTextInput,
            'team_name': RTLTextInput,
        }


class ConstValueAdminForm(ModelForm):
    class Meta:
        model = ConstValue
        fields = '__all__'
        widgets = {
            'Caption': RTLTextInput,
            'Code': RTLTextInput,
            'Parent': RTLSelect,
            'IsActive': RTLRadioSelect(choices=[(True, 'فعال'), (False, 'غیرفعال')]),
            'OrderNumber': RTLTextInput,
            'ConstValue': RTLTextInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Parent'].queryset = ConstValue.objects.filter(Parent__isnull=True)


class ConfigurationChangeRequestAdminForm(ModelForm):
    class Meta:
        model = ConfigurationChangeRequest
        fields = '__all__'
        widgets = {
            'change_title': RTLTextInput,
            'change_description': RTLTextarea,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parent = ConstValue.objects.filter(Code__startswith='Priority').first()
        if parent:
            self.fields['priority'].queryset = ConstValue.objects.filter(Parent=parent)


class RequestExtraInformationAdminForm(ModelForm):
    class Meta:
        model = RequestExtraInformation
        fields = '__all__'
        widgets = {'extra_info': RTLSelect, 'request': RTLSelect}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        parents = ConstValue.objects.filter(Parent__isnull=True, Code__icontains='extra')
        if parents.exists():
            self.fields['extra_info'].queryset = ConstValue.objects.filter(Parent__in=parents)

# =======================
# Admins
# =======================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('national_code', 'first_name', 'last_name', 'username', 'gender_display', 'get_team', 'get_role')
    list_filter = (GenderFilter,)
    search_fields = ('national_code', 'first_name', 'last_name', 'username')
    ordering = ('first_name', 'last_name')

    def get_changelist(self, request, **kwargs):
        return UserChangeList

    def gender_display(self, obj):
        return 'مرد' if obj.gender else 'زن'
    gender_display.short_description = 'جنسیت'

    def get_team(self, obj):
        return obj.get_team
    get_team.short_description = 'تیم'

    def get_role(self, obj):
        return obj.get_role
    get_role.short_description = 'سمت'


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm
    list_display = ('team_code', 'team_name', 'is_active_display')
    list_filter = (TeamActiveFilter,)
    search_fields = ('team_code', 'team_name')
    ordering = ('team_name',)

    def get_changelist(self, request, **kwargs):
        return TeamChangeList

    def is_active_display(self, obj):
        return format_html('<span style="color:{};">{}</span>', 'green' if obj.is_active else 'red',
                           'فعال' if obj.is_active else 'غیرفعال')
    is_active_display.short_description = 'وضعیت'


@admin.register(ConfigurationChangeRequest)
class ConfigurationChangeRequestAdmin(admin.ModelAdmin):
    form = ConfigurationChangeRequestAdminForm
    list_display = ('id', 'change_title', 'requestor_nationalcode', 'status_code', 'priority', 'change_type')
    list_filter = ('status_code', PriorityFilter, 'change_type')
    search_fields = ('change_title', 'requestor_nationalcode__first_name', 'requestor_nationalcode__last_name')

    def get_changelist(self, request, **kwargs):
        return ConfigurationChangeRequestChangeList


@admin.register(RequestExtraInformation)
class RequestExtraInformationAdmin(admin.ModelAdmin):
    form = RequestExtraInformationAdminForm
    list_display = ('request', 'extra_info', 'extra_info_parent', 'is_active_display')
    list_filter = (ExtraInfoParentFilter, 'extra_info')
    search_fields = ('extra_info__Caption', 'request__change_title')

    def get_changelist(self, request, **kwargs):
        return RequestExtraInformationChangeList

    def extra_info_parent(self, obj):
        return obj.extra_info.Parent.Caption if obj.extra_info and obj.extra_info.Parent else '-'
    extra_info_parent.short_description = 'گروه اطلاعات تکمیلی'

    def is_active_display(self, obj):
        return format_html('<span style="color:green;">✓ فعال</span>')
    is_active_display.short_description = 'وضعیت'



@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('title', 'administrator_display', 'is_active_icon')
    list_filter = ('is_active',)
    search_fields = ('title', 'administrator_nationalcode__first_name', 'administrator_nationalcode__last_name')
    autocomplete_fields = ['administrator_nationalcode']
    
    def is_active_icon(self, obj):
        icon = 'fa-check-circle text-success' if obj.is_active else 'fa-times-circle text-danger'
        title = 'فعال' if obj.is_active else 'غیرفعال'
        return format_html(f'<i class="fa {icon} fa-lg is-active-icon" title="{title}"></i>')
    is_active_icon.short_description = 'وضعیت فعال'
    
    class Media:
        css = {
        'all': (
            'ConfigurationChangeRequest/css/all.min.css',
            'admin/css/admin.css',
        )
        }

    def administrator_display(self, obj):
        if obj.administrator_nationalcode:
            username_part = obj.administrator_nationalcode.username.split('@')[0]
            fullname = obj.administrator_nationalcode.fullname
            fullname_gender = obj.administrator_nationalcode.fullname_gender
            return format_html(
                f"""
                <div style="display:flex; align-items:center;">
                    <img src="/static/ConfigurationChangeRequest/images/personnel/{username_part}.jpg" 
                        onerror="this.src='/static/ConfigurationChangeRequest/images/Avatar.png';" 
                        alt="{fullname}" title="{fullname}" 
                        style="width:45px;height:45px;border-radius:50%;margin-left:6px;object-fit:cover;">
                    <span>{ fullname_gender }</span>
                </div>
                """
            )
        return "-"
    administrator_display.short_description = "دبیر کمیته"        
        
# سایر مدل‌ها (بدون تغییر ظاهری)
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_title')
    list_filter = ('role_id',)
    search_fields = ('role_title',)

@admin.register(UserTeamRole)
class UserTeamRoleAdmin(admin.ModelAdmin):
    list_display = ('national_code', 'role_id', 'team_code', 'manager_national_code')
    list_filter = ('role_id', 'team_code')
    search_fields = ('national_code__first_name', 'national_code__last_name', 'role_id__role_title', 'team_code__team_name')

@admin.register(ConstValue)
class ConstValueAdmin(admin.ModelAdmin):
    list_display = ('Caption', 'Code', 'Parent', 'IsActive', 'OrderNumber', 'ConstValue')
    list_filter = ('Parent', 'IsActive')
    search_fields = ('Caption', 'Code')


@admin.register(Corp)
class CorpAdmin(admin.ModelAdmin):
    list_display = ('corp_code', 'corp_name')
    list_filter = ('corp_code',)
    search_fields = ('corp_name',)

@admin.register(ChangeType)
class ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'change_type_title', 'change_title', 'change_description', 'related_manager_nationalcode', 'change_location_data_center', 'change_location_database', 'change_location_system_services', 'change_location_other', 'change_location_other_description', 'need_committee', 'committee', 'change_level', 'classification', 'priority', 'risk_level', 'change_domain', 'stop_critical_service', 'critical_service_title', 'stop_sensitive_service', 'stop_service_title', 'downtime_duration', 'downtime_duration_worstcase', 'has_role_back_plan', 'role_back_plan_description', 'reason_regulatory', 'reason_technical', 'reason_security', 'reason_business', 'reason_other', 'reason_other_description', 'changing_duration')
    list_filter = ('change_type_title','code')
    search_fields = ('change_type_title',)

@admin.register(NotifyGroup)
class NotifyGroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'role_id', 'team_code')
    list_filter = ('code',)
    search_fields = ('title',)

@admin.register(NotifyGroupUser)
class NotifyGroupUserAdmin(admin.ModelAdmin):
    list_display = ('notify_group', 'user_nationalcode', 'user_role_id', 'user_team_code')
    list_filter = ('notify_group', 'user_role_id', 'user_team_code')
    search_fields = ('user_nationalcode__first_name', 'user_nationalcode__last_name', 'user_role_id__role_title', 'user_team_code__team_name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'test_required', 'order_number')
    list_filter = ('test_required',)
    search_fields = ('title',)
    

class ExecutorInline(admin.TabularInline):
    model = TaskUser
    extra = 0
    verbose_name = "مجری"
    verbose_name_plural = "مجریان"
    fields = ('user_nationalcode', 'user_role_id', 'user_team_code', 'is_active')
    autocomplete_fields = ['user_nationalcode', 'user_role_id', 'user_team_code']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_role_code='E')


class TesterInline(admin.TabularInline):
    model = TaskUser
    extra = 0
    verbose_name = "تستر"
    verbose_name_plural = "تسترها"
    fields = ('user_nationalcode', 'user_role_id', 'user_team_code', 'is_active')
    autocomplete_fields = ['user_nationalcode', 'user_role_id', 'user_team_code']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user_role_code='T')


@admin.register(TaskUser)
class TaskUserAdmin(admin.ModelAdmin):
    list_display = ('task', 'user_nationalcode', 'user_role_id', 'user_team_code', 'is_active')
    list_filter = ('user_role_id', 'is_active', 'user_team_code')
    search_fields = ('user_nationalcode__first_name', 'user_nationalcode__last_name', 'user_role_id__role_title', 'user_team_code__team_name')
    # autocomplete_fields = ['task', 'user_nationalcode', 'user_role_id', 'user_team_code']
    # inlines = [ExecutorInline, TesterInline]
        
    def user_display(self, obj):
        """نمایش نام کامل کاربر"""
        return f"{obj.user_nationalcode.first_name} {obj.user_nationalcode.last_name}"
    user_display.short_description = "کاربر"

    def user_role_icon(self, obj):
        """نمایش نقش با آیکون رنگی FontAwesome"""
        if obj.user_role_code == 'E':
            icon = 'fa-user-cog text-primary'
            title = 'مجری'
        else:
            icon = 'fa-vial text-warning'
            title = 'تستر'
        return format_html(f'<i class="fa {icon}" title="{title}"></i> {title}')
    user_role_icon.short_description = "نقش در تسک"

    class Media:
        css = {
            'all': (
                'ConfigurationChangeRequest/css/all.min.css',  # FontAwesome
                'admin/css/admin.css',  # استایل سفارشی در صورت نیاز
            )
        }


@admin.register(RequestTask)
class RequestTaskAdmin(admin.ModelAdmin):
    list_display = ('request', 'task', 'order_number', 'status_code')
    list_filter = ( 'task', 'status_code')
    search_fields = ('request__change_title', 'task__title')

@admin.register(RequestTask_ChangeType)
class RequestTask_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ('changetype', 'task', 'order_number')
    list_filter = ('changetype', 'task')
    search_fields = ('changetype__change_type_title', 'task__title')

@admin.register(RequestTaskUser)
class RequestTaskUserAdmin(admin.ModelAdmin):
    list_display = ('request_task', 'user_nationalcode', 'user_role_id', 'user_team_code','user_role_code')
    list_filter = ('request_task', 'user_role_id', 'user_team_code')
    search_fields = ('user_nationalcode__first_name', 'user_nationalcode__last_name', 'user_role_id__role_title', 'user_team_code__team_name')

@admin.register(RequestTaskUserSelected)
class RequestTaskUserSelectedAdmin(admin.ModelAdmin):
    list_display = ('request_task_user', 'pickup_date', 'user_report_result', 'user_report_date', 'user_report_time', 'user_done_date', 'user_done_time', 'user_report_description')
    list_filter = ('request_task_user', 'pickup_date', 'user_report_result', 'user_report_date', 'user_report_time', 'user_done_date', 'user_done_time')
    search_fields = ('request_task_user__user_nationalcode__first_name', 'request_task_user__user_nationalcode__last_name', 'user_report_description')

# @admin.register(RequestFlow)
# class RequestFlowAdmin(admin.ModelAdmin):
#     list_display = ('request', 'user_nationalcode', 'user_role_id', 'user_team_code', 'receiver_date', 'send_date', 'fields_value', 'user_send_date', 'user_send_time', 'user_reject_description')
#     list_filter = ( 'user_team_code',)
#     search_fields = ('request__change_title', 'user_nationalcode__first_name', 'user_nationalcode__last_name', 'user_role_id__role_title', 'user_team_code__team_name')

@admin.register(RequestNotifyGroup)
class RequestNotifyGroupAdmin(admin.ModelAdmin):
    list_display = ('request', 'notify_group', 'by_email', 'by_sms', 'by_phone')
    list_filter = ( 'notify_group', 'by_email', 'by_sms', 'by_phone')
    search_fields = ('request', 'notify_group__title')

@admin.register(RequestNotifyGroup_ChangeType)
class RequestNotifyGroup_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ('changetype', 'notify_group', 'by_email', 'by_sms', 'by_phone')
    list_filter = ('changetype', 'notify_group', 'by_email', 'by_sms', 'by_phone')
    search_fields = ('changetype', 'notify_group__title')

@admin.register(RequestCorp_ChangeType)
class RequestCorp_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ('changetype', 'corp_code')
    list_filter = ('changetype', 'corp_code')
    search_fields = ('changetype__change_type_title', 'corp_code__corp_name')

@admin.register(RequestTeam_ChangeType)
class RequestTeam_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ('changetype', 'team_code')
    list_filter = ( 'team_code','changetype')
    search_fields = ('changetype__change_type_title', 'team_code__team_name')

@admin.register(RequestExtraInformation_ChangeType)
class RequestExtraInformation_ChangeTypeAdmin(admin.ModelAdmin):
    list_display = ('extra_info', 'changetype')
    list_filter = ('changetype',)
    search_fields = ('changetype',)

@admin.register(RequestCorp)
class RequestCorpAdmin(admin.ModelAdmin):
    list_display = ('request', 'corp_code', )
    list_filter = ('corp_code',)
    search_fields = ('request__change_title', 'corp_code__corp_name')

@admin.register(RequestTeam)
class RequestTeamAdmin(admin.ModelAdmin):
    list_display = ('request', 'team_code')
    list_filter = ('team_code',)
    search_fields = ('request__change_title', 'team_code__team_name')

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('request', 'request_status', 'task_status','template_code','email_to','email_cc','email_bcc','variables','service_data','service_return_val')
    list_filter = ('request', 'request_status', 'task_status','template_code','email_to','variables')
    search_fields = ('request__change_title', 'request_status', 'task_status','template_code','email_to')

@admin.register(DataHistory)
class DataHistoryAdmin(admin.ModelAdmin):
    list_display = ('record_type','old_data','new_data','record_id')
    list_filter = ('record_type',)
    search_fields = ('record_type', 'record_id')

# =======================
# Admin Site Config
# =======================
admin.site.site_header = 'پنل مدیریت سیستم درخواست تغییرات'
admin.site.site_title = 'پنل مدیریت'
admin.site.index_title = 'مدیریت سیستم درخواست تغییرات'

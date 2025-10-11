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


# سایر مدل‌ها (بدون تغییر ظاهری)
admin.site.register(Role)
admin.site.register(UserTeamRole)
admin.site.register(ConstValue)
admin.site.register(Corp)
admin.site.register(Committee)
admin.site.register(ChangeType)
admin.site.register(NotifyGroup)
admin.site.register(NotifyGroupUser)
admin.site.register(Task)
admin.site.register(TaskUser)
admin.site.register(RequestTask)
admin.site.register(RequestTask_ChangeType)
admin.site.register(RequestTaskUser)
admin.site.register(RequestTaskUserSelected)
admin.site.register(RequestFlow)
admin.site.register(RequestNotifyGroup)
admin.site.register(RequestNotifyGroup_ChangeType)
admin.site.register(RequestCorp_ChangeType)
admin.site.register(RequestTeam_ChangeType)
admin.site.register(RequestExtraInformation_ChangeType)
admin.site.register(RequestCorp)
admin.site.register(RequestTeam)
admin.site.register(NotificationLog)
admin.site.register(DataHistory)

# =======================
# Admin Site Config
# =======================
admin.site.site_header = 'پنل مدیریت سیستم درخواست تغییرات'
admin.site.site_title = 'پنل مدیریت'
admin.site.index_title = 'مدیریت سیستم درخواست تغییرات'

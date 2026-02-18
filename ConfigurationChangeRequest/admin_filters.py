from django.contrib.admin import SimpleListFilter
from django.db.models import Q
from .models import ConstValue, Team, Corp


class ClassificationFilter(SimpleListFilter):
    """فیلتر طبقه‌بندی"""
    title = 'طبقه‌بندی'
    parameter_name = 'classification'

    def lookups(self, request, model_admin):
        classifications = ConstValue.objects.filter(
            Code__startswith='Classification_',
            IsActive=True
        ).order_by('OrderNumber')
        return [(cv.Code, cv.Caption) for cv in classifications]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(classification__Code=self.value())
        return queryset


class PriorityFilter(SimpleListFilter):
    """فیلتر اولویت - فقط زیر مجموعه‌ها"""
    title = 'اولویت'
    parameter_name = 'priority'

    def lookups(self, request, model_admin):
        # ابتدا والد اولویت را پیدا کن
        parent_priority = ConstValue.objects.filter(
            Code__startswith='Priority_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_priority:
            # فقط فرزندان والد را نمایش بده
            priorities = ConstValue.objects.filter(
                Parent=parent_priority,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            priorities = ConstValue.objects.filter(
                Code__startswith='Priority_',
                IsActive=True
            ).order_by('OrderNumber')
        
        return [(cv.Code, cv.Caption) for cv in priorities]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(priority__Code=self.value())
        return queryset


class RiskLevelFilter(SimpleListFilter):
    """فیلتر سطح ریسک - فقط زیر مجموعه‌ها"""
    title = 'سطح ریسک'
    parameter_name = 'risk_level'

    def lookups(self, request, model_admin):
        # ابتدا والد سطح ریسک را پیدا کن
        parent_risk = ConstValue.objects.filter(
            Code__startswith='Risk_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_risk:
            # فقط فرزندان والد را نمایش بده
            risk_levels = ConstValue.objects.filter(
                Parent=parent_risk,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            risk_levels = ConstValue.objects.filter(
                Code__startswith='Risk_',
                IsActive=True
            ).order_by('OrderNumber')
        
        return [(cv.Code, cv.Caption) for cv in risk_levels]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(risk_level__Code=self.value())
        return queryset


class ChangeLevelFilter(SimpleListFilter):
    """فیلتر گستردگی تغییرات - فقط زیر مجموعه‌ها"""
    title = 'گستردگی تغییرات'
    parameter_name = 'change_level'

    def lookups(self, request, model_admin):
        # ابتدا والد گستردگی تغییرات را پیدا کن
        parent_level = ConstValue.objects.filter(
            Code__startswith='ChangeLevel_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_level:
            # فقط فرزندان والد را نمایش بده
            change_levels = ConstValue.objects.filter(
                Parent=parent_level,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            change_levels = ConstValue.objects.filter(
                Code__startswith='ChangeLevel_',
                IsActive=True
            ).order_by('OrderNumber')
        
        return [(cv.Code, cv.Caption) for cv in change_levels]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(change_level__Code=self.value())
        return queryset


class ChangeDomainFilter(SimpleListFilter):
    """فیلتر دامنه تغییر - فقط زیر مجموعه‌ها"""
    title = 'دامنه تغییر'
    parameter_name = 'change_domain'

    def lookups(self, request, model_admin):
        # ابتدا والد دامنه تغییر را پیدا کن
        parent_domain = ConstValue.objects.filter(
            Code__startswith='ChangeDomain_',
            Parent__isnull=True,
            IsActive=True
        ).first()
        
        if parent_domain:
            # فقط فرزندان والد را نمایش بده
            change_domains = ConstValue.objects.filter(
                Parent=parent_domain,
                IsActive=True
            ).order_by('OrderNumber')
        else:
            # اگر والد پیدا نشد، از روش قبلی استفاده کن
            change_domains = ConstValue.objects.filter(
                Code__startswith='ChangeDomain_',
                IsActive=True
            ).order_by('OrderNumber')
        
        return [(cv.Code, cv.Caption) for cv in change_domains]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(change_domain__Code=self.value())
        return queryset


class ActiveTeamFilter(SimpleListFilter):
    """فیلتر تیم‌های فعال"""
    title = 'تیم فعال'
    parameter_name = 'active_team'

    def lookups(self, request, model_admin):
        active_teams = Team.objects.filter(is_active=True).order_by('team_name')
        return [(team.team_code, team.team_name) for team in active_teams]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(requestor_team_code__team_code=self.value())
        return queryset


class WorkflowStatusFilter(SimpleListFilter):
    """فیلتر وضعیت گردش درخواست"""
    title = 'وضعیت گردش'
    parameter_name = 'workflow_status'

    def lookups(self, request, model_admin):
        return (
            ('pending', 'در انتظار'),
            ('completed', 'تکمیل شده'),
            ('rejected', 'رد شده'),
            ('returned', 'بازگشت داده شده'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'pending':
            return queryset.filter(send_date__isnull=True)
        elif self.value() == 'completed':
            return queryset.filter(send_date__isnull=False, user_opinion__Caption__icontains='تایید')
        elif self.value() == 'rejected':
            return queryset.filter(send_date__isnull=False, user_opinion__Caption__icontains='رد')
        elif self.value() == 'returned':
            return queryset.filter(send_date__isnull=False, user_opinion__Caption__icontains='بازگشت')
        return queryset


class GenderFilter(SimpleListFilter):
    """فیلتر جنسیت"""
    title = 'جنسیت'
    parameter_name = 'gender'

    def lookups(self, request, model_admin):
        return (
            ('male', 'مرد'),
            ('female', 'زن'),
            ('all', 'همه'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'male':
            return queryset.filter(gender=True)
        elif self.value() == 'female':
            return queryset.filter(gender=False)
        elif self.value() == 'all':
            return queryset
        return queryset


class ParentIdFilter(SimpleListFilter):
    """فیلتر شناسه پدر - فقط والدین"""
    title = 'شناسه پدر'
    parameter_name = 'parent_id'

    def lookups(self, request, model_admin):
        # فقط والدین را نمایش بده (رکوردهایی که خودشان والد هستند)
        parents = ConstValue.objects.filter(
            Parent__isnull=True,
            IsActive=True
        ).order_by('OrderNumber')
        
        return [(cv.id, cv.Caption) for cv in parents]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Parent_id=self.value())
        return queryset


class CorpFilter(SimpleListFilter):
    """فیلتر شرکت"""
    title = 'شرکت'
    parameter_name = 'corp'

    def lookups(self, request, model_admin):
        corps = Corp.objects.all().order_by('corp_name')
        return [(corp.corp_code, corp.corp_name) for corp in corps]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(requestor_nationalcode__corp_code__corp_code=self.value())
        return queryset

from django.contrib.admin.views.main import ChangeList
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from .models import ConfigurationChangeRequest, User, Team, RequestExtraInformation


# ==============================
# ConfigurationChangeRequest Stats
# ==============================
class ConfigurationChangeRequestChangeList(ChangeList):
    """لیست تغییرات درخواست پیکربندی با آمار خلاصه"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # آمار درخواست‌ها
        context['total_requests'] = ConfigurationChangeRequest.objects.count()
        context['pending_requests'] = ConfigurationChangeRequest.objects.filter(
            status_code__in=['DRAFTD', 'DIRMAN', 'RELMAN', 'COMITE', 'DOTASK']
        ).count()
        context['approved_requests'] = ConfigurationChangeRequest.objects.filter(
            status_code='APPROVED'
        ).count()
        context['rejected_requests'] = ConfigurationChangeRequest.objects.filter(
            status_code='REJECTED'
        ).count()

        # آمار کاربر و تیم مرتبط
        context['active_users'] = User.objects.count()
        context['active_teams'] = Team.objects.filter(is_active=True).count()
        return context


# ==============================
# User Stats
# ==============================
class UserChangeList(ChangeList):
    """لیست کاربران با آمار خلاصه"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_users'] = User.objects.count()
        context['male_users'] = User.objects.filter(gender=True).count()
        context['female_users'] = User.objects.filter(gender=False).count()
        context['teams_connected'] = Team.objects.filter(is_active=True).count()
        return context


# ==============================
# Team Stats
# ==============================
class TeamChangeList(ChangeList):
    """لیست تیم‌ها با آمار خلاصه"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_teams'] = Team.objects.count()
        context['active_teams'] = Team.objects.filter(is_active=True).count()
        context['inactive_teams'] = Team.objects.filter(is_active=False).count()

        # شمارش اعضای هر تیم
        context['team_with_most_users'] = (
            Team.objects.annotate(user_count=Count('userteamrole'))
            .order_by('-user_count')
            .first()
        )
        return context


# ==============================
# RequestExtraInformation Stats
# ==============================
class RequestExtraInformationChangeList(ChangeList):
    """لیست اطلاعات تکمیلی با آمار"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_extra_info'] = RequestExtraInformation.objects.count()
        context['with_parent'] = RequestExtraInformation.objects.filter(extra_info__Parent__isnull=False).count()
        context['without_parent'] = RequestExtraInformation.objects.filter(extra_info__Parent__isnull=True).count()

        # شمارش فعال/غیرفعال
        context['active_info'] = RequestExtraInformation.objects.filter(extra_info__IsActive=True).count()
        context['inactive_info'] = RequestExtraInformation.objects.filter(extra_info__IsActive=False).count()
        return context

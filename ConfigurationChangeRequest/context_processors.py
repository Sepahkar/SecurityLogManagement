"""
Context processors for admin panel customization
"""

from django.conf import settings
from .models import ConfigurationChangeRequest, User, Team


def admin_context(request):
    """
    Add custom context variables for admin templates
    """
    context = {}
    
    if request.path.startswith('/admin/'):
        # Add dashboard statistics
        try:
            context.update({
                'total_requests': ConfigurationChangeRequest.objects.count(),
                'pending_requests': ConfigurationChangeRequest.objects.filter(status_code='DRAFTD').count(),
                'completed_requests': ConfigurationChangeRequest.objects.filter(status_code='FINISH').count(),
                'total_users': User.objects.count(),
                'active_teams': Team.objects.filter(is_active=True).count(),
            })
        except Exception:
            # In case of database errors, provide default values
            context.update({
                'total_requests': 0,
                'pending_requests': 0,
                'completed_requests': 0,
                'total_users': 0,
                'active_teams': 0,
            })
        
        # Add admin settings
        context.update({
            'admin_site_header': getattr(settings, 'ADMIN_SITE_HEADER', 'مدیریت سیستم'),
            'admin_site_title': getattr(settings, 'ADMIN_SITE_TITLE', 'پنل مدیریت'),
            'admin_index_title': getattr(settings, 'ADMIN_INDEX_TITLE', 'پنل مدیریت'),
        })
    
    return context

from django.conf import settings
from .models import Announcement, SocialLink


def global_context(request):
    return {
        'open_announcements': Announcement.objects.filter(
            is_active=True, status='open'
        )[:5],
        'social_links': SocialLink.objects.filter(is_active=True),
        'SITE_URL': settings.SITE_URL,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
    }

from .models import Announcement, SocialLink


def global_context(request):
    return {
        'open_announcements': Announcement.objects.filter(
            is_active=True, status='open'
        )[:5],
        'social_links': SocialLink.objects.filter(is_active=True),
    }

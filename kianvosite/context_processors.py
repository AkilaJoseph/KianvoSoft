from .models import Announcement


def global_context(request):
    return {
        'open_announcements': Announcement.objects.filter(
            is_active=True, status='open'
        )[:5],
    }

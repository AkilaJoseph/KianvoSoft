import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_notification(
    subject,
    body_text,
    to_emails,
    from_email=None,
    html_body=None,
):
    from django.conf import settings

    if not to_emails:
        return False

    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject=subject,
            message=html_body if html_body else body_text,
            from_email=from_email,
            recipient_list=[to_emails] if isinstance(to_emails, str) else to_emails,
            html_message=html_body,
            fail_silently=False,
        )
        return True
    except Exception as e:
        logger.error(f'Failed to send email "{subject}": {e}')
        return False


def send_contact_notification(inquiry):
    subject = f'[KianvoSoft Contact] {inquiry.subject or "New Inquiry"} - {inquiry.name}'
    body = f"""
New contact inquiry from {inquiry.name}

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone or 'N/A'}
Service: {inquiry.get_service_type_display() if inquiry.service_type else 'N/A'}
Subject: {inquiry.subject or 'N/A'}

Message:
{inquiry.message}
    """.strip()
    return send_notification(subject, body, 'support@kianvosoft.com')


def send_application_notification(application):
    announcement = application.announcement
    subject = f'[KianvoSoft Application] {application.full_name} - {announcement.title}'
    extra_lines = ''
    if application.extra_data:
        for key, value in application.extra_data.items():
            extra_lines += f'{key.replace("_", " ").title()}: {value}\n'

    body = f"""
New application received

Programme: {announcement.title}
Applicant: {application.full_name}
Email: {application.email}
Phone: {application.phone}

Motivation:
{application.motivation}

{extra_lines}
Submitted: {application.applied_at.strftime('%Y-%m-%d %H:%M')}
    """.strip()
    return send_notification(subject, body, 'info@kianvosoft.com')


def send_new_blog_notification(post):
    subject = f'[KianvoSoft Blog] New Post: {post.title}'
    body = f"""
A new blog post has been published

Title: {post.title}
Category: {post.category.name if post.category else 'Uncategorized'}
Author: {post.author or 'KianvoSoft'}
Published: {post.published_date.strftime('%Y-%m-%d %H:%M') if post.published_date else 'N/A'}

Excerpt:
{post.excerpt or 'No excerpt provided'}

View in portal: http://localhost:8000/portal/blogposts/
    """.strip()
    return send_notification(subject, body, 'info@kianvosoft.com')


def send_new_announcement_notification(announcement):
    subject = f'[KianvoSoft Announcement] {announcement.title}'
    body = f"""
A new announcement has been created

Title: {announcement.title}
Type: {announcement.get_announcement_type_display() if announcement.announcement_type else 'N/A'}
Status: {announcement.get_status_display() if announcement.status else 'N/A'}
Deadline: {announcement.application_deadline.strftime('%Y-%m-%d') if hasattr(announcement, 'application_deadline') and announcement.application_deadline else 'N/A'}

Description:
{announcement.description[:500] if announcement.description else 'N/A'}

View in portal: http://localhost:8000/portal/announcements/
    """.strip()
    return send_notification(subject, body, 'info@kianvosoft.com')

from django.core.management.base import BaseCommand
from django.conf import settings
import os

CONFIG_TEMPLATE = """
# ============================
# Email Configuration (SMTP)
# ============================
# Copy these lines into your environment or .env file.
# Uncomment and fill in your SMTP credentials.

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.kianvosoft.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=support@kianvosoft.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=KianvoSoft <support@kianvosoft.com>
"""


class Command(BaseCommand):
    help = 'Configure and test email sending for KianvoSoft'

    def add_arguments(self, parser):
        parser.add_argument('--test', action='store_true', help='Send a test email to confirm SMTP works')
        parser.add_argument('--to', type=str, help='Email address to send the test to')

    def handle(self, *args, **options):
        backend = settings.EMAIL_BACKEND

        self.stdout.write('=' * 60)
        self.stdout.write('KianvoSoft — Email Configuration')
        self.stdout.write('=' * 60)

        self.stdout.write(f'\nCurrent email backend: {backend}')

        if 'console' in backend:
            self.stdout.write(self.style.WARNING(
                '\n[!] Emails are currently being printed to the console (development mode).\n'
                '   Real emails will NOT be sent until SMTP is configured.'
            ))
            self.stdout.write('\nTo configure real email sending:')
            self.stdout.write(CONFIG_TEMPLATE)
            self.stdout.write('\nOn Windows (PowerShell), set environment variables:')
            self.stdout.write('   $env:EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"')
            self.stdout.write('   $env:EMAIL_HOST = "mail.kianvosoft.com"')
            self.stdout.write('   $env:EMAIL_PORT = "465"')
            self.stdout.write('   $env:EMAIL_USE_SSL = "True"')
            self.stdout.write('   $env:EMAIL_HOST_USER = "support@kianvosoft.com"')
            self.stdout.write('   $env:EMAIL_HOST_PASSWORD = "your-email-password"')
            self.stdout.write('   $env:DEFAULT_FROM_EMAIL = "KianvoSoft <support@kianvosoft.com>"')
        else:
            host = settings.EMAIL_HOST
            user = settings.EMAIL_HOST_USER
            self.stdout.write(f'SMTP Host: {host}')
            self.stdout.write(f'SMTP User: {user}')
            self.stdout.write(self.style.SUCCESS('\n[OK] SMTP is configured.'))

        if options.get('test'):
            to = options.get('to') or 'support@kianvosoft.com'
            self.stdout.write(f'\nSending test email to {to}...')
            try:
                from django.core.mail import send_mail
                send_mail(
                    subject='[KianvoSoft] Test Email from Setup',
                    message=(
                        'This is a test email sent from the KianvoSoft email setup command.\n\n'
                        'If you received this, SMTP is working correctly!\n\n'
                        'Notifications configured:\n'
                        '  - Contact inquiries -> info@kianvosoft.com\n'
                        '  - Announcement applications -> info@kianvosoft.com\n'
                        '  - New blog posts -> info@kianvosoft.com\n'
                        '  - New announcements -> info@kianvosoft.com'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[to],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'[OK] Test email sent to {to}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[FAIL] {e}'))
            
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('Email destinations:')
        self.stdout.write('   Contact inquiries  -> info@kianvosoft.com')
        self.stdout.write('   Announcement applications -> info@kianvosoft.com')
        self.stdout.write('   Blog posts         -> info@kianvosoft.com')
        self.stdout.write('   New announcements  -> info@kianvosoft.com')
        self.stdout.write('=' * 60)

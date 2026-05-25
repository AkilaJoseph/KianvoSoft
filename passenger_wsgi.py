import os
import sys

# -------------------------------------------------------------------
# cPanel Passenger entry point for KianvoSoft Django application
#
# HOW TO SET UP ON CPANEL:
#   1. In cPanel → "Setup Python App":
#      - Application root : /home/<username>/kianvosoft
#      - Application URL  : kianvosoft.com (or your domain)
#      - Python version   : 3.10 (or highest available)
#      - Startup file     : passenger_wsgi.py
#      - Entry point      : application
#   2. Upload all project files to the application root.
#   3. Open the Python App terminal in cPanel and run:
#        pip install -r requirements.txt
#        python manage.py migrate
#        python manage.py collectstatic --noinput
#   4. Restart the app from cPanel.
# -------------------------------------------------------------------

# Point to the correct Python interpreter inside the cPanel virtualenv.
# Replace <username> with your actual cPanel username.
INTERP = os.path.expanduser("~/virtualenv/kianvosoft/3.10/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Tell Django which settings module to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kianvosoft.settings')

# Set production flag so settings.py can switch DEBUG off
os.environ.setdefault('DJANGO_ENV', 'production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

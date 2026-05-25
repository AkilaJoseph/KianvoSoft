import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Tell Django which settings module to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kianvosoft.settings')

# Enable production mode (DEBUG=False, security headers, etc.)
os.environ.setdefault('DJANGO_ENV', 'production')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

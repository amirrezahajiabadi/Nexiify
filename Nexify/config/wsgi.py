"""
WSGI config برای Nexify.

در تولید: گونی‌کورن با config.wsgi اجرا می‌شود و DJANGO_SETTINGS_MODULE
از محیط می‌آید؛ پیش‌فرض production است (در .env یا compose تنظیم می‌شود).
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

application = get_wsgi_application()

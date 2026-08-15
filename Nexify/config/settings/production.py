"""
تنظیمات تولید — سخت‌گیرانه. همه‌ی رازها فقط از متغیرهای محیطی.

نکته: اجرای `python manage.py check --deploy` قبل از go-live الزامی است.
"""
import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403


def env(name: str, default: str | None = None) -> str:
    """متغیر محیطی — اگر موجود نبود، خطای واضح بده (مگر پیش‌فرض داده شده باشد)."""
    value = os.environ.get(name)
    if value is None:
        if default is not None:
            return default
        raise ImproperlyConfigured(f"متغیر محیطی {name} تنظیم نشده است (.env را ببینید)")
    return value


DEBUG = False

SECRET_KEY = env("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = [h.strip() for h in env("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

# ---------------------------------------------------------------------------
# HTTPS
# ---------------------------------------------------------------------------
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS] + [
    o.strip() for o in env("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# ---------------------------------------------------------------------------
# دیتابیس — PostgreSQL (مطابق docker-compose در فاز ۵)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", "nexify"),
        "USER": env("POSTGRES_USER", "nexify"),
        "PASSWORD": env("POSTGRES_PASSWORD", ""),
        "HOST": env("POSTGRES_HOST", "db"),
        "PORT": env("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

# ---------------------------------------------------------------------------
# ایمیل — SMTP (پیش‌فرض: console برای اطمینان از عدم شکست ارسال)
# ---------------------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", "")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", "noreply@example.com")
CONTACT_NOTIFY_EMAIL = env("CONTACT_NOTIFY_EMAIL", "amirrezahajiabadi480@gmail.com")

# ---------------------------------------------------------------------------
# اعلان تلگرام — اختیاری؛ خالی = غیرفعال
# ---------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = env("TELEGRAM_CHAT_ID", "")

# ---------------------------------------------------------------------------
# لاگینگ
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

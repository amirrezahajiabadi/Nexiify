"""
تنظیمات محیط توسعه — فقط برای استفاده‌ی محلی.
"""
import os

from .base import *  # noqa: F401,F403

DEBUG = True

# کلید امضای توسعه — فقط محلی؛ در تولید از .env می‌آید
SECRET_KEY = "django-insecure-dev-only-never-use-in-production-nexify"

# دامنه‌های مجاز در توسعه — شامل تانل‌های عمومی (ngrok/pinggy) برای نمایش سایت
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".ngrok-free.app", ".ngrok-free.dev", ".pinggy.io", ".pinggy-free.link", ".free.pinggy.net"]

# منشأهای مجاز CSRF برای ارسال فرم‌ها از دامنه‌های تانل (https)
CSRF_TRUSTED_ORIGINS = ["https://*.ngrok-free.app", "https://*.ngrok-free.dev", "https://*.pinggy.io", "https://*.pinggy-free.link", "https://*.free.pinggy.net"]

# اعلان تلگرام — توکن بات و آیدی چت را اینجا بگذار (یا در env؛ خالی/placeholder = غیرفعال)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PASTE_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "PASTE_CHAT_ID_HERE")

# تابع زمان‌بندی cache برای توسعه (بدون redis)
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# نشان دادن خطاهای template در توسعه
TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

# در توسعه از storage با cache-busting خودکار (?v=<mtime>) استفاده می‌کنیم —
# بعد از تغییر هر فایل استاتیک، URL آن عوض می‌شود و مرورگر نسخه‌ی تازه را می‌گیرد (بدون Ctrl+F5).
# در production.py این مقدار با STORAGES پایه = whitenoise (manifest+compress) است که خودش هش فایل دارد.
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "config.storage.MtimeStaticFilesStorage",
    },
}

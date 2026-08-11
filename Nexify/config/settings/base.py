"""
تنظیمات مشترک جنگو — بین همه‌ی محیط‌ها (توسعه/تولید) یکسان است.
"""
import os
from pathlib import Path

# مسیر ریشه‌ی پروژه: Nexify/config/settings/base.py → ۳ پوشه بالا = Nexify/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ---------------------------------------------------------------------------
# امنیت پایه (در production.py سخت‌گیرانه‌تر می‌شود)
# ---------------------------------------------------------------------------
SECRET_KEY = "REPLACED_BY_ENVIRONMENT_IN_PRODUCTION"
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok-free.app', '.ngrok-free.dev', '.pinggy.io', '.pinggy-free.link', '.free.pinggy.net']

# ---------------------------------------------------------------------------
# اپلیکیشن‌ها
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # اپ‌های پروژه
    "apps.core",
    "apps.projects",
    "apps.blog",
    "apps.contact",
    "apps.accounts",
    "apps.panel",
]

# ---------------------------------------------------------------------------
# میدل‌ورها — WhiteNoise بلافاصله بعد از SecurityMiddleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "config.middleware.AdminSecurityHeadersMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.VisitTrackingMiddleware",  # آمار بازدید — بعد از SessionMiddleware (نیاز به session)
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.panel.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------------------
# دیتابیس — پیش‌فرض SQLite (در production.py به PostgreSQL تغییر می‌کند)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------------------------
# احراز هویت
# ---------------------------------------------------------------------------
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# ---------------------------------------------------------------------------
# اعتبارسنجی رمز عبور
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# زبان و زمان
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "fa-ir"
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# فایل‌های استاتیک
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# فایل‌های آپلودی (تصاویر شاخص مقالات/پروژه‌ها)
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# سرو استاتیک با WhiteNoise (در توسعه و تولید) + هش فایل در production
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------------------------------------------------------------------------
# ایمیل — پیش‌فرض توسعه: console (در production.py با SMTP جایگزین می‌شود)
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@nexify.ir"
CONTACT_NOTIFY_EMAIL = "amirrezahajiabadi480@gmail.com"

# ---------------------------------------------------------------------------
# اعلان تلگرام — اختیاری؛ خالی = غیرفعال (ارسال fail-silent در apps/core/services.py)
# ---------------------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# ---------------------------------------------------------------------------
# متفرقه
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

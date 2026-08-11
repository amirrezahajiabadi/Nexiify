"""
تنظیمات جنگو به سه ماژول تقسیم شده:

- base.py        : تنظیمات مشترک (همه محیط‌ها)
- development.py : محیط توسعه محلی (پیش‌فرض manage.py)
- production.py  : محیط تولید (توسط DJANGO_SETTINGS_MODULE=config.settings.production)

انتخاب ماژول: `python manage.py runserver` → development (در manage.py)
گونی‌کورن/WSGI در تولید → config.settings.production (در wsgi.py / محیط)
"""

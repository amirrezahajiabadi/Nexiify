# ⚡ Nexify — AI Solutions & Development

وب‌سایت معرفی و نمونه‌کار Nexify؛ **فارسی و راست‌چین (RTL)** با تم تیره/روشن — اکنون با بک‌اند **Django**.

> 📖 فاز ۰ تا ۴ از `ROADMAP.md` انجام شده؛ فاز ۵ (دیپلوی) در پیش است.

---

## 🚀 اجرای پروژه (توسعه محلی)

```bash
cd Nexify

# ۱) نصب وابستگی‌ها (پایتون ۳.۱۲+)
python -m pip install -r requirements.txt

# ۲) آماده‌سازی دیتابیس و داده‌ی نمونه
python manage.py migrate
python manage.py seed_demo          # ۶ پروژه + ۶ مقاله + ۶ سوال متداول
python manage.py createsuperuser    # برای ورود به /admin/

# ۳) اجرای سرور
python manage.py runserver
# → http://127.0.0.1:8000   (ادمین: /admin/)
```

---

## 🧪 تست (pytest)

```bash
cd Nexify
python -m pip install -r requirements-dev.txt   # pytest + pytest-django
pytest -v                                        # ۳۹ تست
```

پوشش تست‌ها:

- **فرم تماس**: اعتبارسنجی فیلدها، رد هانی‌پات در `clean()`، عدم نگاشت `website` به دیتابیس
- **هانی‌پات سمت سرور**: ربات ساکت رد می‌شود (پیام موفقیت می‌بیند ولی **هیچ‌چیز ذخیره نمی‌شود** و ایمیلی ارسال نمی‌شود)
- **ویوهای تماس**: GET (رندر فرم + FAQ منتشرشده + CSRF)، POST معتبر (ذخیره + ایمیل)، POST نامعتبر (خطاهای فیلد)
- **مدل‌ها**: Project / BlogPost / ContactMessage / FAQ (پیش‌فرض‌ها، مرتب‌سازی، استرینگ، slug یکتا)
- **ویوها**: فیلتر `is_published` در پروژه‌ها/مقالات، 404 برای اسلاگ ناموجود یا پیش‌نویس
- **smoke تست**: همه‌ی مسیرهای عمومی ۲۰۰

### CI (GitHub Actions)

فایل `.github/workflows/ci.yml` روی هر push/PR به `main` اجرا می‌شود:
Python 3.12 و 3.13 → نصب وابستگی‌ها → `manage.py check` → `pytest`.

> ℹ️ نکته: `EMAIL_BACKEND` در جنگو ۶ منسوخ اعلام شده (از جنگو ۷ حذف می‌شود).
> برای آینده باید به API جدید `MAILERS` مهاجرت کرد — تا جنگو ۶ مشکلی نیست.

| مسیر | صفحه |
|------|------|
| `/` | خانه |
| `/services/` | خدمات |
| `/projects/` | نمونه کارها (دیتابیس) |
| `/about/` | درباره ما |
| `/blog/` و `/blog/<slug>/` | مقالات + جزئیات (دیتابیس) |
| `/contact/` | تماس (فرم امن) |
| `/admin/` | پنل مدیریت جنگو |

---

## 📂 ساختار پروژه

```
Nexify/
├── manage.py
├── requirements.txt        # توسعه‌ی محلی
├── requirements-dev.txt    # + pytest, pytest-django (تست)
├── requirements-prod.txt   # + gunicorn, psycopg (تولید)
├── pytest.ini              # پیکربندی pytest (DJANGO_SETTINGS_MODULE)
├── .github/workflows/ci.yml # CI: pytest روی Python 3.12/3.13
├── .env.example            # الگوی متغیرهای محیطی تولید
├── config/                 # پیکربندی اصلی جنگو
│   ├── settings/
│   │   ├── base.py         # تنظیمات مشترک (Whitenoise، استاتیک، تمپلیت)
│   │   ├── development.py  # توسعه (SQLite، DEBUG=True)
│   │   └── production.py   # تولید (PostgreSQL، HTTPS، env)
│   ├── urls.py  wsgi.py  asgi.py
├── apps/
│   ├── core/               # خانه، درباره، خدمات + دستور seed_demo
│   ├── projects/           # مدل Project
│   ├── blog/               # مدل BlogPost
│   └── contact/            # مدل‌های ContactMessage + FAQ و فرم امن
├── templates/
│   ├── base.html           # قالب پایه (بلاک‌ها + preload فونت + CSP)
│   ├── partials/           # navbar, footer, preloader, mobile_menu
│   ├── index.html  about.html  services.html  projects.html  contact.html
│   └── blog/               # blog_list.html + blog_detail.html
├── static/
│   ├── css/  js/  fonts/   # فونت‌های self-host (فاز ۳)
├── legacy/                 # بایگانی HTML های استاتیک قبل از جنگو
├── _headers                # هدرهای امنیتی (Netlify/Cloudflare Pages)
├── nginx-security.conf     # هدرهای امنیتی (VPS)
└── ROADMAP.md
```

---

## 🔒 امنیت (فاز ۲ + ۴)

- **CSRF** روی فرم تماس + **هانی‌پات دو لایه** (`website`) — سمت کلاینت و **سمت سرور** (پیام ربات ساکت رد می‌شود و در دیتابیس ذخیره نمی‌شود)
- **اعتبارسنجی سمت سرور** (`minlength` نام/پیام، فرمت ایمیل، انتخاب نوع درخواست) + خطاهای فیلد در قالب
- **CSP** در `base.html` + هدرهای امنیتی برای دیپلوی (`_headers` / `nginx-security.conf`)
- مودال پروژه‌ها بدون `innerHTML` (ساخت DOM امن) — ضد XSS حتی با داده‌ی داینامیک
- در تولید: `SECURE_SSL_REDIRECT`، HSTS، کوکی‌های امن و `check --deploy`

---

## 🧭 وضعیت فازها (ROADMAP)

- ✅ **فاز ۱** — ساختاردهی: `css/`، `js/`، حذف `assets/` مرده، جداسازی استایل/اسکریپت، حذف onclick
- ✅ **فاز ۲** — امنیت: مودال بدون innerHTML، هانی‌پات، CSP + هدرهای امنیتی
- ✅ **فاز ۳** — سرعت: فونت self-host، `font-display: swap`، preload، defer
- ✅ **فاز ۴** — **جنگو**: settings سه‌تایی، ۴ اپ، `base.html` + partials، مدل‌ها (Project/BlogPost/ContactMessage/FAQ)، فرم امن با CSRF و هانی‌پات سمت سرور
- ⏳ **فاز ۵** — دیپلوی: Docker Compose، Gunicorn، Nginx، PostgreSQL، CI/CD (جزئیات در ROADMAP)

---

## 🧪 نکات

- فرم تماس در توسعه پیام را در `db.sqlite3` ذخیره می‌کند (در تولید: PostgreSQL + ایمیل SMTP)
- فونت‌ها self-host هستند (Vazirmatn + JetBrains Mono، همه‌ی وزن‌ها در یک فایل woff2)
- صفحات `index/about/services` فعلاً محتوای استاتیک دارند؛ مدل‌های داینامیک (Service, Skill, ...) در فاز بعدی

© ۱۴۰۳ Nexify. تمام حقوق محفوظ است.

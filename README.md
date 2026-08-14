# ⚡ Nexify — AI Solutions & Development

وب‌سایت معرفی و نمونه‌کار Nexify؛ **فارسی و راست‌چین (RTL)** با تم تیره/روشن — اکنون با بک‌اند **Django**.

> 📖 فازهای ۰ تا ۴.x از `ROADMAP.md` انجام شده؛ فاز ۵ (دیپلوی) در پیش است. وضعیت زنده و جزئیات فنی در `AI-CONTEXT.md`.

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
python manage.py runserver 127.0.0.1:8471
# → http://127.0.0.1:8471   (ادمین: /admin/)
```

---

## 🧪 تست (pytest)

```bash
cd Nexify
python -m pip install -r requirements-dev.txt   # pytest + pytest-django
pytest -v                                        # ۱۱۵ تست
```

پوشش تست‌ها:

- **فرم تماس**: اعتبارسنجی فیلدها، رد هانی‌پات در `clean()`، عدم نگاشت `website` به دیتابیس
- **هانی‌پات سمت سرور**: ربات ساکت رد می‌شود (پیام موفقیت می‌بیند ولی **هیچ‌چیز ذخیره نمی‌شود** و ایمیلی ارسال نمی‌شود)
- **ویوهای تماس**: GET (رندر فرم + FAQ منتشرشده + CSRF)، POST معتبر (ذخیره + ایمیل)، POST نامعتبر (خطاهای فیلد)
- **مدل‌ها**: Project / BlogPost / ContactMessage / FAQ (پیش‌فرض‌ها، مرتب‌سازی، استرینگ، slug یکتا)
- **ویوها**: فیلتر `is_published` در پروژه‌ها/مقالات، 404 برای اسلاگ ناموجود یا پیش‌نویس
- **smoke تست**: همه‌ی مسیرهای عمومی ۲۰۰
- **پنل ادمین + احراز هویت**: انتشار/حذف محتوا، مدیریت پیام‌ها، آمار بازدید، هانی‌پات دولایه‌ی ثبت‌نام، بلاک ریدایرکت خارجی
- **پروفایل کاربر**: اتصال سفارش‌های تماس و دیدگاه‌ها به کاربر لاگین‌شده + آمار پنل فقط برای staff
- **کامنت بلاگ**: ثبت با CSRF، فقط کاربر لاگین‌شده، فیلتر `is_visible` برای مدیریت
- **آمار خانه**: شمارنده‌های واقعی از دیتابیس (پروژه/مشتری/رضایت/مقاله) + ترتیب سکشن‌ها

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
| `/accounts/login/` `/register/` `/logout/` | ورود / ثبت‌نام / خروج |
| `/admin/` | پنل مدیریت جنگو |
| `/panel/` | پنل ادمین سفارشی (داشبورد + آمار بازدید) — فقط staff |

---

## 📂 ساختار پروژه

```
├── README.md                 # همین فایل — راهنمای پروژه
├── ROADMAP.md                # نقشه‌ی راه کلی (فاز ۰ تا ۵)
├── UIUX-ROADMAP.md           # نقشه‌ی بازطراحی UI/UX (فازهای U1–U8)
├── RESPONSIVE-ROADMAP.md     # نقشه‌ی ریسپانسیو موبایل
├── AI-CONTEXT.md             # فایل کانتکست برای AI (ساختار + جزئیات فنی زنده)
└── Nexify/                   # ⭐ خود پروژه‌ی جنگو
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
    │   ├── core/               # خانه، درباره، خدمات + آیکون‌های SVG + دستور seed_demo
    │   ├── projects/           # مدل Project
    │   ├── blog/               # مدل BlogPost + Comment
    │   ├── contact/            # مدل‌های ContactMessage + FAQ و فرم امن
    │   ├── accounts/           # ورود/ثبت‌نام/خروج + پروفایل (هانی‌پات دولایه)
    │   └── panel/              # پنل ادمین سفارشی (داشبورد، مقاله/پروژه/FAQ/پیام/نظر/تنظیمات/کاربران)
    ├── templates/
    │   ├── base.html           # قالب پایه (بلاک‌ها + preload فونت + CSP)
    │   ├── partials/           # navbar, footer, preloader, mobile_menu, auth_*
    │   ├── index.html  about.html  services.html  projects.html  contact.html
    │   ├── blog/               # blog_list.html + blog_detail.html
    │   ├── accounts/           # login.html + register.html + profile.html
    │   └── panel/              # داشبورد + فرم‌ها/لیست‌های مدیریت
    ├── static/
    │   ├── css/  js/  fonts/   # فونت‌های self-host (فاز ۳)
    ├── scripts/security_scan.py # اسکن امنیتی مسیرها/هدرها روی سرور توسعه
    ├── _headers                # هدرهای امنیتی (Netlify/Cloudflare Pages)
    ├── nginx-security.conf     # هدرهای امنیتی (VPS)
    └── start_tunnel.sh         # تانل عمومی pinggy برای نمایش به دیگران
```

---

## 🔒 امنیت (فاز ۲ + ۴)

- **CSRF** روی فرم تماس + **هانی‌پات دو لایه** (`website`) — سمت کلاینت و **سمت سرور** (پیام ربات ساکت رد می‌شود و در دیتابیس ذخیره نمی‌شود)
- **اعتبارسنجی سمت سرور** (`minlength` نام/پیام، فرمت ایمیل، انتخاب نوع درخواست) + خطاهای فیلد در قالب
- **CSP** در `base.html` + هدرهای امنیتی برای دیپلوی (`_headers` / `nginx-security.conf`)

---

## 🚫 فایل‌هایی که هرگز در گیت‌هاب قرار نده

| فایل/پوشه | چرا | وضعیت در مخزن |
|---|---|---|
| `Nexify/db.sqlite3` | دیتابیس توسعه — داده‌ی کاربران و هش رمزها | ignored (`Nexify/.gitignore`) |
| `Nexify/.env` | رازها (SECRET_KEY، رمز SMTP/DB، توکن تلگرام) | ignored — فقط `.env.example` کامیت می‌شود |
| `Nexify/media/` | فایل‌های آپلودی کاربران | ignored |
| `Nexify/staticfiles/` | خروجی `collectstatic` (بازسازی‌شدنی) | ignored |
| `.freebuff/` | لاگ‌ها/دیتابیس ابزار محلی | ignored (root) |
| `.agents/` `.claude/` `skills-lock.json` | ابزارهای محلی agent — به سایت ربطی ندارند | ignored (root) |
- مودال پروژه‌ها بدون `innerHTML` (ساخت DOM امن) — ضد XSS حتی با داده‌ی داینامیک
- در تولید: `SECURE_SSL_REDIRECT`، HSTS، کوکی‌های امن و `check --deploy`

---

## 🧭 وضعیت فازها (ROADMAP)

- ✅ **فاز ۱** — ساختاردهی: `css/`، `js/`، حذف `assets/` مرده، جداسازی استایل/اسکریپت، حذف onclick
- ✅ **فاز ۲** — امنیت: مودال بدون innerHTML، هانی‌پات، CSP + هدرهای امنیتی
- ✅ **فاز ۳** — سرعت: فونت self-host، `font-display: swap`، preload، defer
- ✅ **فاز ۴** — **جنگو**: settings سه‌تایی، ۴ اپ، `base.html` + partials، مدل‌ها (Project/BlogPost/ContactMessage/FAQ)، فرم امن با CSRF و هانی‌پات سمت سرور
- ✅ **فاز ۴.۵** — تست + CI: ۹۴ تست pytest + workflow گیت‌هاب (Python 3.12/3.13)
- ✅ **فاز ۴.۶** — احراز هویت: ورود/ثبت‌نام با انیمیشن + خروج POST-only + هانی‌پات دولایه
- ✅ **فاز ۴.۷** — ریسپانسیو: R1–R6 (جزئیات در `RESPONSIVE-ROADMAP.md`)
- ✅ **فاز ۴.۸** — پنل ادمین سفارشی (`apps/panel`): انتشار مقاله/پروژه، مدیریت سفارش‌ها، ویرایش متن‌های سایت، چند ادمین، آمار بازدید
- ✅ **فاز ۴.۹** — ممیزی UI/UX با اسکیل `ui-ux-pro-max` → `UIUX-ROADMAP.md`
- 🟡 **فاز ۴.۱۰** — بهبود UI/UX: U1 (کنتراست AA + فرم‌ها) و U2 (آیکون‌های SVG) انجام شد — بعدی U3 (مودال + کیبورد)
- ⏳ **فاز ۵** — دیپلوی: Docker Compose، Gunicorn، Nginx، PostgreSQL، CI/CD (جزئیات در ROADMAP)

---

## 🧪 نکات

- فرم تماس در توسعه پیام را در `db.sqlite3` ذخیره می‌کند (در تولید: PostgreSQL + ایمیل SMTP)
- فونت‌ها self-host هستند (Vazirmatn + JetBrains Mono، همه‌ی وزن‌ها در یک فایل woff2)
- پروژه‌ها و مقالات از دیتابیس می‌آیند؛ محتوای `index/about/services` فعلاً از خود قالب است (مدل‌های `Service`/`Skill` در فاز بعدی)

© ۱۴۰۳ Nexify. تمام حقوق محفوظ است.

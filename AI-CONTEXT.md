# 🧠 Nexify — فایل مرجع کامل پروژه (برای هر AI)

> این فایل «سند ورود سریع» پروژه است. اگر می‌خواهید با یک AI دیگر روی این پروژه کار کنید، **فقط همین فایل را به آن بدهید** — این سند کل ساختار، پشته‌ی فناوری، قراردادها، وضعیت کارهای انجام‌شده و کارهای باقی‌مانده را توضیح می‌دهد.
>
> ⚠️ **قانون نگهداری**: این فایل باید **همگام با هر تغییر در پروژه** به‌روز شود. هر زمان که فایلی را اضافه/حذف/تغییر می‌دهید یا رفتاری را عوض می‌کنید، بخش‌های مرتبط این سند (ساختار، تنظیمات، URL ها، مدل‌ها، دستورات، وضعیت فازها) را هم به‌روز کنید و تاریخ را در همین خط بزنید. اگر این فایل با کد ناسازگار باشد، برای AI بعدی بی‌فایده و گمراه‌کننده است.
>
> آخرین به‌روزرسانی: ۷ اوت ۲۰۲۶ — وضعیت: **فازهای ۱ تا ۴ و ۴.۵ (تست/CI) و ۴.۶ (احراز هویت) کامل + روش تماس تلگرام در فرم + آماده‌سازی اشتراک‌گذاری ngrok + اعلان تلگرام (فرم/ثبت‌نام)**، فاز ۵ (دیپلوی) باقی‌مانده. (۷۳ تست)

---

## ۱) معرفی کلی پروژه

**Nexify** یک وب‌سایت شخصی/نمونه‌کار (Portfolio) فارسی و راست‌چین برای ارائه‌ی خدمات «راهکارهای هوش مصنوعی» است. **تمرکز اصلی: ساخت Agent های هوش مصنوعی** و **پکیج‌های آماده اتوماسیون (n8n)** — استقرار مدل‌ها «به‌زودی»؛ طراحی وب/اپلیکیشن فقط به‌عنوان اسکیل مکمل در پروژه‌های Agent/اتوماسیون.

- پروژه از یک **وب‌سایت استاتیک** شروع شد و در **فاز ۴ به جنگو (Django)** مهاجرت کرده است.
- کل پروژه در پوشه‌ی `Nexify/` قرار دارد (پروژه‌ی جنگو درون همین پوشه است — یعنی `manage.py` در `Nexify/manage.py` است).
- **اسناد و رودمپ‌ها در ریشه‌ی مخزن (بالای `Nexify/`) قرار دارند**: `README.md`، `ROADMAP.md`، `UIUX-ROADMAP.md`، `RESPONSIVE-ROADMAP.md` و همین `AI-CONTEXT.md`.
- تم تیره (Dark) پیش‌فرض + تم روشن قابل سوییچ، کاملاً فارسی و RTL.
- دیتای محتوا (پروژه‌ها، مقالات، FAQ ها، پیام‌های تماس) **در دیتابیس** ذخیره می‌شود و از **Django Admin** مدیریت می‌شود.

---

## ۲) پشته‌ی فناوری (Tech Stack)

| لایه | فناوری | نسخه | توضیح |
|------|--------|------|-------|
| بک‌اند | **Django** | 6.1 | رندر سمت سرور (Server-Side Rendering) |
| زبان بک‌اند | **Python** | 3.14 | — |
| دیتابیس توسعه | **SQLite** | — | `db.sqlite3` در ریشه |
| دیتابیس تولید | **PostgreSQL** | — | از طریق متغیرهای محیطی در `production.py` |
| استاتیک در تولید | **WhiteNoise** | ≥6.8 | سرو فایل‌های استاتیک بدون Nginx جداگانه |
| فرانت‌اند | **HTML5 + CSS3 + Vanilla JS** | — | بدون فریم‌ورک، بدون بیلد استپ |
| فونت | **Vazirmatn Variable** + **JetBrains Mono Variable** | — | self-host شده در `static/fonts/` (woff2 متغیر) |
| اسکرول نرم | **Lenis** (کتابخانه‌ی اسکریپت چرخه) | 1.0.42 | از CDN (jsDelivr) لود می‌شود |
| ایمیل توسعه | console backend | — | ایمیل‌ها در خروجی ترمینال نمایش داده می‌شوند |

**وابستگی‌های Python** (فایل `requirements.txt`):
```
Django>=6.0,<7.0
whitenoise>=6.8
```

> ⚠️ **هیچ ابزار بیلد/باندلر (npm, webpack, esbuild) وجود ندارد** — CSS و JS ها دستی و خام هستند. هیچ `package.json` ای نداریم.

---

## ۳) ساختار کامل پوشه‌ها

```
Nexify/
├── config/storage.py                 # ⭐ ذخیره‌ساز استاتیک توسعه: cache-busting خودکار (?v=<mtime>)
├── manage.py                        # نقطه‌ی ورود جنگو (پیش‌فرض: settings توسعه)
├── start_tunnel.sh                  # ⭐ اسکریپت تانل عمومی: سرور + pinggy را بالا می‌آورد و URL را نشان می‌دهد (بستن: taskkill //F //PID $(cat ../.freebuff/pinggy.pid))
├── requirements.txt                 # وابستگی‌های توسعه (محلی) — شامل Pillow (تصاویر شاخص)
├── requirements-dev.txt             # + pytest و pytest-django (تست)
├── requirements-prod.txt            # (فایل تولید — محتوای مشابه + اختیاری psycopg)
├── pytest.ini                       # پیکربندی pytest (DJANGO_SETTINGS_MODULE=development)
├── .github/                         # ⭐ در ریشه‌ی مخزن (بالای Nexify/)
│   ├── workflows/ci.yml             # ⭐ CI — روی push/PR به main: check + makemigrations --check + pytest (Python 3.12/3.13)
│   ├── ISSUE_TEMPLATE/              # قالب‌های گزارش باگ + پیشنهاد ویژگی
│   └── PULL_REQUEST_TEMPLATE.md     # قالب PR (چک‌لیست تست)
├── .env.example                     # الگوی متغیرهای محیطی تولید
├── .gitignore                       # .env، staticfiles/، db.sqlite3، __pycache__ و...
├── README.md                        # ⭐ معرفی به‌عنوان نمونه‌کار (گالری اسکرین‌شات + امکانات — مخزن عمومی است؛ هدف نمایش است نه کولب/مشارکت)
├── LICENSE                          # ⭐ تمام حقوق محفوظ (All rights reserved — نه MIT؛ چون نمونه‌کار است)
├── ROADMAP.md                       # نقشه‌ی راه فازها (۱→۵)
├── RESPONSIVE-ROADMAP.md            # ⭐ نقشه‌ی راه ریسپانسیو (بریک‌پوینت‌های یکپارچه، فازهای R1→R6، چک‌لیست تست موبایل)
├── UIUX-ROADMAP.md                  # ⭐ نقشه‌ی راه بهبود UI/UX (ممیزی با اسکیل ui-ux-pro-max — فازهای U1→U8: کنتراست، آیکون‌ها، مودال، فوتر، Social Proof، صنایع، پرفورمنس)
├── AI-CONTEXT.md                    # ← همین فایل
├── _headers                         # هدرهای امنیتی (فرمت Netlify/Cloudflare Pages)
├── nginx-security.conf              # هدرهای امنیتی برای Nginx (VPS — بلوک /admin/ مخصوص جنگو)
├── scripts/security_scan.py         # ⭐ اسکن امنیتی خودکار (فقط stdlib، بدون وابستگی)
│   └── ...                          # پروب‌های واقعی: هدرها، کوکی‌ها، CSRF، SQLi، XSS، path traversal، OPTIONS/TRACE، فایل‌های حساس
│
├── config/                          # ⭐ پیکربندی اصلی جنگو
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py              # (پکیج settings)
│   │   ├── base.py                  # تنظیمات مشترک همه‌ی محیط‌ها
│   │   ├── development.py           # DEBUG=True، SQLite، ALLOWED_HOSTS=['localhost','127.0.0.1','.ngrok-free.app','.ngrok-free.dev','.pinggy.io'] + CSRF_TRUSTED_ORIGINS تانل‌ها
│   │   └── production.py            # DEBUG=False، PostgreSQL، HTTPS سخت‌گیرانه
│   ├── urls.py                      # مسیرهای اصلی (include اپ‌ها)
│   ├── middleware.py                # ⭐ AdminSecurityHeadersMiddleware — هدر CSP برای /admin/ (ادمین جنگو base.html ندارد)
│   ├── wsgi.py                      # WSGI (برای Gunicorn در تولید)
│   └── asgi.py                      # ASGI
│
├── apps/                            # ⭐ اپلیکیشن‌ها (۶ اپ)
│   │                                # هر اپ یک tests.py دارد — ۸۷ تست pytest (فاز ۵-آماده)
│   ├── __init__.py
│   ├── core/                        # صفحه‌ی اصلی، درباره، خدمات + دستور seed_demo
│   │   ├── icons.py                 # ⭐ منبع واحد آیکون‌های SVG (فاز U2): نگاشت ایموجی/کلید → SVG stroke-based (viewBox 24، currentColor) + ستاره (U5) + صنایع (U6: 🛒🏦🏥🚚🎓🏭)
│   │   └── templatetags/core_extras.py  # فیلتر icon_svg — {{ "📞"|icon_svg }} (mark_safe؛ برای آیکون دیتابیس: {{ post.icon|icon_svg }}) + stars (U5: {{ t.rating|stars }} → ردیف ستاره SVG) + fa_num (ارقام فارسی)
│   │   ├── models.py                # (فعلاً خالی — فقط منبع دستور seed)
│   │   ├── views.py                 # index، about، services
│   │   ├── urls.py                  # app_name = "core"
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   └── management/commands/seed_demo.py   # ساخت داده‌ی نمونه
│   ├── projects/                    # نمونه‌کارها
│   │   ├── models.py                # مدل Project
│   │   ├── views.py                 # project_list
│   │   ├── urls.py                  # app_name = "projects"
│   │   ├── admin.py                 # (با نمایش سفارشی)
│   │   ├── apps.py  ─  tests.py
│   ├── blog/                        # مقالات
│   │   ├── models.py                # مدل BlogPost
│   │   ├── views.py                 # blog_list + blog_detail (با slug + کامنت)
│       └── forms.py                 # CommentForm (فقط body)
│   │   ├── urls.py                  # app_name = "blog"
│   │   ├── admin.py  ─  apps.py  ─  tests.py
│   └── contact/                     # فرم تماس + سوالات متداول
│       ├── models.py                # ContactMessage + FAQ
│       ├── forms.py                 # ContactForm (امن: CSRF + هانی‌پات)
│       ├── views.py                 # contact (GET/POST)
│       ├── urls.py                  # app_name = "contact"
│       ├── admin.py  ─  apps.py  ─  tests.py
│   └── accounts/                    # ⭐ احراز هویت: ورود / ثبت‌نام / خروج + پروفایل کاربر
│       ├── forms.py                 # LoginForm (AuthenticationForm فارسی) + RegisterForm (UserCreationForm + ایمیل + هانی‌پات)
│       ├── views.py                 # NexifyLoginView (LoginView) + register + logout_view (POST-only)
│       ├── urls.py                  # app_name = "accounts" (+ profile)
│       ├── profile.html             # پروفایل: درخواست‌های من + دیدگاه‌های من + (staff) خلاصه پنل + پنل مدیریت
│       ├── apps.py  ─  tests.py
│   └── panel/                       # ⭐ پنل ادمین سفارشی (طراحی شیشه‌ای هماهنگ با سایت) — فقط staff
│       ├── models.py                # SiteSetting (متن‌ها) + Testimonial (نظر مشتری — فاز U5) + PageView
│       ├── forms.py                 # BlogPostForm / ProjectForm / FAQForm / TestimonialForm / SiteSettingForm
│       ├── views.py                 # dashboard + CRUD مقاله/پروژه/نظر مشتری/FAQ/پیام/متن + مدیریت کاربران
│       ├── urls.py                  # app_name = "panel" — همه زیر /panel/
│       ├── context_processors.py    # ⭐ site_settings — متن‌ها را به همه‌ی تمپلیت‌ها می‌دهد ({{ site_settings.hero_title_1 }})
│       ├── templatetags/panel_extras.py  # فیلتر get_item برای دیکشنری‌ها
│       ├── admin.py
│       ├── management/commands/seed_settings.py  # ۱۰ متن پیش‌فرض سایت
│       ├── apps.py  ─  tests.py     # ۱۴ تست (دسترسی، CRUD، چند ادمین، متن‌ها)
│       └── migrations/0001_initial.py
│
├── templates/                       # ⭐ تمپلیت‌های جنگو (جایگزین HTML های قدیمی)
│   ├── base.html                    # قالب اصلی: هدر + preloader + نوبار + فوتر + بلاک‌ها
│   ├── partials/
│   │   ├── navbar.html              # نوبار (همه‌ی صفحات) — وضعیت کاربر شرطی (user.is_authenticated)
│   │   ├── footer.html              # فوتر
│   │   ├── preloader.html           # انیمیشن بارگذاری
│   │   ├── mobile_menu.html         # منوی موبایل — وضعیت کاربر شرطی
│   │   ├── auth_background.html     # پس‌زمینه‌ی متحرک مشترک صفحات ورود/ثبت‌نام (اُرب‌ها + شبکه‌ی نقطه‌چین)
│   │   └── auth_eye_toggle.html     # دکمه‌ی نمایش/پنهان‌کردن رمز (متغیر field_id) — جلوگیری از تکرار SVG
│   ├── accounts/                    # ⭐ صفحات احراز هویت
│   │   ├── login.html               # ورود (کارت شیشه‌ای + اُرب‌های شناور + هاله‌ی موس + eye toggle)
│   │   └── register.html            # ثبت‌نام (+ متر قدرت رمز + هانی‌پات + ?next=)
│   └── panel/                       # ⭐ تمپلیت‌های پنل ادمین (base_panel + ۱۴ صفحه)
│       ├── base_panel.html          # قالب پنل: سایدبار + هدر + جداول/کارت‌های شیشه‌ای RTL
│       ├── dashboard.html           # آمار (مقالات/پروژه/سفارش/کاربران/نظرات) + آخرین سفارش‌ها/مقالات
│       ├── testimonial_list.html  testimonial_form.html   # نظرات مشتریان (فاز U5)
│       ├── blog_list.html  blog_form.html
│       ├── project_list.html  project_form.html
│       ├── message_list.html  message_detail.html  # سفارش‌ها با تغییر وضعیت (new/in_progress/done)
│       ├── faq_list.html  faq_form.html
│       ├── setting_list.html  setting_form.html    # متن‌های قابل ویرایش سایت
│       └── user_list.html          # چند ادمین — فقط مدیر اصلی دسترسی می‌دهد/برمی‌دارد
│   ├── index.html                   # صفحه‌ی اصلی (دیتا: استاتیک در قالب) — شعار hero: «ساخت و توسعه سرویس‌های هوش مصنوعی» (۲ خط، فونت کوچک‌تر از قبل)
│   ├── about.html                   # درباره (دیتا: استاتیک در قالب)
│   ├── services.html                # خدمات (دیتا: استاتیک در قالب)
│   ├── projects.html                # نمونه‌کارها (دیتا: حلقه از مدل Project)
│   ├── contact.html                 # تماس (فرم جنگو + FAQ از DB)
│   └── blog/
│       ├── blog_list.html           # لیست مقالات (حلقه از BlogPost)
│       └── blog_detail.html         # جزئیات مقاله (متغیر post)
│
├── static/                          # ⭐ فایل‌های استاتیک (با {% static %} ارجاع می‌شوند)
│   ├── css/
│   │   ├── style.css                # استایل مشترک همه‌ی صفحات (+ @font-face فونت‌ها)
│   │   ├── index.css  about.css  services.css
│   │   ├── projects.css  blog.css  contact.css  auth.css  panel.css
│   ├── js/
│   │   ├── main.js                  # اسکریپت مشترک (تم، نوبار، اسکرول، کانترها...)
│   │   ├── index.js  about.js  projects.js  blog.js  contact.js  auth.js  panel.js
│   └── fonts/
│       ├── Vazirmatn-Variable.woff2        # فونت فارسی (همه‌ی وزن‌ها، یک فایل)
│       └── JetBrainsMono-Variable.woff2    # فونت مونو (کد/اعداد)
│
├── staticfiles/                     # خروجی collectstatic (تولید) — در .gitignore
├── media/                           # فایل‌های آپلودی (blog_covers/, project_covers/) — در .gitignore
└── db.sqlite3                       # دیتابیس توسعه (در .gitignore)

> 📄 اسناد (README/ROADMAP/UIUX-ROADMAP/RESPONSIVE-ROADMAP/AI-CONTEXT) در **ریشه‌ی مخزن** — بالای `Nexify/`
> 🧹 `legacy/` (HTML های استاتیک قدیمی) حذف شد — نسخه‌ها در تاریخ گیت هستند
```

---

## ۴) تنظیمات جنگو (config/settings/)

### `base.py` — مشترک
- `BASE_DIR` = سه پوشه بالاتر از `config/settings/` → `Nexify/`
- `SECRET_KEY` پیش‌فرض placeholder (در تولید باید از env بیاید)، `DEBUG=False`
- **INSTALLED_APPS**: ۶ اپ داخلی جنگو (admin, auth, contenttypes, sessions, messages, staticfiles) + ۶ اپ پروژه: `apps.core`, `apps.projects`, `apps.blog`, `apps.contact`, `apps.accounts`, `apps.panel`
- **Context processor**: `apps.panel.context_processors.site_settings` — همه‌ی تمپلیت‌ها به `{{ site_settings.<key> }}` دسترسی دارند (خالی اگر کلید نباشد، بدون خطا)
- **احراز هویت**: `LOGIN_URL = "/accounts/login/"`، `LOGIN_REDIRECT_URL = "/"`، `LOGOUT_REDIRECT_URL = "/"` — **پروفایل** (`accounts:profile`): چیپ نام کاربری در نوبار حالا **لینک به پروفایل** است؛ پنل مدیریت (`panel:dashboard`) از هدر حذف و **فقط داخل پروفایل برای staff** نمایش داده می‌شود. درخواست‌های تماس وقتی کاربر لاگین باشد به `ContactMessage.user` متصل می‌شوند و در پروفایل فهرست می‌شوند.
- **MIDDLEWARE**: ترتیب مهم است — `SecurityMiddleware` ← `WhiteNoiseMiddleware` ← ...
- `ROOT_URLCONF = "config.urls"`، قالب‌ها از `templates/` (`APP_DIRS=True`)
- دیتابیس پیش‌فرض: **SQLite** (`db.sqlite3`)
- `LANGUAGE_CODE = "fa-ir"`، `TIME_ZONE = "Asia/Tehran"`
- استاتیک: `STATIC_URL = "static/"`، `STATICFILES_DIRS = [BASE_DIR/"static"]`، `STATIC_ROOT = BASE_DIR/"staticfiles"`
- **STORAGES**: پیش‌فرض = `whitenoise.storage.CompressedManifestStaticFilesStorage` (هش فایل + فشرده‌سازی)
- ایمیل: `console` backend، `DEFAULT_FROM_EMAIL = "noreply@example.com"` (placeholder — قبل از دیپلوی با دامنه‌ی واقعی عوض شود)، `CONTACT_NOTIFY_EMAIL = "amirrezahajiabadi480@gmail.com"`
- `DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"`

### `development.py` — محلی
- `DEBUG=True`، `SECRET_KEY` ثابت توسعه، `ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".ngrok-free.app", ".ngrok-free.dev", ".pinggy.io", ".pinggy-free.link", ".free.pinggy.net"]` (دقیق — به‌جای `["*"]`؛ شامل تانل‌های ngrok/pinggy برای نمایش عمومی سایت)
- `CSRF_TRUSTED_ORIGINS = ["https://*.ngrok-free.app", "https://*.ngrok-free.dev", "https://*.pinggy.io", "https://*.pinggy-free.link", "https://*.free.pinggy.net"]` — برای ارسال فرم‌ها از دامنه‌ی تانل (Origin خارجی)
- ⚠️ **تانل عمومی**: باینری ngrok در `.freebuff/bin/ngrok.exe` (خارج از git — نسخه‌ی v3)؛ توکن در `%LOCALAPPDATA%\ngrok\ngrok.yml` — هرگز در پروژه/کامیت ننویس. **ngrok از IP ایران بلاک شده** (`ERR_NGROK_9040: agents not allowed from this IP`) — راه‌حل جایگزین فعال: **pinggy** (با `ssh -p 443 -R0:localhost:8471 a.pinggy.io`، بدون ثبت‌نام؛ URL های `.run.pinggy-free.link` / `.free.pinggy.net` می‌دهد — دامنه‌هایشان به ALLOWED_HOSTS/CSRF_TRUSTED اضافه شده؛ نسخه‌ی رایگان ۶۰ دقیقه و کمی کندتر است). `django_ngrok` از INSTALLED_APPS حذف شد (در requirements نبود — نصب تمیز را می‌شکست).
- **اعلان تلگرام**: `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` — placeholder قابل ویرایش در همین فایل (`PASTE_BOT_TOKEN_HERE`)؛ خالی/placeholder = غیرفعال بی‌صدا. (سرویس: `apps/core/services.py`)
- کش درون‌حافظه‌ای LocMemCache
- **`STORAGES` → `config.storage.MtimeStaticFilesStorage`** (کلاس توسعه در `config/storage.py`): به هر URL استاتیک `?v=<mtime فایل>` اضافه می‌کند — وقتی فایل تغییر کند URL عوض می‌شود و مرورگر نسخه‌ی تازه را می‌گیرد (**بدون نیاز به Ctrl+F5** در توسعه؛ production با whitenoise hash دست‌نخورده است). فایل بدون تغییر → همان URL → کش سالم و سریع.

### `production.py` — تولید (هنوز تست نشده)
- `DEBUG=False`، `SECRET_KEY` و همه‌ی رازها فقط از `os.environ` (تابع `env()` با خطای واضح)
- `ALLOWED_HOSTS` از env (پیش‌فرض `localhost,127.0.0.1`)
- **HTTPS سخت‌گیرانه**: SSL Redirect، کوکی‌های امن، HSTS (یک سال + includeSubdomains + preload)، `CSRF_TRUSTED_ORIGINS` خودکار از ALLOWED_HOSTS
- دیتابیس: **PostgreSQL** (`POSTGRES_DB/USER/PASSWORD/HOST/PORT` از env — مطابق docker-compose فاز ۵)
- ایمیل SMTP قابل تنظیم از env
- LOGGING کنسول

> ⚠️ نکته برای توسعه‌دهنده: برای فعال‌سازی تولید باید `DJANGO_SETTINGS_MODULE=config.settings.production` ست شود (WSGI پیش‌فرض آن را می‌خواند).

---

## ۵) URL ها و ویوها (مسیرهای کامل)

| مسیر | ویو | نام URL | توضیح |
|------|-----|---------|-------|
| `/` | `apps.core.views.index` | `core:index` | صفحه‌ی اصلی |
| `/about/` | `apps.core.views.about` | `core:about` | درباره |
| `/services/` | `apps.core.views.services` | `core:services` | خدمات |
| `/projects/` | `apps.projects.views.project_list` | `projects:list` | نمونه‌کارها (از DB) |
| `/blog/` | `apps.blog.views.blog_list` | `blog:list` | لیست مقالات |
| `/blog/<slug>/` | `apps.blog.views.blog_detail` | `blog:detail` | جزئیات مقاله + **کامنت** (مدل `Comment` — فقط لاگین‌شده‌ها، POST با CSRF، `is_visible` برای مدیریت) |
| `/contact/` | `apps.contact.views.contact` | `contact:index` | فرم تماس + FAQ — پری‌سلکت با `?type=` (مقادیر معتبر) و `?subject=` (U6: از ویجت مسیر انتخاب صفحه‌ی اصلی — ویجت موقتاً از صفحه‌ی اصلی حذف شده ولی پری‌سلکت فعال است) |
| `/accounts/login/` | `apps.accounts.views.NexifyLoginView` | `accounts:login` | ورود (مدیریت خودکار `?next=`) |
| `/accounts/register/` | `apps.accounts.views.register` | `accounts:register` | ثبت‌نام + ورود خودکار |
| `/accounts/logout/` | `apps.accounts.views.logout_view` | `accounts:logout` | خروج — فقط POST (CSRF-safe) |
| `/accounts/profile/` | `apps.accounts.views.profile` | `accounts:profile` | پروفایل کاربر (لاگین الزامی) — درخواست‌های تماس + دیدگاه‌ها + لینک پنل + **آمار خلاصه‌ی پنل** برای staff |
| `/admin/` | Django Admin | — | پنل مدیریت جنگو |
| `/panel/` | `apps.panel.views.dashboard` | `panel:dashboard` | ⭐ پنل ادمین سفارشی (فقط staff — مهمان → ورود) |
| `/panel/blog/` (+new/`<pk>`/toggle/delete) | `apps.panel.views` | `panel:blog_*` | مدیریت و انتشار مقالات |
| `/panel/projects/` (+new/`<pk>`/toggle/delete) | `apps.panel.views` | `panel:project_*` | مدیریت پروژه‌ها/محصولات |
| `/panel/messages/` (+`<pk>`/status/delete) | `apps.panel.views` | `panel:message_*` | مدیریت سفارش‌ها/پیام‌های تماس (وضعیت: new/in_progress/done) |
| `/panel/faq/` (+new/`<pk>`/toggle/delete) | `apps.panel.views` | `panel:faq_*` | مدیریت سوالات متداول |
| `/panel/testimonials/` (+new/`<pk>`/toggle/delete) | `apps.panel.views` | `panel:testimonial_*` | نظرات مشتریان (سکشن Social Proof صفحه‌ی اصلی — فاز U5) |
| `/panel/settings/` (+new/`<pk>`/delete) | `apps.panel.views` | `panel:setting_*` | ⭐ ویرایش متن‌های سایت بدون کد (هیرو/CTA/ایمیل/تلگرام...) |
| `/panel/users/` (+`<pk>/toggle-staff`) | `apps.panel.views` | `panel:user_*` | چند ادمین — فقط سوپریوزر ادمین می‌دهد/برمی‌دارد |

در تمپلیت‌ها حتماً از `{% url 'core:index' %}` و... استفاده می‌شود (نه مسیر سخت‌کد). ساختار urls مرکزی:
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("projects/", include("apps.projects.urls")),
    path("blog/", include("apps.blog.urls")),
    path("contact/", include("apps.contact.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("panel/", include("apps.panel.urls")),
]
```

---

## ۶) احراز هویت (accounts) — ورود/ثبت‌نام/خروج

- **ورود** (`NexifyLoginView` از `django.contrib.auth.views.LoginView`): مدیریت امن `?next=` (با محافظت در برابر open-redirect — next خارجی نادیده گرفته می‌شود)، `redirect_authenticated_user=True` (کاربر واردشده مستقیم به خانه می‌رود). فرم `LoginForm` = `AuthenticationForm` با برچسب‌های فارسی.
- **ثبت‌نام** (`register`): `RegisterForm` = `UserCreationForm` + فیلد `email` اجباری + **هانی‌پات `website`** (در ویو: پر شدن → بی‌صدا رد مثل موفقیت، بدون ساخت کاربر؛ در `clean()`: لایه‌ی دفاعی دوم — هر دو لایه تست دارند). بعد از ساخت، کاربر **خودکار وارد** می‌شود و به `?next=` (با اعتبارسنجی `url_has_allowed_host_and_scheme` — ضد open-redirect) یا خانه می‌رود.
- **خروج** (`logout_view`): فقط POST (سازگار با CSRF) — فرم کوچک `nav-logout-form` در نوبار با `{% csrf_token %}`. GET به صفحه‌ی ورود ریدایرکت می‌شود.
- **نوبار/منوی موبایل** با `{% if user.is_authenticated %}` شرطی: مهمان → دکمه‌های ورود/ثبت‌نام (هر دو با `?next={{ request.path }}` تا بعد از ورود/ثبت‌نام به همان صفحه برگردند) | واردشده → **باکس واحد شیشه‌ای `.auth-user-box`** (پوسته‌ی `--glass-bg` + blur 12px + انیمیشن ورود `userChipIn`) شامل: لینک پروفایل `.auth-user-chip` (آواتار دایره‌ای گرادیانی با **آیکون کاربری SVG از پیش آماده** `.auth-user-icon` + نام) + **جداکننده‌ی عمودی `.auth-user-divider`** + دکمه‌ی خروج `.auth-btn-logout` (آیکون SVG log-out، hover قرمز با پس‌زمینه‌ی قرمز کمرنگ). پنل مدیریت از هدر حذف شده — فقط از صفحه‌ی پروفایل (staff). **در موبایل (≤768px) دکمه‌های auth در هدر فشرده و همیشه نمایان هستند** (قبلاً `display:none` بودند و فقط پشت منوی همبرگری بودند). جزئیات بیشتر و فازهای بعدی: `RESPONSIVE-ROADMAP.md`.
- **استایل**: `static/css/auth.css` — اُرب‌های گرادیانی شناور (`auth-orb-*`، فقط transform/opacity → GPU)، شبکه‌ی نقطه‌چین متحرک `auth-grid`، کارت شیشه‌ای با ورود فنری `authCardIn` + خط گرادیان بالای کارت، **هاله‌ی دنبال‌کننده‌ی موس** `.auth-card-glow` (JS فقط `transform`/`opacity` ست می‌کند — rAF throttle، سازگار با CSP)، دکمه‌ی ارسال گرادیانی با موج نور `authBtnShine` + درخشش تنفسی `authBtnGlow` (`.auth-submit` با `justify-content: center` — متن دکمه وسط است چون `.btn` پایه inline-flex بدون justify-content است)، لرزش کارت روی خطا `authShake`، متر قدرت رمز (راهنمای UX فقط — اعتبارسنجی واقعی سمت سرور)، گارد `prefers-reduced-motion` و `@media (hover:none)`. **ریسپانسیو (R1/R2)**: اینپوت‌ها در موبایل `font-size: 1rem` (ضد زوم iOS — در style.css سراسری)، اُرب‌ها در موبایل کوچک‌تر/کم‌رنگ‌تر، eye-toggle 40px، `100dvh`، safe-area، `touch-action: manipulation`، `tap-highlight: transparent` — جزئیات در `RESPONSIVE-ROADMAP.md`.
- **JS**: `static/js/auth.js` — eye toggle رمز عبور (تغییر type + آیکن دوحالته)، spotlight با rAF، متر قدرت رمز (ضعیف/متوسط/قوی — اتصال به اینپوت با `data-target` روی متر). بدون inline handler → سازگار با CSP.

---

## ۶) مدل‌های دیتابیس

### `Project` (apps/projects/models.py)
فیلدها: `title`، `order`، `icon` (اموجی)، `cover_image` (ImageField اختیاری — آپلود از پنل)، `categories` (کلیدهای فیلتر با فاصله مثل `"web ai"`)، `category_label`، `short_description`، `description` (مودال)، `tags` (JSONField — لیست تکنولوژی‌ها)، `duration`، `role`، `status`، `github_url`، `gradient` (رشته‌ی CSS گرادیان **خام** مثل `135deg,#1e1b4b,#312e81` — بدون `linear-gradient()`؛ قالب آن را wrap می‌کند)، `is_published`، `created_at`
- ترتیب‌دهی: `["order"]` — ویو فقط `is_published=True` را می‌دهد.

### `BlogPost` (apps/blog/models.py)
فیلدها: `title`، `slug` (unique — آدرس سئو-دوست)، `category`، `icon`، `gradient`، `cover_image` (ImageField اختیاری — آپلود از پنل)، `excerpt`، `content` (متن کامل)، `read_time`، `published_at` (DateField)، `is_published` (پیش‌فرض **False** — باید از ادمین True شود)
- ترتیب‌دهی: `["-published_at"]` — ویوها `is_published=True` را فیلتر می‌کنند.

### `ContactMessage` (apps/contact/models.py)
- `REQUEST_TYPES` (۸ انتخاب — به ترتیب تمرکز): agent-ai / automation / mlops / consulting / web-design / app-development / education / other
- `CONTACT_METHODS` (۲ انتخاب): phone (تماس تلفنی، پیش‌فرض) / telegram (تلگرام)
- فیلدها: `name`، `email`، `contact_method` (پیش‌فرض phone)، `phone` (اختیاری)، `telegram_id` (اختیاری — «@» ابتدایی در فرم حذف می‌شود)، `request_type`، `subject` (اختیاری)، `message`، `is_read`، `status` (new / in_progress / done — از پنل تغییر می‌کند)، `created_at`
- **اعتبارسنجی شرطی در فرم**: روش «تماس تلفنی» → `phone` الزامی؛ روش «تلگرام» → `telegram_id` الزامی (طبق انتخاب کاربر فقط یکی پر می‌شود)
- ترتیب‌دهی: `["-created_at"]`

### `FAQ` (apps/contact/models.py)
- فیلدها: `question`، `answer`، `order`، `is_published` — ترتیب: `["order"]`

### `Testimonial` (apps/panel/models.py) — نظر مشتری (فاز U5)
- فیلدها: `name`، `company` (شرکت/سمت — «لوگو»ی متنی)، `text`، `rating` (۱-۵ با validator)، `order`، `is_published`، `created_at` — ترتیب: `["order", "id"]`
- **نمایش در صفحه‌ی اصلی**: `apps/core/views.py` → نظرات منتشرشده (حداکثر ۳) + لوگو/نام مشتریان = شرکت‌های یکتا + **آمار واقعی**: پروژه‌ی موفق/مقاله = شمارش منتشرشده، مشتری راضی = شرکت‌های یکتا، رضایت = میانگین امتیاز ×۲۰
- **پنل**: `/panel/testimonials/` (CRUD + toggle) — ستاره‌ها با فیلتر `{{ t.rating|stars }}` (SVG، فاز U5)
- در Django Admin نیز ثبت شده (list_editable: order/is_published)

### `PageView` (apps/panel/models.py) — آمار بازدید
- فیلدها: `path` (مسیر)، `session_key` (اختیاری — شمارش بازدیدکننده‌ی تقریبی)، `created_at`
- توسط **`VisitTrackingMiddleware`** (config/middleware.py — آخرین در MIDDLEWARE، بعد از SessionMiddleware) ثبت می‌شود: فقط GET موفق (200) صفحات عمومی؛ `/panel`، `/admin`، `/static/`، `/media/`، `/accounts/`، `/favicon.ico`، `/robots.txt` ثبت نمی‌شوند؛ **fail-safe** (خطا هرگز جریان اصلی را نمی‌شکند).
- **داشبورد**: کل/امروز/۷ روز/۳۰ روز + نمودار ۱۴ روزه (CSS خالص — `--h` custom property، بدون کتابخانه، سازگار با CSP) + پربازدیدترین ۵ صفحه.
- در Django Admin فقط‌خواندنی است (add/change ممنوع).

---

## ۶٫۵) پنل ادمین سفارشی (apps/panel) — راهنمای سریع

- **ورود**: `/panel/` — فقط `staff` (مهمان → `/accounts/login/?next=/panel/`). دکمه‌ی «خروج از پنل» در سایدبار. لینک ورود به پنل فقط از **صفحه‌ی پروفایل** (برای staff) در دسترس است — در نوبار نیست.
- **داشبورد**: آمار (تعداد مقالات منتشرشده، پروژه‌ها، سفارش‌های جدید، کاربران/ادمین‌ها) + **آمار بازدید** (کل/امروز/۷ روز/۳۰ روز + نمودار ۱۴ روزه با CSS خالص + پربازدیدترین صفحات — از مدل `PageView` که توسط `VisitTrackingMiddleware` پر می‌شود) + آخرین سفارش‌ها و مقالات.
- **مقالات**: لیست + فرم (new/edit) + toggle انتشار + حذف — `BlogPostForm` (مدل BlogPost با `is_published`). فرم‌ها `enctype="multipart/form-data"` دارند (فایل‌ها بدون `request.FILES` در ویو ذخیره نمی‌شوند — دو ویو `blog_edit`/`project_edit` آن را پاس می‌دهند).
- **پروژه‌ها**: لیست + فرم + toggle + حذف — `ProjectForm` (فیلد `tags` متن با ویرگول → JSONField؛ `gradient` رشته‌ی CSS خام مثل `135deg,#1e1b4b,#312e81`).
- **تصویر شاخص (⭐ آپلود)**: هر دو مدل `cover_image` (ImageField اختیاری) دارند — در فرم‌های پنل با پیش‌نمایش زنده (`panel.js` → `#coverPreview`، بدون inline handler). فایل‌ها در `media/blog_covers/` و `media/project_covers/` ذخیره می‌شوند و در سایت: کارت‌های بلاگ (`blog-image-photo`)، صفحه‌ی جزئیات مقاله، کارت پروژه (`project-visual-photo`) و مودال (`data-cover` → `modal-cover` در `projects.js`). اگر تصویری نباشد گرادیان قبلی نمایش داده می‌شود. **نیازمند Pillow** (در requirements.txt). `MEDIA_URL`/`MEDIA_ROOT` در `base.py` + سرو شدن در DEBUG در `config/urls.py`.
- **سفارش‌ها/پیام‌ها**: لیست با فیلتر وضعیت + جزئیات + تغییر وضعیت (`new`/`in_progress`/`done` — از `ContactMessage.status`) + حذف.
- **نظرات مشتریان (⭐ فاز U5)**: لیست + فرم (new/edit) + toggle نمایش + حذف — `TestimonialForm`. سکشن Social Proof صفحه‌ی اصلی (مارکی لوگو + ۳ کارت نظر + آمار واقعی) کاملاً از همین‌جا کنترل می‌شود.
- **FAQ**: لیست + فرم + toggle + حذف.
- **متن‌های سایت** (⭐): `SiteSetting` با `key` یکتا (مثل `hero_title_1`، `cta_title_2`، `contact_email`) — ویرایش بلافاصله در سایت بازتاب می‌یابد. Context processor `site_settings` همه‌ی کلیدهای فعال را به `{{ site_settings.<key> }}` می‌دهد. کلیدها را بعد از ساخت تغییر نده (در قالب‌ها استفاده شده‌اند). seed: `python manage.py seed_settings` (۱۰ متن پیش‌فرض — idempotent).
- **کاربران (چند ادمین)**: فقط **سوپریوزر** می‌تواند `is_staff` بدهد/بردارد (`user_toggle_staff` — POST-only، نمی‌تواند خودش را حذف کند).
- **CSP**: پنل از `base_panel.html` استفاده می‌کند که متای CSP **ندارد** — سرور توسعه‌ی جنگو هدر CSP ندارد و پنل `panel.js` خارجی است، پس هیچ اسکریپت inline ای لازم نیست. در تولید، `nginx-security.conf`/`_headers` پوشش می‌دهند.
- **طراحی**: `static/css/panel.css` (شیشه‌ای RTL هماهنگ با سایت) + `static/js/panel.js` (حذف با تأیید، بدون inline handler).

---

## ۷) فرم تماس امن (مهم)

**سه لایه دفاعی دارد:**

1. **CSRF**: `{% csrf_token %}` داخل فرم — توکن خودکار جنگو.
2. **هانی‌پات سمت کلاینت** (`static/js/contact.js`): فیلد مخفی `#hpWebsite` (`name="website"`) داخل `.hp-wrap` (مخفی با CSS — الگوی `sr-only` با `clip: rect(0,0,0,0)`؛ نه `left:-9999px` چون در RTL scrollWidth صفحه را پف می‌کرد، `tabindex="-1"`، `autocomplete="off"`) — اگر ربات آن را پر کند، اسکریپت فرم را **ساکت رد** می‌کند.
3. **هانی‌پات سمت سرور** (دو لایه):
   - در **ویو** (`contact`): اول از همه `if request.POST.get("website"):` → ساکت رد (بدون خطا، بدون ذخیره در DB، پیام موفقیت نمایش داده می‌شود تا ربات متوجه نشود).
   - در **فرم** (`forms.py`): `clean()` هم چک می‌کند و `ValidationError` می‌دهد — فیلد `website` **عمداً در `Meta.fields` نیست** تا هرگز در DB ذخیره نشود.

**جریان موفق**: POST معتبر → `form.save()` → ارسال ایمیل اطلاع‌رسانی (`_notify_by_email` با `fail_silently=True` — شکست ایمیل جریان را نمی‌شکند) → رندر دوباره با `success=True` → تمپلیت پیام موفقیت نمایش می‌دهد.

**اعتبارسنجی**: `name` (min 2)، `message` (min 10)، ایمیل استاندارد + **اعتبارسنجی شرطی روش تماس** (روش «تماس تلفنی» → `phone` الزامی؛ روش «تلگرام» → `telegram_id` الزامی و «@» ابتدایی حذف می‌شود) — سمت سرور مطابق سمت کلاینت.

**سرریز افقی موبایل** (`contact.css` + `style.css`): اینپوت‌ها عرض ذاتی min-content دارند و ترک‌های `1fr` زیر آن جمع نمی‌شوند → فرم از ستون بیرون می‌زد. رفع: `repeat(2, minmax(0,1fr))` برای `.form-row`/`.contact-method-group`، `min-width:0` روی `.form-input/.form-textarea` (سراسری)، و در موبایل `minmax(0,1fr)` برای `.contact-layout` + `min-width:0` روی `.form-card`/`.contact-info-cards`. توجه: scrollWidth ~10000px در صفحه‌ی تماس از هانی‌پات (`left:-9999px`) و منوی موبایل بسته است — عمدی، بی‌خطر.

**روش تماس در UI** (`contact.html` + `contact.css` + `contact.js`): انتخاب‌گر دو کارتی شیشه‌ای (`📞 تماس تلفنی` / `✈️ تلگرام`) داخل پوسته‌ی `.contact-method-group` — هر کارت `.method-card` شامل: آیکون‌باکس `.method-icon` (روی انتخاب → گرادیان بنفش `#8b5cf6→#6d28d9` + درخشش؛ آیکون تلگرام = **لوگوی رسمی SVG** `.method-icon-svg` با `fill="currentColor"` — خاکستری عادی → سفید روی حالت انتخاب)، عنوان + زیرعنوان `.method-sub`، و نشان `✓` فنری `.method-check`. حالت انتخاب: بوردر بنفش + گرادیان شیشه‌ای + سایه‌ی درخشش؛ **هاله‌ی دنبال‌کننده‌ی موس** `.method-spot` روی پوسته (JS فقط `--mx/--my` را با rAF ست می‌کند — CSP-safe، گارد `prefers-reduced-motion` و `(hover:none)`). در موبایل ≤480px کارتها عمودی می‌شوند. JS (`syncMethodGroups`) فقط فیلد متناظر را نمایش می‌دهد (`.hidden` toggle روی `#phoneGroup`/`#telegramGroup`) و `required` را جابه‌جا می‌کند. در ایمیل اطلاع‌رسانی (`_notify_by_email`) روش تماس + آیدی تلگرام هم درج می‌شود.

**آیکون‌های نوع درخواست** در ویو (`REQUEST_TYPE_ICONS`) برای سلکت سفارشی UI.

---

## ۷٫۵) اعلان به مالک سایت (تلگرام — اختیاری)

- سرویس: `apps/core/services.py` — `send_telegram_notify(text)` با **urllib استاندارد** (بدون وابستگی جدید)، همیشه **fail-silent** (خطا هرگز جریان اصلی را نمی‌شکند)، متن با `html.escape` پاک‌سازی می‌شود (قبل از `parse_mode=HTML`).
- پیام‌های آماده: `notify_contact_message(message)` (📩 پیام جدید فرم تماس) و `notify_new_user(user, ip)` (🆕 ثبت‌نام جدید + IP بازدیدکننده).
- اتصال‌ها: در `apps/contact/views.py` بعد از `form.save()` و در `apps/accounts/views.py` بعد از ساخت کاربر (قبل از ورود خودکار).
- تنظیمات: `TELEGRAM_BOT_TOKEN` و `TELEGRAM_CHAT_ID` — `base.py` از env (پیش‌فرض خالی)، `development.py` placeholder قابل ویرایش، `production.py` از env (اختیاری). مقادیر خالی/placeholder → بدون هیچ درخواست شبکه‌ای غیرفعال.
- ساخت بات: توکن از **@BotFather** و آیدی چت از **@userinfobot** (یا `getUpdates`).
- تست: ۵ تست سرویس در `apps/core/tests.py` (خالی / placeholder / ارسال موفق با mock / خطای شبکه / **escape محتوای کاربر**) + تست اتصال ویوها (mock) + تست «هانی‌پات اعلان نمی‌فرستد» در `apps/contact` و `apps/accounts`.

---

## ۸) تمپلیت‌ها و partial ها

### `base.html` — بلاک‌ها
- `{% block title %}` — عنوان صفحه
- `{% block meta %}` — متاتگ‌های اضافه (توضیحات/OG)
- `{% block extra_css %}` — CSS صفحه
- `{% block content %}` — محتوای اصلی
- `{% block extra_js %}` — JS صفحه

**ترتیب لود در پایین body**: `js/vendor/lenis.min.js` (self-hosted، فاز U7 — بدون CDN) (defer) ← `js/main.js` (defer) ← اسکریپت صفحه.

**CSP متا در head** همه‌ی صفحات (مهم، دست‌نزنید):
```
default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'
```
(فاز U7: `https://cdn.jsdelivr.net` از script-src حذف شد — Lenis self-host شد.)

**فونت‌ها (فاز U7)**: `@font-face` و preload هر دو در `partials/fonts.html` با URL نسخه‌دار `{% static %}` — دقیقاً منطبق → هر فونت یک بار دانلود می‌شود (در توسعه `?v=<mtime>`، در تولید نام هش‌شده). از `style.css` حذف شد.

### قوانین مهم تمپلیت
- همه‌ی فایل‌های استاتیک با `{% static 'css/...' %}` و `{% static 'js/...' %}` ارجاع می‌شوند (اول `{% load static %}`).
- لینک‌های داخلی فقط با `{% url 'app:name' %}`.
- **هیچ استایل inline در تمپلیت‌ها نیست** (به‌خاطر قانون پروژه). فقط دو استثنای مجاز:
  - `style="--grad:linear-gradient({{ post.gradient }});"` — گرادیان دیتا-محور (مقدار `gradient` در DB **خام** ذخیره می‌شود مثل `135deg,#1e1b4b,#312e81` — بدون `linear-gradient()`؛ wrap کردن با `linear-gradient()` فقط در قالب است. اگر مقدار DB کامل بود، دوگانه نشود!) → در CSS با `background: var(--grad);` اعمال می‌شود.
  - `style="--i:N"` برای تأخیر انیمیشن کارت‌ها.
- **کلاس‌های utility مشترک** (در `style.css`): `.accent-text` (رنگ تاکید)، `.grid-empty-state` (پیام خالی لیست‌ها)، `.nav-auth`/`.auth-btn` (دکمه‌های ورود/ثبت‌نام در نوبار با انیمیشن نور — `.auth-btn-register` گرادیان بنفش + پالس درخشش `authGlow` + موج نور شیب‌دار `authShine`، `.auth-btn-login` خطی شیشه‌ای، نسخه‌ی موبایل داخل `mobile_menu.html` با `.mobile-auth`؛ لینک ورود به `accounts:login` با `?next=` و ثبت‌نام به `accounts:register` وصل شده‌اند؛ کاربر واردشده چیپ شیشه‌ای نام کاربری `.auth-user-chip` (پوسته‌ی `--glass-bg` + بوردر + انیمیشن ورود نرم `userChipIn` + hover با درخشش بنفش و lift؛ آواتار `.auth-user-avatar` دایره‌ی گرادیانی بنفش با **آیکون SVG کاربر** `.auth-user-icon` — `currentColor`، بدون حرف اول نام — درخشش تنفسی `userAvatarGlow` و بزرگ‌شدن فنری روی hover؛ گارد `prefers-reduced-motion` دارد) + فرم خروج `.nav-logout-form` با دکمه‌ی `.auth-btn-logout` می‌بیند)، **`.coming-soon-badge`** (برچسب «به‌زودی» کهربایی با انیمیشن پالس `soonPulse` + نقطه‌ی چشمک‌زن `soonBlink` — برای سرویس‌های آماده‌نشده، فعلاً استقرار مدل). کلاس‌های اختصاصی هر صفحه در همان CSS صفحه تعریف شده‌اند (مثل `.section-flush-top`، `.projects-section`، `.newsletter-section`، `.btn-resend`). استایل جدید → کلاس جدید، هرگز `style=`.
- **سرویس «استقرار مدل» (MLOps) «به‌زودی»** (۴ جا، همه با انیمیشن کهربایی متفاوت از بقیه — spotlight/بوردر کهربایی به‌جای بنفش؛ چرخش آیکون ⚙️ با `soonSpin` فقط روی صفحه‌ی خدمات `.service-reveal-icon` باقی است): کارت صفحه‌ی اصلی (`.service-card-soon` در `index.css`)، کارت صفحه‌ی خدمات (`.service-reveal-card-soon` در `services.css`)، فیلتر + کارت‌های نمونه‌کارها (`filter-btn-soon` و `project-soon-badge` در `projects.css` — badge روی کارت با `{% if 'mlops' in project.categories %}` از DB)، گزینه‌ی فرم تماس (`.select-option-soon` در `contact.css` — با `{% if opt.value == 'mlops' %}`). اگر سرویس دیگری آماده نشد، همین الگو را تکرار کن؛ اگر استقرار مدل آماده شد، کلاس‌ها را حذف کن.
- **بخش خدمات صفحه‌ی اصلی** (در `index.html` + `index.css`): Bento grid ناهم‌ساز — کارت بزرگ `ساخت Agent هوش مصنوعی` (`.service-card-feature` ۲×۲) + ۴ سرویس کوچک + کارت CTA تمام‌عرض (`.service-card-cta` با `grid-column: 1 / -1`). هر کارت: **آیکون SVG شیشه‌ای** (`.service-card-icon` — باکس ۵۰px با `--glass-bg`/`--glass-border` و گوشه‌ی 14px، آیکون stroke با `currentColor` خاکستری؛ روی hover → گرادیان رنگی متمایز هر سرویس + آیکون سفید + درخشش + پاپ فنری؛ کارت بزرگ Agent AI باکس ۶۲px). **هویت رنگی هر سرویس** (با کلاس‌های `service-card-*`): ساخت Agent AI = سبز زمردی `.service-card-green` (`#10b981→#059669`)، پکیج اتوماسیون = فیروزه‌ای `.service-card-cyan` (`#06b6d4→#0891b2` + title/arrow `#22d3ee` + `::before` فیروزه‌ای)، استقرار مدل = کهربایی `.service-card-soon` (`#fbbf24→#f59e0b`، آیکون تیره) + چرخش آرام چرخ‌دنده `.service-card-icon-gear` با `soonSpin`، مشاوره AI = بنفش `.service-card-purple` (`#8b5cf6→#6d28d9`)، طراحی وب/اپ = آبی `.service-card-blue` (`#3b82f6→#2563eb`) + بج `.side-skill-badge` (خاکستری ظریف — برای اسکیل‌های مکمل). نور دنبال‌کننده‌ی موس (`.service-card::before` با `--mx/--my`)، خط گرادیانی پایین کارت در hover (`.service-card::after`)، فلش ←. کارت CTA تمام‌عرض با آیکون 💬. آیکون‌ها: Agent AI=CPU، اتوماسیون=Zap، استقرار مدل=Settings، مشاوره=CPU، طراحی وب=Globe (Feather-style، `aria-hidden`).) کلاس‌های `service-pill`/`services-minimal` قدیمی حذف شدند — در `style.css` فقط `.service-card` ارجاع دارد (micro-interactions + `@media (hover:none)`).
- حلقه‌های دیتا: `{% for project in projects %}` — کارت‌ها دیتا-اتریبیوت‌های `data-*` دارند که `projects.js` از آن‌ها مودال می‌سازد (بدون innerHTML!).

---

## ۹) فرانت‌اند (CSS/JS)

### فایل‌های JS
| فایل | وظیفه |
|------|-------|
| `main.js` | مشترک: `initTheme` (تم تاریک/روشن + localStorage با کلید `nexify-theme`)، `initPreloader`، `initCounters` (شمارنده‌های آمار با IntersectionObserver)، `initReveal` (انیمیشن اسکرول)، `initNavbar` (افکت اسکرول)، `initBackToTop`، `initMobileMenu`، `initActiveNav` (هایلایت نوبار با URL های جنگو)، `initSmoothScroll` (Lenis) |
| `index.js` | شبکه‌ی عصبی Canvas + ذرات شناور + **نور دنبال‌کننده‌ی موس روی کارت‌های خدمات** (`.service-card` — custom properties `--mx/--my` + requestAnimationFrame، CSP-safe) |
| `about.js` | انیمیشن نوار مهارت‌ها (IntersectionObserver) + **نور دنبال‌کننده‌ی موس در بخش «ما که هستیم؟»** (custom properties `--mx/--my` + requestAnimationFrame — بدون inline handler، سازگار با CSP) |
| `projects.js` | **فیلتر دسته‌بندی** (کلیک روی چیپ‌ها → نمایش/مخفی‌سازی کارت‌ها) + **مودال جزئیات** (createElement/textContent — بدون innerHTML، بدون استایل اینلاین) |
| `blog.js` | (اسکلت — لیست‌ها سمت سرور رندر می‌شوند) |
| `contact.js` | سلکت سفارشی (توسعه‌ی select مخفی)، اعتبارسنجی کلاینت، هانی‌پات کلاینت، **FAQ آکاردئون** (فقط یک کارت باز می‌ماند؛ بسته‌ها با اتریبیوت `hidden` = display:none واقعی حذف می‌شوند — در هیچ مرورگری محتوای بسته دیده/خوانده نمی‌شود؛ `aria-expanded`/`aria-controls` دارد؛ انیمیشن با reflow-guard حفظ شده؛ **باگ «کش‌آمدن کارت روبرو» رفع شد**: در گرید دوستونه، `align-items: start` در `.faq-grid` باعث می‌شود کارت مقابل در ردیف مشترک کش نیاید و شبیه بازشده‌ی بدون جواب دیده نشود)، ارسال فرم (JS اجازه می‌دهد فرم طبیعی submit شود — با CSRF کار می‌کند) |
| `auth.js` | صفحات ورود/ثبت‌نام: eye toggle رمز عبور (تغییر type + آیکن دوحالته با کلاس `active`)، هاله‌ی دنبال‌کننده‌ی موس روی کارت (rAF throttle + فقط transform/opacity)، متر قدرت رمز (۳ سطح — راهنمای UX، اعتبارسنجی واقعی سمت سرور) — بدون inline handler، سازگار با CSP |

> ⚠️ **قانون XSS**: هرگز از `innerHTML` با داده‌ی کاربری استفاده نکنید — `createElement` + `textContent` (باگ فاز ۲ رفع شده، این را حفظ کنید).

### فایل‌های CSS
- `style.css` — متغیرها (`--accent`, `--bg` و...) در `:root`، تم تاریک/روشن با `[data-theme]`، `@font-face` دو فونت متغیر، استایل‌های پایه (نوبار، دکمه‌ها، فوتر...)
- ⭐ **قانون کنتراست (U1)**: `--text`/`--text-secondary`/`--text-muted` در هر دو تم باید حداقل **۴.۵:۱** کنتراست داشته باشند (تیره: `#f5f5f5`/`#a3a3a3`/`#9ca3af` — روشن: `#1a1a1a`/`#4b5563`/`#6b7280`). رنگ جدید اضافه نکن مگر AA پاس کند.
- `index.css`، `about.css`، `services.css`، `projects.css`، `blog.css`، `contact.css`، `auth.css` — استایل‌های مخصوص هر صفحه

### فونت‌ها
- `@font-face` با `font-display: swap` و سینتکس متغیر مدرن: `format('woff2') tech('variations')`
- فارسی: Vazirmatn — مونو: JetBrains Mono
- **Google Fonts حذف شده** — هیچ درخواست خارجی برای فونت نیست.

---

## ۱۰) امنیت (خلاصه)

| لایه | پیاده‌سازی |
|------|-----------|
| CSP | صفحات: متا در `base.html`؛ ادمین: هدر از `config/middleware.py` (script-src شامل `'unsafe-inline'` چون ادمین جنگو اسکریپت اینلاین دارد) |
| هدرهای امنیتی | `_headers` (Netlify/Cloudflare) + `nginx-security.conf` (VPS — با رفع باگ ارث‌بری add_header در location ها) |
| XSS | حذف innerHTML، حذف handler های inline، autoescape جنگو |
| فرم | CSRF + هانی‌پات دولایه |
| احراز هویت | ورود با `LoginView` استاندارد (محافظت open-redirect)، خروج فقط POST (CSRF-safe)، هانی‌پات در ثبت‌نام، اعتبارسنجی رمز عبور جنگو |
| جنگو | کوکی‌های امن، HSTS، SSL Redirect در production |
| سمت سرور | `python manage.py check --deploy` (قبل از go-live) |
| اسکن خودکار | `python scripts/security_scan.py [URL]` — ۹۶ چک: هدرها، کوکی‌ها، CSRF، SQLi، XSS، traversal، OPTIONS/TRACE، فایل‌های حساس. آخرین اجرا روی توسعه: **73 PASS / 22 WARN / 0 FAIL** |

> ⚠️ **قانون CSP**: اگر اسکریپت/استایل جدیدی از CDN اضافه کردید، باید `script-src`/`style-src` در **متای base.html + فایل‌های هدر** هم‌زمان به‌روز شود. **هیچ‌وقت `script-src` ادمین را به `'self'` خالص سخت نکنید** — تمپلیت‌های ادمین جنگو (change_form، popup_response، prepopulated_fields_js) اسکریپت اینلاین دارند و بدون `'unsafe-inline'` می‌شکنند.

---

## ۱۱) دیتابیس و داده‌ی نمونه

- **دستور seed**: `python manage.py seed_demo` → ۶ پروژه + ۶ مقاله (با slug های مثل `fastapi-guide`) + ۶ FAQ. از `update_or_create` استفاده می‌کند (اجرای چندباره امن است).
- **سوپریوزر توسعه**: `admin` / `admin123` (فقط برای توسعه — در تولید هرگز).
- **داده‌ی فعلی**: ۶ پروژه، ۶ مقاله، ۶ FAQ، ۰ پیام تماس (تمیز).

---

## ۱۲) دستورات کاربردی

```bash
cd Nexify

# نصب وابستگی‌ها
python -m pip install -r requirements.txt

# نصب وابستگی‌های تست
python -m pip install -r requirements-dev.txt   # pytest + pytest-django

# اجرای سرور توسعه
python manage.py runserver 127.0.0.1:8471

# اسکرین‌شات‌های README (سرور در حال اجرا باشد)
python ../scripts/capture_screenshots.py    # → docs/screenshots/*.png (۸ صفحه، تمام‌صفحه، ۱۴۴۰px)

# اشتراک‌گذاری عمومی (نمایش به دوست/کلاینت) — ⚠️ ngrok از IP ایران بلاک است، از pinggy استفاده کن
./start_tunnel.sh   # ⭐ اسکریپت آماده: سرور را بالا می‌آورد + تانل pinggy می‌سازد + URL را نشان می‌دهد (PID واقعی ssh در .freebuff/pinggy.pid)
# معادل دستی:
ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -p 443 -R0:localhost:8471 a.pinggy.io   # تانل pinggy — URL ها را در خروجی می‌دهد (پس از ۶۰ دقیقه منقضی می‌شود)
# ngrok (اگر IP مجاز باشد):
../.freebuff/bin/ngrok.exe config add-authtoken <TOKEN>   # یک‌بار — توکن را کامیت نکن
../.freebuff/bin/ngrok.exe http 8471                      # تانل — URL در ترمینال/کنسول ngrok
curl -s http://127.0.0.1:4040/api/tunnels                 # یا URL عمومی را از API بگیر

# مایگریشن
python manage.py makemigrations
python manage.py migrate

# داده‌ی نمونه
python manage.py seed_demo

# ساخت سوپریوزر (توسعه)
python manage.py createsuperuser

# جمع‌آوری استاتیک (تولید)
python manage.py collectstatic --noinput

# بررسی سلامت (تولید: + --deploy)
python manage.py check
python manage.py check --deploy

# ⭐ اجرای تست‌ها (۱۱۵ تست)
pytest -v
pytest apps/contact -v                # فقط اپ تماس
pytest apps/accounts -v               # فقط اپ احراز هویت
pytest apps/contact/tests.py::test_honeypot_filled_is_silently_dropped -v   # یک تست خاص
```

### تست‌ها (pytest)

تست‌ها در `apps/<app>/tests.py` هر اپ هستند (سبک pytest با فیکسچرهای `client` و `db`) — **جمعاً ۷۳ تست**:

| اپ | تعداد | پوشش |
|----|------|------|
| `contact` | ۲۲ | فرم (اعتبارسنجی، هانی‌پات در `clean()`، اثبات عدم نگاشت website، **روش تماس شرطی: phone بدون شماره / telegram بدون آیدی نامعتبر، telegram با آیدی معتبر + حذف @ + رد قالب نامعتبر، phone آیدی تلگرام را نادیده می‌گیرد**)، GET (فرم + FAQ + CSRF)، POST معتبر (ذخیره + ایمیل با `locmem` backend)، **POST با روش تلگرام** (ذخیره‌ی آیدی + بدون نیاز به شماره)، **هانی‌پات ساکت رد**، POST نامعتبر، مدل‌ها (str، مرتب‌سازی، فیلتر FAQ منتشرشده)، **دسترس‌پذیری (U1): هر ۷ input دارای label با for منطبق** |
| `projects` | ۷ | مدل (str، مرتب‌سازی order، پیش‌فرض‌ها، JSONField تگ‌ها)، ویو (فقط is_published، ترتیب، حالت لیست خالی) |
| `blog` | ۱۰ | مدل (str، slug یکتا با `IntegrityError`، `is_published=False` پیش‌فرض، مرتب‌سازی، read_time پیش‌فرض)، لیست/جزئیات (فیلتر منتشرشده، 404 برای پیش‌نویس و slug ناموجود)، **آیکون SVG به‌جای ایموجی (U2)** |
| `core` | ۱۵ | رندر ۳ صفحه‌ی استاتیک (پارامتری) + **smoke تست ۶ مسیر عمومی ۲۰۰** (پارامتری) + زبان RTL و عنوان صفحه‌ی اصلی + **۵ تست سرویس اعلان تلگرام** (غیرفعال/placeholder/ارسال موفق با mock/خطای شبکه/escape) |
| `accounts` | ۲۱ | ثبت‌نام (GET فرم + CSRF، ساخت کاربر + ورود خودکار، رد رمزهای ناهماهنگ/نام کاربری تکراری، **هانی‌پات ساکت رد + لایه‌ی دوم clean()**، `?next=` به صفحه‌ی قبل + **بلاک next خارجی**، ریدایرکت کاربر واردشده)، ورود (GET، موفق → خانه، نامعتبر → خطا، `?next=` به صفحه‌ی قبل، **بلاک next خارجی**، ریدایرکت کاربر واردشده)، خروج (فقط POST، POST → لاگ‌اوت)، نوبار (مهمان → ورود/ثبت‌نام | واردشده → چیپ نام کاربری + خروج) |
| `panel` | ۱۹ | ⭐ پنل ادمین: مهمان/کاربر عادی → ریدایرکت به ورود، داشبورد، انتشار مقاله، ساخت/حذف پروژه، تغییر وضعیت پیام (done)، ساخت FAQ، **ویرایش متن سایت → بازتاب در صفحه‌ی اصلی** (context processor)، ساخت متن جدید، **آپلود تصویر شاخص مقاله → نمایش در لیست و جزئیات**، **آپلود تصویر شاخص پروژه → data-cover در کارت**، **آمار بازدید: فقط صفحات عمومی GET-موفق ثبت می‌شوند (پنل/ادمین/استاتیک نه)، ۴۰۴/POST نه، داشبورد جمع‌بندی + نمودار ۱۴ روزه + پربازدیدترین صفحات**، لیست همه‌ی کاربران، ادمین‌کردن/برداشتن توسط سوپریوزر، **نمی‌توان دسترسی خودش را بردارد**، ادمین غیرسوپریوزر نمی‌تواند ادمین بدهد |
| **جمع** | **۹۴** | — |

> ⚠️ **قانون**: بعد از هر تغییر در مدل/ویو/فرم، تست‌ها را اجرا کن: `pytest` — باید همه‌ی تست‌ها سبز بمانند.
> ℹ️ هشدار deprecation درباره‌ی `EMAIL_BACKEND` در جنگو ۶ (حذف در جنگو ۷ → مهاجرت به API جدید `MAILERS`) — تا جنگو ۶ مشکلی نیست، فقط برای آینده.

---

## ۱۳) اسکیل‌های نصب‌شده (Skills برای AI)

اسکیل‌ها به‌صورت آینه‌ای در **دو مکان** نصب می‌شوند — `.agents/skills/` و `.claude/skills/` — و در `skills-lock.json` (ریشه‌ی پروژه، کنار `Nexify/`) ردیابی می‌شوند (source + skillPath + computedHash). هر اسکیل جدید: همان ساختار (پوشه + `SKILL.md`) را در هر دو مکان نصب کن و یک entry به `skills-lock.json` اضافه کن.

| اسکیل | منبع (GitHub) | کاربرد |
|-------|---------------|--------|
| `html-css-best-practices` | hack23/homepage | بهترین‌پردازی HTML/CSS |
| `modern-web-design` | kuse-ai/kuse-skills | طراحی مدرن وب |
| `vanilla-web` | janjaszczak/cursor | وب خالص (بدون فریمورک) |
| `ui-ux-pro-max` ⭐ | nextlevelbuilder/ui-ux-pro-max-skill | هوش طراحی UI/UX — تولید سیستم طراحی (پالت رنگ، تایپوگرافی، استایل، ضدالگوها) |

### `ui-ux-pro-max` — راهنمای استفاده

- **SKILL.md** هنگام درخواست‌های UI/UX (طراحی/ساخت/بازبینی صفحه، کامپوننت، رنگ، تایپوگرافی، چیدمان، انیمیشن، داشبورد/چارت) خودکار فعال می‌شود.
- **موتور جستجو** (Python استاندارد — بدون وابستگی و بدون شبکه؛ روی ویندوز از `python` استفاده کن نه `python3`):

```bash
cd Nexify

# تولید سیستم طراحی کامل برای یک محصول (خروجی ASCII)
python ../.agents/skills/ui-ux-pro-max/scripts/search.py "AI services agency software development" --design-system -p "Nexify"

# خروجی Markdown
python ../.agents/skills/ui-ux-pro-max/scripts/search.py "fintech banking" --design-system -f markdown

# جستجوی دامنه‌ای: style / typography / color / chart
python ../.agents/skills/ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style

# راهنمای استک‌خاص
python ../.agents/skills/ui-ux-pro-max/scripts/search.py "responsive layout" --stack html-tailwind
```

- **دیتابیس داخلی**: ۶۷ استایل، ۱۶۱ پالت رنگ، ۵۷ جفت فونت، ۹۹ راهنمای UX، ۲۵ نوع چارت، ۲۲ استک.
- نصب از طریق CLI رسمی: `npx --yes ui-ux-pro-max-cli init --ai universal` (بدون نصب global).

---

## ۱۴) دیپلوی — وضعیت و برنامه (فاز ۵، انجام نشده)

**انجام شده در فازهای قبل**: `_headers` (Netlify/Cloudflare)، `nginx-security.conf`، `production.py` کامل، `requirements-prod.txt`، `.env.example`.

**انجام شده**: ✅ `pytest` (۹۹ تست) + ✅ `pytest.ini` + ✅ `requirements-dev.txt` + ✅ `.github/workflows/ci.yml`.

**CI (`.github/workflows/ci.yml`)** — روی هر push/PR به `main`، ماتریس Python 3.12 و 3.13، با کش pip (`requirements*.txt`):
1. نصب وابستگی‌ها: `pip install -r requirements.txt -r requirements-dev.txt`
2. `python manage.py check` (سلامت جنگو)
3. `python manage.py makemigrations --check --dry-run` — **تغییر مدل بدون فایل مایگریشن = شکست CI**
4. `pytest -v` (اجرای همه‌ی تست‌ها)

**باقی‌مانده (فاز ۵ طبق ROADMAP)**:
- `Dockerfile` + `docker-compose.yml` (django + postgres + nginx)
- `gunicorn.conf.py` + `entrypoint.sh`
- `.github/workflows/deploy.yml` (CD استقرار)
- انتخاب میزبان: Docker+VPS (Hetzner/DigitalOcean)، یا Railway/Render
- بکاپ خودکار دیتابیس، مانیتورینگ (Sentry/UptimeRobot)
- ⭐ **محدودسازی نرخ ورود (rate limiting / django-axes)** برای محافظت در برابر Brute-force — پیشنهاد امنیتی برای فاز ۵

**استک هدف**: `Nginx → Gunicorn (4-5 worker) → Django → PostgreSQL` + Whitenoise برای استاتیک.

**الگوی `.env.example`** (کلیدهای موردنیاز تولید):
```
DJANGO_SECRET_KEY=
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1
POSTGRES_DB=nexify
POSTGRES_USER=nexify
POSTGRES_PASSWORD=
POSTGRES_HOST=db
POSTGRES_PORT=5432
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@example.com
CONTACT_NOTIFY_EMAIL=amirrezahajiabadi480@gmail.com
```

---

## ۱۵) گیت — نسخه‌بندی

ریشه‌ی مخزن: **ریشه‌ی پروژه** (`D:/Nexify`) — شامل `Nexify/` + پوشه‌های اسکیل + `skills-lock.json`. برنچ پیش‌فرض: `main`. پیام‌های کامیت به **انگلیسی**.

- `.gitignore` دولایه: ریشه‌ی پروژه (`.freebuff/`, `__pycache__/`, قالب‌های common Python/Node/IDE/OS) + `Nexify/.gitignore` (django: `db.sqlite3` + journal/wal/shm, `staticfiles/`, `media/`, `media-test/`, `.env`, venv‌ها، کَش‌های ابزار).
- `.gitattributes` (ریشه): همه‌ی متن‌ها LF ذخیره/خروجی می‌شوند (هماهنگ با دیپلوی لینوکس؛ `*.bat/.cmd/.ps1` استثنا CRLF) + فونت‌ها/تصاویر/دیتابیس `binary` (دست‌نخورده). اگر فایل جدیدی با فرمت غیرمتن اضافه کردی، پسوندش را به بخش binary اضافه کن.
- **هرگز کامیت نکن**: `.freebuff/` (لاگ‌ها + دیتابیس داخلی ابزار — حاوی توکن ngrok)، `db.sqlite3`، `.env`، `media-test/` (خروجی تست آپلود)، `__pycache__`.
- **قانون ثابت**: بعد از هر تغییر، خودم کامیت می‌کنم (فایل‌های مرتبط فقط — نه `git add -A`)، با پیام انگلیسی و بدون `git push` مگر اینکه خواسته شود.

```bash
cd /d D:/Nexify
git status                      # وضعیت فعلی
git add <فایل‌های مرتبط>        # بدون git add -A (فایل‌های دیگر را نبر)
git commit -m "..."             # انگلیسی
git log --oneline -5
```

---

## ۱۶) وضعیت فازها (Roadmap)

| فاز | عنوان | وضعیت |
|-----|-------|--------|
| ۰ | Audit و بررسی | ✅ |
| ۱ | ساختاردهی مجدد فرانت (css/js جدا، حذف assets مرده، جداسازی inline ها) | ✅ |
| ۲ | امنیت (بدون innerHTML، هانی‌پات دوم، CSP + هدرها) | ✅ |
| ۳ | سرعت (فونت self-host، preload، defer، حذف Google Fonts) | ✅ |
| ۴ | **مهاجرت به جنگو** (settings سه‌تایی، ۴ اپ، base.html، فرم امن، Django Admin) | ✅ |
| ۴.۵ | **تست + CI** (۳۹ تست pytest: فرم/هانی‌پات/ویوها/مدل‌ها + workflow گیت‌هاب) | ✅ |
| ۴.۶ | **احراز هویت** (صفحات ورود/ثبت‌نام با انیمیشن + خروج POST-only + هانی‌پات دولایه + ۱۹ تست) | ✅ |
| ۴.۷ | **ریسپانسیو R1–R6** (نقشه‌ی راه در `RESPONSIVE-ROADMAP.md`) | ✅ |
| ۴.۸ | **پنل ادمین سفارشی** (اپ `panel` — داشبورد، انتشار مقاله/پروژه، مدیریت سفارش‌ها با وضعیت، ویرایش متن‌های سایت بدون کد، چند ادمین) | ✅ |
| ۴.۹ | **ممیزی UI/UX با اسکیل `ui-ux-pro-max`** — کنتراست شکست‌خورده‌ی `--text-muted`، ایموجی به‌جای آیکون، label بدون اتصال، مودال بدون focus-trap، تارگت لمس فوتر، preload فونت بیهوده + نقشه‌ی راه `UIUX-ROADMAP.md` (فازهای U1→U8) | ✅ (تحلیل) |
| ۵ | دیپلوی (Docker، Gunicorn، Nginx، PostgreSQL، CI/CD) | ⏳ **بعدی** |
| ۴.۱۰ | **بهبود UI/UX** — اجرای فازهای `UIUX-ROADMAP.md` (U1 کنتراست/فرم‌ها → U8 تایپوگرافی) | ✅ **U1–U9 همه انجام شد** — رودمپ UI/UX کامل (U8: وزن هیرو ۳۰۰ + spacing فارسی + سلسله‌مراتب CTA؛ U9: استانداردسازی تماس/درباره — page-title سراسری، دکمه‌های بدون spacing، چیپ‌های شیشه‌ای — ۹۹ تست) |
| ۴.۱۱ | **رفع باگ «محتوای حذف‌شده برمی‌گردد»** — سرور توسعه هدر کش نمی‌فرستاد و مرورگر صفحات داینامیک را کش می‌کرد؛ میان‌افزار `NoStoreCacheMiddleware` در `config/middleware.py` حالا روی همه‌ی پاسخ‌های داینامیک `Cache-Control: no-store` ست می‌کند (بعد از WhiteNoise — استاتیک دست‌نخورده). اثبات: حذف رکورد + ریاستارت سرور → برنگشت. +۶ تست (۱۰۵ تست) | ✅ |
| ۴.۱۲ | **چیدمان صفحه‌ی اصلی (درخواست مشتری، ۱۲ اوت ۲۰۲۶)** — سکشن‌های «راه‌حل بر اساس صنعت» و «مسیر انتخاب» (U6) از صفحه‌ی اصلی حذف شدند (CSS/JS عمداً حفظ شد — بازگردانی با paste HTML) و «نظرات مشتریان» به انتهای صفحه (دقیقاً قبل از CTA تماس) منتقل شد. ترتیب فعلی: هیرو → آمار → خدمات → نظرات مشتریان → CTA | ✅ |
| ۴.۱۳ | **بازطراحی آمار صفحه‌ی اصلی (۱۲ اوت ۲۰۲۶)** — پنل شیشه‌ای (`--glass-bg` + `blur(16px)` + بوردر نیمه‌شفاف — با صفحه ادغام می‌شود نه بلوک توپُر) + خط نور بالایی + جداکننده‌های درست در RTL + آیکون‌های هویتی رنگی (🚀 بنفش / 👥 سبز / ⭐ کهربایی / 📚 آبی — گرادیان روی hover) + **شمارنده‌ی نرم** (index.js: IntersectionObserver + rAF + easeOutQuart ۱.۶s + تأخیر پلکانی ۱۴۰ms + ارقام فارسی + `tabular-nums` + reduced-motion → مقدار نهایی). موبایل: ۲×۲ با جداکننده‌های اصلاح‌شده. تست‌های آمار به ساختار `span.stat-count` به‌روز شدند (۱۰۵ تست) | ✅ |
| ۴.۱۴ | **هدر + پروفایل کاربر (اوت ۲۰۲۶)** — ۱) رفع باگ آیکون ماه در دارک‌مود: `.theme-toggle` بدون `color` صریح بود → UA button رنگ سیاه می‌داد؛ حالا `color: var(--text)` + سایز SVG 20px. ۲) چیپ نام کاربری در نوبار **لینک به `accounts:profile`** شد؛ دکمه‌ی «پنل مدیریت» از هدر حذف و فقط داخل پروفایل برای staff نمایش داده می‌شود. ۳) صفحه‌ی پروفایل (`profile.html`): آواتار SVG + «درخواست‌های من» (`ContactMessage.user` — وقتی لاگین باشد به کاربر وصل می‌شود) + «دیدگاه‌های من» (مدل جدید `Comment` بلاگ — `apps/blog/models.py` + فرم + نمایش در `blog_detail`) + وضعیت پیام (new/in_progress/done). ۴) فاصله‌گذاری هدر بهینه (nav-links 34px، nav-auth gap 12px). ۵) **آمار خلاصه‌ی پنل در پروفایل staff** (`.profile-panel-stats`): سفارش‌های جدید (`status="new"`، لینک به `panel:message_list`) + کامنت‌های منتظر تأیید (`is_visible=False`). +۱۰ تست (۱۱۵ تست) | ✅ |
| ۴.۱۴ | **بازطراحی «فرآیند همکاری» صفحه‌ی خدمات (۱۲ اوت ۲۰۲۶)** — بج‌های شیشه‌ای دایره‌ای با **اعداد انگلیسی** ۰۱–۰۴ (خطاها: فارسی بود → انگلیسی) + خط اتصال گرادیانی که هنگام ورود به دید رسم می‌شود (scaleX با origin راست در RTL) + پاپ فنری پلکانی بج‌ها (easeOutBack + تأخیر ۲۰۰ms — با `nth-of-type` چون `.process-line` شاخص `nth-child` را جابه‌جا می‌کرد، باگ وسط انیمیشن پیدا و رفع شد) + hover گرادیان بنفش. خط با `calc((100% - 72px)/8)` دقیقاً به مرکز بج اول/آخر تراز است (گپ ۲۴px ستون‌ها را می‌کشد). موبایل: عمودی با اتصال‌های scaleY بین قدم‌ها. reduced-motion → حالت نهایی. فقط CSS + مکانیزم reveal موجود (بدون JS جدید) | ✅ |

> **ریسپانسیو — خلاصه‌ی فازهای انجام‌شده (جزئیات کامل در `RESPONSIVE-ROADMAP.md`):**
> - **R1 پایه/ایمنی**: `100dvh` منوی موبایل، safe-area ناچ، `tap-highlight` حذف، `touch-action: manipulation`، `overflow-x` بدن.
> - **R2 auth**: اینپوت‌ها در موبایل `font-size: 1rem` (ضد زوم iOS — سراسری در style.css)، اُرب‌ها کوچک‌تر/کم‌رنگ‌تر، eye-toggle 40px، `100dvh`.
> - **R3 صفحه‌ی اصلی**: هیرو `100dvh`، آمار خودکار ۲×۲ در موبایل، پس‌زمینه‌های متحرک کم‌رنگ‌تر در موبایل.
> - **R4 صفحات داخلی**: services گرید ۱ ستونه در 360px، مودال پروژه اسکرول‌پذیر + `overscroll-contain`، تایم‌لاین about، **رفع سرریز فرم تماس** (اینپوت‌ها min-content ذاتی دارند → `minmax(0,1fr)` در `.form-row`/`.contact-method-group` + `min-width:0` روی `.form-input/.form-textarea` سراسری + `min-width:0` روی `.form-card`/`.contact-info-cards`). توجه: scrollWidth ~10000px در صفحه‌ی تماس = هانی‌پات (`left:-9999px`) + منوی موبایل بسته — عمدی.
> - **R5 تایپوگرافی**: `clamp()` روی `.newsletter-title` و `.about-text-panel h2` (hero-title/page-title/cta-title از قبل clamp داشتند)؛ padding سکشن‌ها در ≤480 → ۷۲px (page-header ۸۸/۴۰، newsletter ۸۰، faq-wrap ۷۲/۸۰)؛ `.page-desc` در ≤480 → `1rem` + `line-height:1.9`؛ `.section-label` margin-bottom ۶۴→۴۰px.
> - **R6 پرفورمنس**: Lenis فقط روی `(hover:hover) and (pointer:fine)` ساخته می‌شود (موبایل → `scrollIntoView`/`window.scrollTo` نیتیو smooth در `main.js`)؛ Canvas شبکه‌ی عصبی (`index.js`) در `prefers-reduced-motion` فقط یک فریم ثابت رسم می‌کند و در `(hover:none)` ذرات کمتر (`/90000`) + ۳۰fps؛ ذرات شناور در reduced-motion ساخته نمی‌شوند؛ فونت‌ها از قبل `font-display:swap` + preload داشتند.

---

## ۱۷) قوانین طلایی برای هر AI که روی این پروژه کار می‌کند

1. **همیشه از پوشه‌ی `Nexify/` کار کن** — همه‌ی دستورات را با `cd Nexify` اجرا کن.
2. **هرگز CSP را نشکن**: بدون اسکریپت/استایل inline، بدون `innerHTML` با داده‌ی کاربری. تنها استثنای مجاز: `--grad` برای گرادیان‌های دیتا-محور و `--i:N` برای تأخیر انیمیشن. هر منبع خارجی جدید → به‌روزرسانی `script-src` در `base.html` + `_headers` + `nginx-security.conf`.
3. **فایل‌های استاتیک را به `static/` اضافه کن** و با `{% static %}` ارجاع بده — نه مسیر سخت‌کد.
4. **لینک‌های داخلی فقط با `{% url %}`** و نام‌های app_name (core:index و...).
5. **فرم‌ها با ModelForm جنگو** ساخته می‌شوند — همیشه `{% csrf_token %}`.
6. **داده‌ی محتوا از دیتابیس** می‌آید (نه هاردکد در قالب) — مگر صفحات استاتیک مثل درباره.
7. **روی نوبار/فوتر دست نزن مگر از طریق partial ها** — تکرار ممنوع.
8. اگر مدل/فیلدی تغییر کردی: `makemigrations` + `migrate` را فراموش نکن.
9. قبل از تحویل: `python manage.py check` + **`pytest` (همه‌ی تست‌ها سبز)** + تست در مرورگر + چک کنسول (صفر خطای CSP).
9. **تارگت لمسی همه‌ی المان‌های تعاملی ≥ ۴۴px** (U4): `min-height: 44px` + `flex-shrink: 0` برای دکمه‌های آیکونی هدر. هر المان تعاملی جدید باید حداقل ۴۴px (عرض یا ارتفاع) باشد — اسکن DOM بعد از هر تغییر UI.
10. `staticfiles/`، `db.sqlite3`، `.env` و `__pycache__` هرگز کامیت نمی‌شوند.
11. **بعد از هر تغییر (هر فایل/رفتاری)، `AI-CONTEXT.md` را همگام به‌روز کن** — ساختار پوشه‌ها، جدول‌ها، دستورات، شماره‌ی تست‌ها و تاریخ را اگر تغییر کرده‌اند اصلاح کن. این تنها راهی است که این سند برای AI های بعدی معتبر می‌ماند.

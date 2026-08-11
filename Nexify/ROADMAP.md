# 🗺️ Roadmap حرفه‌ای‌سازی پروژه Nexify

> **هدف:** تبدیل Nexify از یک وب‌سایت استاتیک به یک پروژه‌ی استاندارد، امن، سریع و آماده‌ی اتصال به بک‌اند **جنگو (Django)** و دیپلوی تولیدی.
>
> **نکته مهم:** این سند فقط نقشه‌ی راه است؛ هر فازی باید در یک برنچ جدا و با تست کامل انجام شود.

---

## 📊 فاز ۰ — وضعیت فعلی (Audit)

| بخش | وضعیت | مشکل |
|-----|--------|------|
| صفحات | ۷ فایل HTML مستقل | نوبار/فوتر/هدر در همه‌ی صفحات **کپی شده** (تکرار کد) |
| استایل | `style.css` مشترک + `<style>` درون‌صفحه‌ای هر صفحه | استایل صفحه‌ها از HTML جدا نشده |
| اسکریپت | `script.js` مشترک + اسکریپت درون‌صفحه‌ای | تابع‌های صفحات داخل HTML هستند |
| فایل‌های مرده | `assets/` (۳ فایل CSS) + `assets/Js/` (۳ فایل خالی) | **هیچ‌کدام استفاده نمی‌شوند** — `main.css` از یک قالب قدیمی «ARHA Portfolio» است |
| README | خالی | بدون مستندات |
| امنیت | فقط هانی‌پات ساده در فرم تماس | بدون Security Headers، اسکریپت‌های inline، `innerHTML` |
| سرعت | فونت از Google Fonts (رندر بلاکینگ) | بدون minify، بدون lazy loading |
| بک‌اند | ندارد — فرم‌ها فقط ظاهری | فرم تماس/خبرنامه دیتا را جایی ذخیره نمی‌کنند |
| پنل ادمین | `admin.html` UI نمایشی | دیتای هاردکد، بدون لاگین، به هیچ‌جا لینک نشده |

---

## 🗂️ فاز ۱ — ساختاردهی مجدد فرانت‌اند (بدون تغییر رفتار)

**هدف:** ساختار پوشه‌ای استاندارد + حذف تکرار و فایل‌های مرده.

### اقدامات:
1. **حذف فایل‌های مرده:**
   ```bash
   rm -r Nexify/assets          # هیچ صفحه‌ای از آن استفاده نمی‌کند
   ```
   > قبل از حذف، یک‌بار `grep -r "assets/" *.html` بزنید تا مطمئن شوید.

2. **ساختار پوشه‌ای جدید:**
   ```
   Nexify/
   ├── index.html  about.html  services.html  projects.html  blog.html  contact.html
   ├── admin.html                    # بعداً با پنل جنگو جایگزین می‌شود
   ├── css/
   │   ├── style.css                 # استایل مشترک (فعلی)
   │   ├── index.css                 # استایل‌های صفحه اصلی (خارج از <style>)
   │   ├── about.css
   │   ├── services.css
   │   ├── projects.css
   │   ├── blog.css
   │   └── contact.css
   ├── js/
   │   ├── main.js                   # اسکریپت مشترک (فعلی script.js)
   │   ├── theme.js  reveal.js  ...  # (اختیاری) ماژول‌سازی با ES Modules
   │   ├── index.js  projects.js  contact.js  ...
   ├── images/                       # تصاویر (بعداً)
   ├── fonts/                        # فونت self-host (فاز ۳)
   └── vendor/                       # کتابخانه‌های محلی (مثلاً lenis)
   ```

3. **جدا کردن `<style>` و `<script>` درون‌صفحه‌ای** به فایل‌های `css/<page>.css` و `js/<page>.js`.

4. **استانداردسازی:** افزودن `defer` به اسکریپت‌ها، حذف `onclick`های inline (سازگار با CSP در فاز ۲).

5. **مستندات:** نوشتن `README.md` کامل (نصب، ساختار، نحوه‌ی اجرا).

---

## 🔒 فاز ۲ — امنیت ✅ (انجام شد)

> وضعیت: موارد سمت فرانت‌اند انجام شد — مودال بدون innerHTML، هانی‌پات دوم، حذف event handler اینلاین، متای CSP در همه‌ی صفحات + فایل‌های هدر (`_headers` و `nginx-security.conf`).

### الف) امنیت سمت فرانت‌اند

| اقدام | جزئیات |
|-------|--------|
| **حذف `innerHTML` با داده‌ی کاربری** | در `projects.html` مودال با `innerHTML` ساخته می‌شود → جایگزینی با `textContent` یا `createElement` (آسیب‌پذیری XSS) |
| **حذف event handler های inline** | `onclick="..."` → `addEventListener` (برای سازگاری با CSP) |
| **هانی‌پات دوم در فرم تماس** | یک فیلد مخفی `website` اضافه کنید (فیلد فعلی `hiddenSelect` خوب است ولی با جنگو formal تر می‌شود) |
| **اعتبارسنجی سمت کلاینت** | `minlength`، `type="email"` وجود دارد ✓ — سمت سرور هم اضافه می‌شود |
| **`rel="noopener"`** | برای لینک‌های خارجی وجود دارد ✓ |
| **CSP آماده** | با حذف اسکریپت‌های inline، می‌توان CSP سخت‌گیرانه گذاشت |

### ب) امنیت سطح سرور (زمان دیپلوی)
این هدرها در **Nginx/Caddy/فایل `_headers`** تنظیم می‌شوند:

```nginx
# Nginx - بخش server
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'" always;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

### ج) امنیت بک‌اند (جنگو) — در فاز ۴

```python
# config/settings/production.py
DEBUG = False
ALLOWED_HOSTS = ['nexify.ir', 'www.nexify.ir']
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']        # فقط از env
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
CSRF_TRUSTED_ORIGINS = ['https://nexify.ir', 'https://www.nexify.ir']
# حتماً: python manage.py check --deploy
```

---

## ⚡ فاز ۳ — بهینه‌سازی سرعت

### اولویت‌بندی بر اساس Core Web Vitals (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1)

| # | اقدام | تأثیر |
|---|-------|-------|
| ۱ | **فونت self-host + متغیر** — دانلود **Vazirmatn Variable** (یک فایل woff2 برای همه‌ی وزن‌ها) و قراردادن در `fonts/` | حذف رندر بلاکینگ Google Fonts، کاهش حجم شدید |
| ۲ | **`font-display: swap` + preload** | رندر فوری متن با فونت جایگزین |
| ۳ | **Minify** — `npx esbuild css js --minify` یا اسکریپت npm ساده | کاهش ۳۰-۷۰٪ حجم |
| ۴ | **`defer` همه‌ی اسکریپت‌ها** (Lenis و فایل‌های خودی) | حذف render-blocking |
| ۵ | **Lazy loading** تصاویر پایین صفحه (`loading="lazy"` + `width`/`height` برای جلوگیری از CLS) | کاهش زمان اولیه |
| ۶ | **Preconnect** برای فونت‌ها (اگر CDN ماند) | کاهش تأخیر |
| ۷ | **Caching headers** — فایل‌های استاتیک: `Cache-Control: public, max-age=31536000, immutable` / HTML: `no-cache` | کاهش درخواست‌های تکراری |
| ۸ | **سنجش**: اجرای Lighthouse و PageSpeed Insights قبل/بعد هر مرحله | اثبات بهبود |

### اسکریپت build ساده (بدون وابستگی سنگین):
```json
// package.json
{
  "scripts": {
    "minify:css": "esbuild css/style.css --minify --outfile=css/style.min.css",
    "minify:js": "esbuild js/main.js --minify --outfile=js/main.min.js",
    "build": "npm run minify:css && npm run minify:js"
  }
}
```
> نکته: بعد از ورود به جنگو، minify را می‌توان به ابزارهای جنگو (مثل `django-compressor`) واگذار کرد.

---

## 🐍 فاز ۴ — یکپارچه‌سازی با جنگو ✅ (انجام شد)

> وضعیت: پروژه‌ی جنگو کامل راه‌اندازی شد — `config/` با settings سه‌تایی (base/development/production)، ۴ اپ (`core`, `projects`, `blog`, `contact`)، `base.html` + partials (حذف تکرار نوبار/فوتر)، تبدیل همه‌ی HTML ها به Template با `{% static %}`، مدل‌های `Project`/`BlogPost`/`ContactMessage`/`FAQ`، فرم تماس امن با CSRF و هانی‌پات سمت سرور (ربات ساکت رد می‌شود)، پنل `Django Admin` جایگزین `admin.html` شد، دستور `seed_demo` برای داده‌ی نمونه، فایل‌های `requirements*.txt`/`.env.example`/`.gitignore`، و HTML های قدیمی به `legacy/` بایگانی شدند.

## 🔐 فاز ۴.۶ — احراز هویت (ورود/ثبت‌نام) ✅ (انجام شد)

> وضعیت: اپ جدید `apps/accounts` اضافه شد — صفحات `/accounts/login/` و `/accounts/register/` با انیمیشن‌های سبک (اُرب‌های شناور، کارت شیشه‌ای، هاله‌ی دنبال‌کننده‌ی موس، متر قدرت رمز، eye toggle) + خروج فقط با POST (CSRF-safe). ورود با `LoginView` استاندارد جنگو (محافظت open-redirect، مدیریت امن `?next=`) و ثبت‌نام با هانی‌پات دولایه + ورود خودکار + `?next=` اعتبارسنجی‌شده. تمپلیت‌ها از partial های مشترک (`auth_background.html`، `auth_eye_toggle.html`) استفاده می‌کنند. نوبار/منوی موبایل با `{% if user.is_authenticated %}` شرطی شدند (مهمان → ورود/ثبت‌نام | واردشده → چیپ نام کاربری + خروج). ۱۹ تست pytest جدید → جمعاً ۵۸ تست.

### ۴.۱ — تفکر معماری

**روش انتخابی: Django Templates (رندر سمت سرور).** چون سایت چندصفحه‌ای دارید و محتوای داینامیک (بلاگ، پروژه‌ها، پیام‌ها) می‌خواهید، بهترین مسیر این است:

- هر `*.html` فعلی → یک **Django Template**
- `base.html` + `partials/` → حذف تکرار نوبار/فوتر
- `{% static %}` → مدیریت خودکار فایل‌های استاتیک (با هش فایل + CDN آماده)
- فرم تماس → **ModelForm جنگو** با CSRF و ذخیره در دیتابیس + ایمیل اطلاع‌رسانی

### ۴.۲ — نصب و راه‌اندازی

```bash
pip install django psycopg[binary] whitenoise django-environ gunicorn
django-admin startproject config .
python manage.py startapp core    # خانه، درباره، خدمات
python manage.py startapp blog    # مقالات
python manage.py startapp projects
python manage.py startapp contact # فرم تماس، FAQ
```

### ۴.۳ — ساختار نهایی پروژه (هدف نهایی)

```
nexify/                              # ← ریشه‌ی ریپو (بعد از ادغام)
├── manage.py
├── requirements.txt
├── .env.example                     # الگوی متغیرهای محیطی
├── .gitignore                       # .env، staticfiles/، db، __pycache__ و...
├── .dockerignore
├── Dockerfile
├── docker-compose.yml               # django + postgres + nginx
├── gunicorn.conf.py
├── entrypoint.sh
├── .github/workflows/
│   └── deploy.yml                   # CI/CD
│
├── config/                          # پیکربندی اصلی جنگو
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py              # انتخاب environment
│   │   ├── base.py                  # تنظیمات مشترک
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py                      # مسیر اصلی (include اپ‌ها)
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── core/
│   │   ├── models.py                # Skill, TimelineEvent, SiteStat, Service
│   │   ├── views.py                 # IndexView, AboutView, ServicesView
│   │   ├── urls.py
│   │   └── admin.py
│   ├── projects/
│   │   ├── models.py                # Project (title, category, tags, github_url, ...)
│   │   ├── views.py                 # ProjectsView (فیلتر دسته‌بندی از DB)
│   │   └── urls.py
│   ├── blog/
│   │   ├── models.py                # BlogPost (title, slug, category, excerpt, ...)
│   │   ├── views.py                 # BlogListView, BlogDetailView
│   │   └── urls.py
│   └── contact/
│       ├── models.py                # ContactMessage, FAQ
│       ├── forms.py                 # ContactForm (با honeypot + validation)
│       ├── views.py                 # ContactView (POST → ذخیره + ایمیل)
│       └── urls.py
│
├── templates/                       # ← HTMLهای فعلی اینجا تبدیل می‌شوند
│   ├── base.html                    # هدر + نوبار + فوتر + بلاک‌ها
│   ├── partials/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   ├── preloader.html
│   │   └── mobile_menu.html
│   ├── index.html
│   ├── about.html
│   ├── services.html
│   ├── projects.html
│   ├── blog/
│   │   ├── blog_list.html
│   │   └── blog_detail.html
│   └── contact.html
│
├── static/                          # ← css/js فعلی اینجا
│   ├── css/   (style.css + صفحه‌ای‌ها)
│   ├── js/    (main.js + صفحه‌ای‌ها)
│   ├── images/
│   └── fonts/ (Vazirmatn وواف)
│
├── media/                           # آپلود کاربر/ادمین (پروژه، بلاگ)
└── staticfiles/                     # خروجی collectstatic (gitignored)
```

### ۴.۴ — تبدیل HTML به Template (نمونه)

**`templates/base.html`:**
```html
{% load static %}
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Nexify | AI Solutions{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% include 'partials/preloader.html' %}
    {% include 'partials/navbar.html' %}

    <main>{% block content %}{% endblock %}</main>

    {% include 'partials/footer.html' %}
    <script src="{% static 'js/main.js' %}" defer></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**`templates/index.html`:**
```html
{% extends 'base.html' %}
{% load static %}
{% block title %}Nexify | AI Solutions{% endblock %}
{% block extra_css %}<link rel="stylesheet" href="{% static 'css/index.css' %}">{% endblock %}

{% block content %}
    <section class="hero"> ... آمار با حلقه: {% for stat in stats %} ... {% endfor %} ... </section>
{% endblock %}
```

### ۴.۵ — تنظیمات استاتیک و Whitenoise

```python
# config/settings/base.py
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← بعد از Security
    ...
]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
```

**نقشه‌ی دقیق هر فایل فعلی → مقصد جنگو:**

| فایل فعلی | تبدیل به | تغییرات |
|-----------|----------|---------|
| `index.html` | `templates/index.html` | دیتای آمار/خدمات → حلقه از Context جنگو |
| `about.html` | `templates/about.html` | مهارت‌ها/تایم‌لاین → حلقه از DB |
| `services.html` | `templates/services.html` | خدمات → حلقه از مدل `Service` |
| `projects.html` | `templates/projects.html` | پروژه‌ها + فیلتر → حلقه از مدل `Project`، دیتای مودال → DB |
| `blog.html` | `templates/blog/blog_list.html` | مقالات → لیست از مدل `BlogPost` |
| `contact.html` | `templates/contact.html` | فرم → `ContactForm` جنگو (CSRF + honeypot + ذخیره) |
| `admin.html` | حذف میشود | جایگزین: **Django Admin** سفارشی‌سازی‌شده (بخش ۴.۷) |
| `style.css` | `static/css/style.css` | بدون تغییر محتوا |
| `<style>` های صفحات | `static/css/<page>.css` | خارج از HTML |
| `script.js` | `static/js/main.js` | بدون تغییر |
| اسکریپت‌های صفحات | `static/js/<page>.js` | با `defer` |
| `assets/` مرده | حذف شد (فاز ۱) | — |

### ۴.۶ — مدل‌های پیشنهادی

```python
# apps/blog/models.py
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)          # آدرس سئو-دوست
    category = models.CharField(max_length=50)
    excerpt = models.TextField()
    content = models.TextField()                  # بدنه مقاله
    image = models.ImageField(upload_to='blog/', blank=True)
    read_time = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

# apps/contact/models.py
class ContactMessage(models.Model):
    REQUEST_TYPES = [...]                         # همان ۷ گزینه فرم تماس
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### ۴.۷ — فرم تماس امن با جنگو

```python
# apps/contact/forms.py
from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)  # هانی‌پات

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'request_type', 'subject', 'message']

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('website'):                # ربات فیلد مخفی را پر کرده
            raise forms.ValidationError('ارسال غیرمجاز')
        return cleaned
```

در ویو: ذخیره در DB + ارسال ایمیل با `send_mail` + محدودیت نرخ با `django-ratelimit`، و CSRF به‌صورت خودکار فعال است (`{% csrf_token %}` در فرم).

### ۴.۸ — پنل مدیریت
- `admin.html` فعلی **نمایشی** است → با **Django Admin** جایگزین می‌شود (`/admin/`) که رایگان: لاگین، CRUD، جستجو، فیلتر دارد.
- برای تم‌های حرفه‌تر: پکیج `django-jazzmin` یا `django-unfold` (پوسته‌ی مدرن فارسی).
- لاگین فقط با HTTPS و rate-limit (پکیج `django-axes` برای جلوگیری از brute-force).

---

## 🚀 فاز ۵ — دیپلوی و CI/CD

### گزینه‌های پیشنهادی (مرتب‌شده بر اساس سادگی)

| گزینه | مناسب برای | هزینه |
|-------|-----------|-------|
| **Docker + VPS** (Hetzner/DigitalOcean) | کنترل کامل، هزینه کم | ~۵-۱۰$/ماه |
| **Railway / Render** | سریع‌ترین راه‌اندازی | رایگان شروع |
| **Fly.io** | دیپلوی چندمنطقه | رایگان شروع |

### استک تولیدی استاندارد
```
Nginx (یا Caddy — SSL خودکار)  →  Gunicorn (4-5 worker)  →  Django  →  PostgreSQL
                                      │
                                      └─ Whitenoise (استاتیک) + S3/CDN (اختیاری بعداً)
```

### Docker Compose نمونه
```yaml
services:
  db:
    image: postgres:16-alpine
    env_file: .env
    volumes: [pgdata:/var/lib/postgresql/data]

  web:
    build: .
    env_file: .env
    depends_on: [db]
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    volumes: [static_volume:/app/staticfiles]

  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes: [static_volume:/static, ./nginx:/etc/nginx/conf.d:ro]
    depends_on: [web]
```

### Checklist دیپلوی (قبل از go-live)
- [ ] `DEBUG=False` و `python manage.py check --deploy` بدون خطا
- [ ] `SECRET_KEY` و همه‌ی رازها فقط در `.env` (هرگز در گیت)
- [ ] `collectstatic` و تست فایل‌های استاتیک
- [ ] HTTPS فعال + هدرهای امنیتی فاز ۲
- [ ] بکاپ خودکار دیتابیس (cron + pg_dump)
- [ ] CI/CD: روی `main` → تست (`pytest`) → lint (`ruff`) → دیپلوی
- [ ] مانیتورینگ: `django-sentry` + UptimeRobot

---

## ✅ جمع‌بندی و ترتیب پیشنهادی کار

| اولویت | فاز | زمان تخمینی | وابستگی |
|--------|-----|-------------|---------|
| ۱ | فاز ۱ — ساختاردهی فرانت‌اند | نیم روز | — |
| ۲ | فاز ۳ — سرعت (فونت، minify، defer) | نیم روز | فاز ۱ |
| ۳ | فاز ۲ — امنیت فرانت (CSP-ready) | چند ساعت | فاز ۱ |
| ۴ | فاز ۴ — مهاجرت به جنگو | ۲-۳ روز | فاز ۱، ۳ |
| ۵ | فاز ۵ — دیپلوی | ۱ روز | فاز ۴ |

> 💡 **پیشنهاد:** فاز ۱ را با فاز ۳ ترکیب کنید (هر دو روی ساختار استاتیک) و بلافاصله نتیجه را با Lighthouse بسنجید. سپس مستقیم به فاز ۴ بروید — بقیه‌ی بهینه‌سازی‌های امنیتی در سطح جنگو/سرور به‌صورت طبیعی در فاز ۴ و ۵ اعمال می‌شوند.

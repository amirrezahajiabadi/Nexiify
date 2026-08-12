# -*- coding: utf-8 -*-
"""
Nexify — میان‌افزارهای امنیتی
=============================
CSP صفحه‌های عادی از طریق <meta> در base.html ارسال می‌شود، اما Django Admin
از base.html استفاده نمی‌کند (تمپلیت اختصاصی خودش را دارد)؛ بنابراین این
میان‌افزار هدر Content-Security-Policy را فقط برای مسیرهای /admin/ اضافه می‌کند.

نکته: Django Admin اسکریپت‌های اینلاین دارد (change_form، popup_response و
prepopulated_fields_js)؛ به همین دلیل script-src شامل 'unsafe-inline' است.
در production نیز همین هدر از میان‌افزار می‌رسد و Nginx آن را بازنویسی نمی‌کند
(بلوک /admin/ در nginx-security.conf هدر CSP ندارد تا تداخل پیش نیاید).
"""

ADMIN_CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'"
)


class AdminSecurityHeadersMiddleware:
    """افزودن هدر CSP (و اطمینان از X-Frame-Options) برای پنل ادمین."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        if path == "/admin" or path.startswith("/admin/"):
            if "Content-Security-Policy" not in response:
                response["Content-Security-Policy"] = ADMIN_CSP
        return response


class NoStoreCacheMiddleware:
    """رفع باگ «محتوای حذف‌شده بعد از بستن/باز کردن سایت برمی‌گردد».

    سرور توسعه‌ی Django هیچ هدر Cache-Control نمی‌فرستد؛ در نتیجه مرورگر/وب‌ویو
    ممکن است صفحات داینامیک را به‌صورت heuristic کش کند و نسخه‌ی قدیمی (با
    محتوای حذف‌شده) را بعد از بستن/باز کردن سایت یا گذشت زمان نشان دهد — حتی
    وقتی دیتابیس درست است.

    این میان‌افزار برای همه‌ی پاسخ‌های داینامیک `Cache-Control: no-store`
    ست می‌کند (معادل استاندارد `never_cache` جنگو) تا مرورگر هر بار صفحه را
    تازه از سرور بگیرد. چون بعد از WhiteNoise در MIDDLEWARE قرار دارد، درخواست‌های
    استاتیک به اینجا نمی‌رسند و کش استاتیک WhiteNoise دست‌نخورده می‌ماند.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # استاتیک هرگز به اینجا نمی‌رسد (WhiteNoise زودتر intercept می‌کند) — فقط احتیاط:
        if request.path.startswith("/static/") or request.path.startswith("/media/"):
            return response
        response["Cache-Control"] = "no-store, max-age=0, must-revalidate"
        response["Pragma"] = "no-cache"
        return response


# مسیرهای داخلی که بازدیدشان ثبت نمی‌شود (پنل، ادمین، استاتیک، مدیا)
TRACKING_EXCLUDED_PREFIXES = (
    "/panel",
    "/admin",
    "/static/",
    "/media/",
    "/accounts/",
    "/favicon.ico",
    "/robots.txt",
)


class VisitTrackingMiddleware:
    """ثبت بازدید صفحات عمومی (GET موفق) در جدول PageView برای آمار داشبورد.

    همیشه fail-safe: هر خطایی در ثبت، بی‌صدا نادیده گرفته می‌شود تا
    هیچ‌وقت سایت را از کار نیندازد.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method != "GET" or response.status_code != 200:
            return response
        path = request.path
        if path.startswith(TRACKING_EXCLUDED_PREFIXES):
            return response
        try:
            from apps.panel.models import PageView

            PageView.objects.create(
                path=path,
                session_key=getattr(request.session, "session_key", None),
            )
        except Exception:  # pragma: no cover — هرگز نباید جریان اصلی را بشکند
            pass
        return response

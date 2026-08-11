"""
اعلان‌های خارجی سایت — ارسال پیام به تلگرام مالک (اختیاری).

تا وقتی `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` تنظیم نشده باشند، همه‌چیز
بی‌صدا غیرفعال است (بدون خطا و بدون درخواست شبکه). از urllib استاندارد
استفاده می‌شود تا وابستگی جدیدی به پروژه اضافه نشود.
"""
import http.client
import json
import logging
import urllib.error
import urllib.request
from html import escape

from django.conf import settings

logger = logging.getLogger(__name__)

# مقدارهای «تنظیم نشده» در settings → ارسال بی‌صدا غیرفعال می‌شود
_UNSET_VALUES = {"", "PASTE_BOT_TOKEN_HERE", "PASTE_CHAT_ID_HERE"}


def _notify_configured() -> bool:
    token = str(getattr(settings, "TELEGRAM_BOT_TOKEN", "") or "").strip()
    chat_id = str(getattr(settings, "TELEGRAM_CHAT_ID", "") or "").strip()
    return token not in _UNSET_VALUES and chat_id not in _UNSET_VALUES


def send_telegram_notify(text: str) -> bool:
    """ارسال متن به تلگرام — همیشه fail-silent؛ هیچ‌وقت جریان اصلی را نمی‌شکند."""
    if not _notify_configured() or not text:
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps(
        {
            "chat_id": str(settings.TELEGRAM_CHAT_ID),
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    request = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            status = response.status
    except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException) as exc:
        # خطای شبکه/API — بدون traceback کامل (هر بار ارسال با شکست، لاگ‌اسپم نشود)
        logger.warning("ارسال اعلان تلگرام ناموفق بود: %s", exc)
        return False
    if status != 200:
        logger.warning("تلگرام پاسخ غیرموفق داد: HTTP %s", status)
    return status == 200


def notify_contact_message(message) -> None:
    """اعلان پیام جدید از فرم تماس."""
    send_telegram_notify(
        "📩 <b>پیام جدید از سایت</b>\n"
        f"👤 نام: {escape(message.name)}\n"
        f"📧 ایمیل: {escape(message.email)}\n"
        f"📞 روش تماس: {escape(message.get_contact_method_display())}\n"
        f"☎️ تلفن: {escape(message.phone or '—')}\n"
        f"✈️ تلگرام: {escape(message.telegram_id or '—')}\n"
        f"🏷 نوع درخواست: {escape(message.get_request_type_display())}\n"
        f"📝 موضوع: {escape(message.subject or '—')}\n\n"
        f"💬 {escape(message.message)}"
    )


def notify_new_user(user, ip: str = "") -> None:
    """اعلان ثبت‌نام کاربر جدید."""
    send_telegram_notify(
        "🆕 <b>ثبت‌نام جدید در سایت</b>\n"
        f"👤 نام کاربری: {escape(user.username)}\n"
        f"📧 ایمیل: {escape(user.email or '—')}\n"
        f"🌐 IP: {escape(ip or '—')}"
    )

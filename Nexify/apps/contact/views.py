import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render

from apps.core.icons import build_icon
from apps.core.services import notify_contact_message

from .forms import ContactForm
from .models import ContactMessage, FAQ

logger = logging.getLogger(__name__)

# آیکون‌های نمایشی هر نوع درخواست (فقط UI) — کلیدهای نگاشت به SVG در apps/core/icons.py
REQUEST_TYPE_ICONS = {
    "consulting": "🧠",
    "web-design": "🌐",
    "app-development": "📱",
    "agent-ai": "🤖",
    "mlops": "⚙️",
    "education": "📚",
    "other": "💡",
}


def contact(request):
    faqs = FAQ.objects.filter(is_published=True)
    options = [
        {
            "value": value,
            "icon": REQUEST_TYPE_ICONS.get(value, "💡"),
            "icon_svg": build_icon(REQUEST_TYPE_ICONS.get(value, "💡")),
            "label": label,
        }
        for value, label in ContactMessage.REQUEST_TYPES
    ]
    context = {"faqs": faqs, "options": options}

    if request.method == "POST":
        form = ContactForm(request.POST)

        # هانی‌پات پر شده؟ → ساکت رد کن (ربات متوجه نمی‌شود؛ بدون خطا و بدون ذخیره)
        if request.POST.get("website"):
            context.update({"form": form, "success": True})
            return render(request, "contact.html", context)

        if form.is_valid():
            message = form.save()
            _notify_by_email(message)
            notify_contact_message(message)
            context.update({"form": ContactForm(), "success": True})
            return render(request, "contact.html", context)

        context["form"] = form
        return render(request, "contact.html", context)

    context["form"] = ContactForm()
    return render(request, "contact.html", context)


def _notify_by_email(message: ContactMessage) -> None:
    """ارسال ایمیل اطلاع‌رسانی — شکست آن هرگز نباید جریان اصلی را بشکند."""
    try:
        send_mail(
            subject=f"پیام جدید از سایت: {message.name} ({message.get_request_type_display()})",
            message=(
                f"نام: {message.name}\n"
                f"ایمیل: {message.email}\n"
                f"روش تماس: {message.get_contact_method_display()}\n"
                f"تلفن: {message.phone or '—'}\n"
                f"تلگرام: {message.telegram_id or '—'}\n"
                f"نوع درخواست: {message.get_request_type_display()}\n"
                f"موضوع: {message.subject or '—'}\n\n"
                f"متن پیام:\n{message.message}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
            fail_silently=True,
        )
    except Exception:  # noqa: BLE001
        logger.exception("ارسال ایمیل اطلاع‌رسانی ناموفق بود")

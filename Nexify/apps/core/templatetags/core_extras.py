"""تگ‌های تمپلیت مشترک اپ core."""

from django import template
from django.utils.safestring import mark_safe

from ..icons import build_icon

register = template.Library()


@register.filter
def icon_svg(value, class_name=""):
    """ایموجی/کلید آیکون را به SVG استروک‌محور تبدیل می‌کند (فاز U2).

    استفاده:
        {% load core_extras %}
        {{ "📞"|icon_svg }}          → <svg class="icon-svg" ...>
        {{ post.icon|icon_svg }}     → برای آیکون دیتابیس
        {{ "💬"|icon_svg:"big" }}    → کلاس اضافه روی svg

    خروجی mark_safe است (SVG تولیدی خود پروژه — نه داده‌ی کاربر) تا escape نشود.
    """
    return mark_safe(build_icon(value, class_name))


@register.filter
def stars(value, max_stars=5):
    """امتیاز (۱ تا ۵) را به ردیف ستاره‌ی SVG تبدیل می‌کند (فاز U5).

    استفاده:
        {{ t.rating|stars }}   → <span class="testimonial-stars" role="img" aria-label="امتیاز ۵ از ۵">
                                     <svg class="icon-svg star-on" fill="currentColor">...</svg> ×۵
                                 </span>

    ستاره‌های پُر با fill=currentColor و ستاره‌های خالی با opacity کم (CSS) نمایش داده می‌شوند.
    """
    try:
        n = min(max(int(value), 0), int(max_stars))
    except (TypeError, ValueError):
        n = 0
    filled = build_icon("⭐", "star-on", filled=True) * n
    empty = build_icon("☆", "star-off") * (int(max_stars) - n)
    label = f"امتیاز {n} از {max_stars}"
    return mark_safe(
        f'<span class="testimonial-stars" role="img" aria-label="{label}">'
        f"{filled}{empty}</span>"
    )


@register.filter
def fa_num(value):
    """ارقام انگلیسی را به فارسی تبدیل می‌کند: ۱۵ → ۱۵. برای آمار و اعداد نمایشی."""
    try:
        return str(int(value)).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
    except (TypeError, ValueError):
        return value

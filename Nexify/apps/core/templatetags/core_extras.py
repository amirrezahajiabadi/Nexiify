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

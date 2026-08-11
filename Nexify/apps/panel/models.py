# -*- coding: utf-8 -*-
"""مدل‌های پنل ادمین — متن‌های قابل ویرایش سایت."""

from django.db import models


class SiteSetting(models.Model):
    """متن/مقدار قابل ویرایش سایت (هیرو، CTA، ایمیل تماس و...)."""

    GROUP_HOME = "home"
    GROUP_CONTACT = "contact"
    GROUP_ABOUT = "about"
    GROUP_OTHER = "other"

    GROUP_CHOICES = [
        (GROUP_HOME, "صفحه اصلی"),
        (GROUP_CONTACT, "تماس"),
        (GROUP_ABOUT, "درباره ما"),
        (GROUP_OTHER, "سایر"),
    ]

    key = models.SlugField(unique=True, verbose_name="کلید (شناسه)")
    label = models.CharField(max_length=100, verbose_name="عنوان نمایشی")
    value = models.TextField(blank=True, verbose_name="مقدار")
    group = models.CharField(
        max_length=20, choices=GROUP_CHOICES, default=GROUP_OTHER,
        verbose_name="گروه",
    )
    is_textarea = models.BooleanField(
        default=False, verbose_name="چندخطی (textarea)",
        help_text="برای متن‌های طولانی مثل توضیحات",
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        verbose_name = "متن سایت"
        verbose_name_plural = "متن‌های سایت"
        ordering = ["group", "key"]

    def __str__(self):
        return f"{self.label} ({self.key})"


class PageView(models.Model):
    """یک بازدید از یک صفحه‌ی عمومی سایت — برای آمار داشبورد.

    توسط VisitTrackingMiddleware (config/middleware.py) ثبت می‌شود.
    مسیرهای داخلی (/panel/، /admin/، /static/، /media/) ثبت نمی‌شوند.
    """

    path = models.CharField(max_length=255, verbose_name="مسیر")
    session_key = models.CharField(
        max_length=40, blank=True, null=True, verbose_name="کلید نشست"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان بازدید")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "بازدید"
        verbose_name_plural = "بازدیدها"

    def __str__(self):
        return f"{self.path} — {self.created_at:%Y/%m/%d %H:%M}"

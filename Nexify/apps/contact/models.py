from django.db import models


class ContactMessage(models.Model):
    """پیام ارسالی از فرم تماس — در ادمین جنگو مدیریت می‌شود."""

    REQUEST_TYPES = [
        ("consulting", "مشاوره رایگان"),
        ("web-design", "طراحی سایت"),
        ("app-development", "طراحی اپلیکیشن"),
        ("agent-ai", "ساخت Agent AI"),
        ("mlops", "MLOps و استقرار مدل"),
        ("education", "آموزش"),
        ("other", "سایر موارد"),
    ]

    # روش تماس ترجیحی کاربر — یا تلفنی، یا تلگرام (یکی را انتخاب می‌کند)
    CONTACT_METHODS = [
        ("phone", "تماس تلفنی"),
        ("telegram", "تلگرام"),
    ]

    # وضعیت پیگیری سفارش/درخواست — از پنل ادمین مدیریت می‌شود
    STATUSES = [
        ("new", "جدید"),
        ("in_progress", "در حال بررسی"),
        ("done", "انجام شده"),
    ]

    name = models.CharField(max_length=100, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    status = models.CharField(
        max_length=20, choices=STATUSES, default="new", verbose_name="وضعیت پیگیری"
    )
    contact_method = models.CharField(
        max_length=10,
        choices=CONTACT_METHODS,
        default="phone",
        verbose_name="روش تماس",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="شماره تماس")
    telegram_id = models.CharField(
        max_length=64, blank=True, verbose_name="آیدی تلگرام"
    )
    request_type = models.CharField(
        max_length=20, choices=REQUEST_TYPES, verbose_name="نوع درخواست"
    )
    subject = models.CharField(max_length=200, blank=True, verbose_name="موضوع")
    message = models.TextField(verbose_name="توضیحات")
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"

    def __str__(self):
        return f"{self.name} — {self.get_request_type_display()}"


class FAQ(models.Model):
    """سوال متداول — لیست FAQ صفحه‌ی تماس."""

    question = models.CharField(max_length=250, verbose_name="سوال")
    answer = models.TextField(verbose_name="پاسخ")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="ترتیب")
    is_published = models.BooleanField(default=True, verbose_name="نمایش در سایت")

    class Meta:
        ordering = ["order"]
        verbose_name = "سوال متداول"
        verbose_name_plural = "سوالات متداول"

    def __str__(self):
        return self.question

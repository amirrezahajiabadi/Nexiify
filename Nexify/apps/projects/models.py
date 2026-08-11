from django.db import models


class Project(models.Model):
    """پروژه‌ی نمونه — دیتای کارت‌ها و مودال جزئیات از همین مدل می‌آید."""

    title = models.CharField(max_length=120, verbose_name="عنوان")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="شماره نمایش")
    icon = models.CharField(max_length=8, default="🌐", verbose_name="آیکون")
    cover_image = models.ImageField(
        upload_to="project_covers/", blank=True, null=True,
        verbose_name="تصویر شاخص",
        help_text="تصویر کارت و مودال (اختیاری — اگر نباشد گرادیان نمایش داده می‌شود)",
    )
    categories = models.CharField(
        max_length=50,
        default="web",
        verbose_name="کلیدهای فیلتر",
        help_text="کلیدها با فاصله جدا می‌شوند، مثل: web ai",
    )
    category_label = models.CharField(max_length=50, verbose_name="برچسب دسته")
    short_description = models.CharField(max_length=250, verbose_name="توضیح کوتاه کارت")
    description = models.TextField(blank=True, verbose_name="توضیح کامل مودال")
    tags = models.JSONField(default=list, blank=True, verbose_name="تکنولوژی‌ها")
    duration = models.CharField(max_length=50, blank=True, verbose_name="زمان اجرا")
    role = models.CharField(max_length=50, blank=True, verbose_name="نقش")
    status = models.CharField(max_length=50, blank=True, verbose_name="وضعیت")
    github_url = models.URLField(blank=True, verbose_name="لینک GitHub")
    gradient = models.CharField(
        max_length=120, default="135deg,#1e1b4b,#7c3aed", verbose_name="گرادیان پس‌زمینه"
    )
    is_published = models.BooleanField(default=True, verbose_name="نمایش در سایت")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه‌ها"

    def __str__(self):
        return f"Project-{self.order} | {self.title}"

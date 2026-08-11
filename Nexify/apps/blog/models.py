from django.db import models


class BlogPost(models.Model):
    """مقاله‌ی بلاگ — لیست و صفحه‌ی جزئیات از همین مدل ساخته می‌شود."""

    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(unique=True, verbose_name="اسلاگ (آدرس سئو-دوست)")
    category = models.CharField(max_length=50, verbose_name="دسته")
    icon = models.CharField(max_length=8, default="📝", verbose_name="آیکون")
    gradient = models.CharField(
        max_length=120, default="135deg,#1e3a5f,#2563eb", verbose_name="گرادیان پس‌زمینه"
    )
    cover_image = models.ImageField(
        upload_to="blog_covers/", blank=True, null=True,
        verbose_name="تصویر شاخص",
        help_text="تصویر سربرگ مقاله (اختیاری — اگر نباشد گرادیان نمایش داده می‌شود)",
    )
    excerpt = models.TextField(verbose_name="خلاصه")
    content = models.TextField(blank=True, verbose_name="متن کامل")
    read_time = models.PositiveSmallIntegerField(default=5, verbose_name="زمان مطالعه (دقیقه)")
    published_at = models.DateField(verbose_name="تاریخ انتشار")
    is_published = models.BooleanField(default=False, verbose_name="منتشر شده")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "read_time", "is_published")
    list_editable = ("is_published",)
    list_filter = ("category", "is_published", "published_at")
    search_fields = ("title", "category", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"

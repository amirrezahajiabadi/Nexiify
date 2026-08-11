from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "category_label", "categories", "status", "is_published")
    list_editable = ("is_published",)
    list_filter = ("categories", "status", "is_published")
    search_fields = ("title", "category_label", "tags")
    ordering = ("order",)

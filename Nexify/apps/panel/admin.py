# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import PageView, SiteSetting, Testimonial


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "group", "is_active")
    list_filter = ("group", "is_active")
    search_fields = ("key", "label", "value")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "rating", "order", "is_published")
    list_filter = ("is_published", "rating")
    search_fields = ("name", "company", "text")
    list_editable = ("order", "is_published")


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ("path", "session_key", "created_at")
    list_filter = ("created_at",)
    search_fields = ("path",)
    date_hierarchy = "created_at"
    readonly_fields = ("path", "session_key", "created_at")

    def has_add_permission(self, request):
        return False  # فقط توسط middleware ثبت می‌شود

    def has_change_permission(self, request, obj=None):
        return False  # فقط خواندنی

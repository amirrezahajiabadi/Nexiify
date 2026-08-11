from django.contrib import admin

from .models import ContactMessage, FAQ


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "contact_method",
        "phone",
        "telegram_id",
        "request_type",
        "is_read",
        "created_at",
    )
    list_editable = ("is_read",)
    list_filter = ("request_type", "contact_method", "is_read", "created_at")
    search_fields = ("name", "email", "phone", "telegram_id", "subject", "message")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)

    def has_add_permission(self, request):
        # پیام‌ها فقط از فرم سایت ساخته می‌شوند، نه از ادمین
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "is_published")
    list_editable = ("order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("question", "answer")

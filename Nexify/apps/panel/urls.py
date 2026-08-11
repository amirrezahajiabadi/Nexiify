# -*- coding: utf-8 -*-
"""مسیرهای پنل ادمین — همه زیر /panel/."""

from django.urls import path

from . import views

app_name = "panel"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    # مقالات
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/new/", views.blog_edit, name="blog_new"),
    path("blog/<int:pk>/", views.blog_edit, name="blog_edit"),
    path("blog/<int:pk>/toggle/", views.blog_toggle, name="blog_toggle"),
    path("blog/<int:pk>/delete/", views.blog_delete, name="blog_delete"),

    # پروژه‌ها
    path("projects/", views.project_list, name="project_list"),
    path("projects/new/", views.project_edit, name="project_new"),
    path("projects/<int:pk>/", views.project_edit, name="project_edit"),
    path("projects/<int:pk>/toggle/", views.project_toggle, name="project_toggle"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),

    # پیام‌ها / سفارش‌ها
    path("messages/", views.message_list, name="message_list"),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("messages/<int:pk>/status/<str:status>/", views.message_status, name="message_status"),
    path("messages/<int:pk>/delete/", views.message_delete, name="message_delete"),

    # سوالات متداول
    path("faq/", views.faq_list, name="faq_list"),
    path("faq/new/", views.faq_edit, name="faq_new"),
    path("faq/<int:pk>/", views.faq_edit, name="faq_edit"),
    path("faq/<int:pk>/toggle/", views.faq_toggle, name="faq_toggle"),
    path("faq/<int:pk>/delete/", views.faq_delete, name="faq_delete"),

    # متن‌های سایت
    path("settings/", views.setting_list, name="setting_list"),
    path("settings/new/", views.setting_add, name="setting_add"),
    path("settings/<int:pk>/", views.setting_edit, name="setting_edit"),
    path("settings/<int:pk>/delete/", views.setting_delete, name="setting_delete"),

    # کاربران (چند ادمین)
    path("users/", views.user_list, name="user_list"),
    path("users/<int:pk>/toggle-staff/", views.user_toggle_staff, name="user_toggle_staff"),
]

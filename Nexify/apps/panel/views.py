# -*- coding: utf-8 -*-
"""ویوهای پنل ادمین — دسترسی فقط برای کارکنان (staff)."""

from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from apps.blog.models import BlogPost
from apps.contact.models import ContactMessage, FAQ
from apps.projects.models import Project

from .forms import BlogPostForm, FAQForm, ProjectForm, SiteSettingForm
from .models import PageView, SiteSetting

LOGIN_URL = "accounts:login"


# ---------------------------------------------------------------- داشبورد
@staff_member_required(login_url=LOGIN_URL)
def dashboard(request):
    # ---------- آمار بازدید ----------
    today = timezone.localdate()
    start_today = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    views = PageView.objects
    visit_total = views.count()
    visit_today = views.filter(created_at__gte=start_today).count()
    visit_week = views.filter(created_at__gte=start_today - timedelta(days=7)).count()
    visit_month = views.filter(created_at__gte=start_today - timedelta(days=30)).count()
    visitors_today = (
        views.filter(created_at__gte=start_today)
        .exclude(session_key__isnull=True)
        .values("session_key")
        .distinct()
        .count()
    )

    # ۱۴ روز اخیر — پر کردن روزهای بدون بازدید با صفر
    start_14 = start_today - timedelta(days=13)
    rows = (
        views.filter(created_at__gte=start_14)
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(c=Count("id"))
    )
    count_by_day = {r["day"]: r["c"] for r in rows}
    visit_chart = [
        {
            "day": today - timedelta(days=i),
            "count": count_by_day.get(today - timedelta(days=i), 0),
        }
        for i in range(13, -1, -1)
    ]
    chart_max = max((c["count"] for c in visit_chart), default=0) or 1
    for c in visit_chart:
        c["percent"] = round(c["count"] * 100 / chart_max)

    top_pages = list(views.values("path").annotate(c=Count("id")).order_by("-c")[:5])

    ctx = {
        "blog_count": BlogPost.objects.count(),
        "blog_published": BlogPost.objects.filter(is_published=True).count(),
        "project_count": Project.objects.count(),
        "project_published": Project.objects.filter(is_published=True).count(),
        "message_new": ContactMessage.objects.filter(status="new").count(),
        "message_total": ContactMessage.objects.count(),
        "user_count": User.objects.count(),
        "user_staff": User.objects.filter(is_staff=True).count(),
        "recent_messages": ContactMessage.objects.all()[:5],
        "recent_posts": BlogPost.objects.all()[:5],
        # بازدیدها
        "visit_total": visit_total,
        "visit_today": visit_today,
        "visit_week": visit_week,
        "visit_month": visit_month,
        "visitors_today": visitors_today,
        "visit_chart": visit_chart,
        "visit_chart_max": chart_max,
        "top_pages": top_pages,
    }
    return render(request, "panel/dashboard.html", ctx)


# ---------------------------------------------------------------- مقالات
@staff_member_required(login_url=LOGIN_URL)
def blog_list(request):
    q = request.GET.get("q", "").strip()
    posts = BlogPost.objects.all()
    if q:
        posts = posts.filter(
            Q(title__icontains=q) | Q(category__icontains=q) | Q(slug__icontains=q)
        )
    ctx = {"posts": posts, "q": q}
    return render(request, "panel/blog_list.html", ctx)


@staff_member_required(login_url=LOGIN_URL)
def blog_edit(request, pk=None):
    post = get_object_or_404(BlogPost, pk=pk) if pk else None
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "مقاله ذخیره شد.")
        return redirect("panel:blog_list")
    ctx = {"form": form, "post": post, "title": "ویرایش مقاله" if post else "مقاله جدید"}
    return render(request, "panel/blog_form.html", ctx)


@staff_member_required(login_url=LOGIN_URL)
def blog_toggle(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    post.is_published = not post.is_published
    post.save(update_fields=["is_published"])
    state = "منتشر شد" if post.is_published else "از انتشار خارج شد"
    messages.success(request, f"مقاله «{post.title}» {state}.")
    return redirect("panel:blog_list")


@staff_member_required(login_url=LOGIN_URL)
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "مقاله حذف شد.")
    return redirect("panel:blog_list")


# ---------------------------------------------------------------- پروژه‌ها
@staff_member_required(login_url=LOGIN_URL)
def project_list(request):
    q = request.GET.get("q", "").strip()
    projects = Project.objects.all()
    if q:
        projects = projects.filter(
            Q(title__icontains=q) | Q(category_label__icontains=q)
        )
    ctx = {"projects": projects, "q": q}
    return render(request, "panel/project_list.html", ctx)


@staff_member_required(login_url=LOGIN_URL)
def project_edit(request, pk=None):
    project = get_object_or_404(Project, pk=pk) if pk else None
    form = ProjectForm(request.POST or None, request.FILES or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "پروژه ذخیره شد.")
        return redirect("panel:project_list")
    ctx = {
        "form": form,
        "project": project,
        "title": "ویرایش پروژه" if project else "پروژه جدید",
    }
    return render(request, "panel/project_form.html", ctx)


@staff_member_required(login_url=LOGIN_URL)
def project_toggle(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.is_published = not project.is_published
    project.save(update_fields=["is_published"])
    state = "نمایش داده شد" if project.is_published else "از نمایش خارج شد"
    messages.success(request, f"پروژه «{project.title}» {state}.")
    return redirect("panel:project_list")


@staff_member_required(login_url=LOGIN_URL)
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request, "پروژه حذف شد.")
    return redirect("panel:project_list")


# ------------------------------------------------- پیام‌ها / سفارش‌ها
@staff_member_required(login_url=LOGIN_URL)
def message_list(request):
    status = request.GET.get("status", "")
    messages_qs = ContactMessage.objects.all()
    if status in dict(ContactMessage.STATUSES):
        messages_qs = messages_qs.filter(status=status)
    ctx = {
        "msgs": messages_qs,
        "status": status,
        "statuses": ContactMessage.STATUSES,
        "counts": {
            s[0]: ContactMessage.objects.filter(status=s[0]).count()
            for s in ContactMessage.STATUSES
        },
    }
    return render(request, "panel/message_list.html", ctx)


@staff_member_required(login_url=LOGIN_URL)
def message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=["is_read"])
    return render(request, "panel/message_detail.html", {"msg": msg})


@staff_member_required(login_url=LOGIN_URL)
def message_status(request, pk, status):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if status in dict(ContactMessage.STATUSES):
        msg.status = status
        msg.save(update_fields=["status"])
        messages.success(request, "وضعیت درخواست به‌روز شد.")
    return redirect(request.GET.get("next") or "panel:message_list")


@staff_member_required(login_url=LOGIN_URL)
def message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        msg.delete()
        messages.success(request, "درخواست حذف شد.")
    return redirect("panel:message_list")


# ---------------------------------------------------------------- سوالات متداول
@staff_member_required(login_url=LOGIN_URL)
def faq_list(request):
    faqs = FAQ.objects.all()
    return render(request, "panel/faq_list.html", {"faqs": faqs})


@staff_member_required(login_url=LOGIN_URL)
def faq_edit(request, pk=None):
    faq = get_object_or_404(FAQ, pk=pk) if pk else None
    form = FAQForm(request.POST or None, instance=faq)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "سوال متداول ذخیره شد.")
        return redirect("panel:faq_list")
    ctx = {"form": form, "faq": faq, "title": "ویرایش سوال" if faq else "سوال جدید"}
    return render(request, "panel/faq_form.html", ctx)


@staff_member_required(login_url=LOGIN_URL)
def faq_toggle(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    faq.is_published = not faq.is_published
    faq.save(update_fields=["is_published"])
    messages.success(request, "وضعیت سوال به‌روز شد.")
    return redirect("panel:faq_list")


@staff_member_required(login_url=LOGIN_URL)
def faq_delete(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == "POST":
        faq.delete()
        messages.success(request, "سوال حذف شد.")
    return redirect("panel:faq_list")


# -------------------------------------------------------- متن‌های سایت
@staff_member_required(login_url=LOGIN_URL)
def setting_list(request):
    group = request.GET.get("group", "")
    settings = SiteSetting.objects.all()
    if group:
        settings = settings.filter(group=group)
    ctx = {
        "settings": settings,
        "group": group,
        "groups": SiteSetting.GROUP_CHOICES,
    }
    return render(request, "panel/setting_list.html", ctx)


@staff_member_required(login_url=LOGIN_URL)
def setting_add(request):
    form = SiteSettingForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "متن جدید اضافه شد.")
        return redirect("panel:setting_list")
    return render(request, "panel/setting_form.html", {"form": form, "title": "متن جدید"})


@staff_member_required(login_url=LOGIN_URL)
def setting_edit(request, pk):
    setting = get_object_or_404(SiteSetting, pk=pk)
    form = SiteSettingForm(request.POST or None, instance=setting)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "متن ذخیره شد.")
        return redirect("panel:setting_list")
    return render(
        request, "panel/setting_form.html", {"form": form, "title": "ویرایش متن"}
    )


@staff_member_required(login_url=LOGIN_URL)
def setting_delete(request, pk):
    setting = get_object_or_404(SiteSetting, pk=pk)
    if request.method == "POST":
        setting.delete()
        messages.success(request, "متن حذف شد.")
    return redirect("panel:setting_list")


# ---------------------------------------------------------------- کاربران
@staff_member_required(login_url=LOGIN_URL)
def user_list(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "panel/user_list.html", {"users": users})


@staff_member_required(login_url=LOGIN_URL)
def user_toggle_staff(request, pk):
    # فقط سوپریوزر می‌تواند دسترسی ادمین بدهد/بگیرد
    if not request.user.is_superuser:
        messages.error(request, "فقط مدیر اصلی می‌تواند دسترسی ادمین را تغییر دهد.")
        return redirect("panel:user_list")
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, "نمی‌توانید دسترسی خودتان را بردارید.")
        return redirect("panel:user_list")
    if request.method == "POST":
        user.is_staff = not user.is_staff
        user.save(update_fields=["is_staff"])
        state = "ادمین شد" if user.is_staff else "از ادمین‌ها حذف شد"
        messages.success(request, f"{user.get_full_name() or user.username} {state}.")
    return redirect("panel:user_list")

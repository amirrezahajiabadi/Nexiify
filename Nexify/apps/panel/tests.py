# -*- coding: utf-8 -*-
"""تست‌های پنل ادمین — دسترسی، داشبورد، CRUD مقاله/پروژه/FAQ، متن‌های سایت و چند ادمین."""

import io

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from PIL import Image

from apps.blog.models import BlogPost
from apps.contact.models import ContactMessage, FAQ
from apps.projects.models import Project
from .models import PageView, SiteSetting, Testimonial


def make_admin(username="admin"):
    return User.objects.create_superuser(username=username, email=f"{username}@x.com", password="pass")


def make_user(username="user"):
    return User.objects.create_user(username=username, email=f"{username}@x.com", password="pass")


def make_setting(key="hero_title_1", value="ساخت و توسعه"):
    return SiteSetting.objects.create(key=key, label="عنوان هیرو", value=value, group="home")


@pytest.fixture
def client_admin(client):
    client.force_login(make_admin())
    return client


# ===========================================================================
# دسترسی — فقط کارکنان (staff)
# ===========================================================================

@pytest.mark.django_db
def test_panel_redirects_anonymous_to_login(client):
    for url in [
        reverse("panel:dashboard"),
        reverse("panel:blog_list"),
        reverse("panel:message_list"),
        reverse("panel:setting_list"),
        reverse("panel:user_list"),
    ]:
        r = client.get(url)
        assert r.status_code == 302
        assert "/accounts/login/" in r.url


@pytest.mark.django_db
def test_panel_blocks_regular_user(client):
    client.force_login(make_user())
    for url in [
        reverse("panel:dashboard"),
        reverse("panel:blog_list"),
        reverse("panel:setting_list"),
        reverse("panel:user_list"),
    ]:
        r = client.get(url)
        assert r.status_code == 302  # به صفحه‌ی ورود برمی‌گردد


@pytest.mark.django_db
def test_dashboard_ok(client_admin):
    r = client_admin.get(reverse("panel:dashboard"))
    assert r.status_code == 200
    assert "داشبورد" in r.content.decode("utf-8")


# ===========================================================================
# مقالات — انتشار از پنل
# ===========================================================================

@pytest.mark.django_db
def test_blog_list_and_create(client_admin):
    url = reverse("panel:blog_list")
    assert client_admin.get(url).status_code == 200

    r = client_admin.post(
        reverse("panel:blog_new"),
        {
            "title": "مقاله از پنل",
            "slug": "post-from-panel",
            "category": "آموزش",
            "icon": "📝",
            "gradient": "135deg,#1e3a5f,#2563eb",
            "excerpt": "خلاصه",
            "content": "متن کامل",
            "read_time": 4,
            "published_at": "2026-08-09",
            "is_published": "on",
        },
    )
    assert r.status_code == 302
    post = BlogPost.objects.get(slug="post-from-panel")
    assert post.is_published is True


@pytest.mark.django_db
def test_blog_toggle_publish(client_admin):
    post = BlogPost.objects.create(
        title="تست", slug="t1", category="آموزش", excerpt="x", published_at="2026-08-09"
    )
    r = client_admin.post(reverse("panel:blog_toggle", args=[post.pk]))
    assert r.status_code == 302
    post.refresh_from_db()
    assert post.is_published is True


# ===========================================================================
# پروژه‌ها / محصولات
# ===========================================================================

def make_png(color=(124, 58, 237)):
    """یک تصویر PNG کوچک و معتبر برای تست آپلود."""
    buf = io.BytesIO()
    Image.new("RGB", (8, 8), color).save(buf, format="PNG")
    return buf.getvalue()


@pytest.mark.django_db
@override_settings(MEDIA_ROOT="media-test")
def test_blog_cover_image_upload_and_display(client_admin):
    """آپلود تصویر شاخص مقاله از پنل → نمایش در لیست و صفحه‌ی جزئیات."""
    r = client_admin.post(
        reverse("panel:blog_new"),
        {
            "title": "مقاله با تصویر",
            "slug": "post-with-cover",
            "category": "آموزش",
            "icon": "📝",
            "gradient": "135deg,#1e3a5f,#2563eb",
            "cover_image": SimpleUploadedFile("cover.png", make_png(), content_type="image/png"),
            "excerpt": "خلاصه",
            "content": "متن",
            "read_time": 3,
            "published_at": "2026-08-09",
            "is_published": "on",
        },
    )
    assert r.status_code == 302
    post = BlogPost.objects.get(slug="post-with-cover")
    assert post.cover_image

    detail = client_admin.get(reverse("blog:detail", args=[post.slug])).content.decode("utf-8")
    assert post.cover_image.url in detail
    assert "blog-image-photo" in detail

    lst = client_admin.get(reverse("blog:list")).content.decode("utf-8")
    assert post.cover_image.url in lst


@pytest.mark.django_db
@override_settings(MEDIA_ROOT="media-test")
def test_project_cover_image_upload(client_admin):
    """آپلود تصویر شاخص پروژه → data-cover در صفحه‌ی نمونه‌کارها (برای مودال)."""
    r = client_admin.post(
        reverse("panel:project_new"),
        {
            "title": "پروژه با تصویر", "order": 1, "icon": "🌐", "categories": "web",
            "category_label": "وب", "short_description": "توضیح", "description": "",
            "tags": "django", "duration": "", "role": "", "status": "",
            "github_url": "", "gradient": "135deg,#1e3a5f,#2563eb", "is_published": "on",
            "cover_image": SimpleUploadedFile("pcover.png", make_png((59, 130, 246)), content_type="image/png"),
        },
    )
    assert r.status_code == 302
    project = Project.objects.get(title="پروژه با تصویر")
    assert project.cover_image

    page = client_admin.get(reverse("projects:list")).content.decode("utf-8")
    assert f'data-cover="{project.cover_image.url}"' in page
    assert "project-visual-photo" in page


@pytest.mark.django_db
def test_project_create_and_delete(client_admin):
    r = client_admin.post(
        reverse("panel:project_new"),
        {
            "title": "پروژه از پنل",
            "order": 1,
            "icon": "🌐",
            "categories": "وب",
            "category_label": "وب",
            "short_description": "توضیح",
            "description": "توضیح کامل",
            "tags": "django, ai",
            "duration": "۲ هفته",
            "role": "توسعه‌دهنده",
            "status": "انجام شده",
            "github_url": "",
            "gradient": "135deg,#1e3a5f,#2563eb",
            "is_published": "on",
        },
    )
    assert r.status_code == 302
    p = Project.objects.get(title="پروژه از پنل")
    assert p.is_published is True

    r = client_admin.post(reverse("panel:project_delete", args=[p.pk]))
    assert r.status_code == 302
    assert not Project.objects.filter(pk=p.pk).exists()


# ===========================================================================
# سفارش‌ها / پیام‌ها
# ===========================================================================

@pytest.mark.django_db
def test_message_list_detail_and_status(client_admin):
    msg = ContactMessage.objects.create(
        name="علی", email="a@x.com", request_type="web-design",
        subject="س", message="متن پیام", contact_method="phone", phone="09123456789",
    )
    assert client_admin.get(reverse("panel:message_list")).status_code == 200
    assert client_admin.get(reverse("panel:message_detail", args=[msg.pk])).status_code == 200

    r = client_admin.post(reverse("panel:message_status", args=[msg.pk, "done"]))
    assert r.status_code == 302
    msg.refresh_from_db()
    assert msg.status == "done"


# ===========================================================================
# سوالات متداول
# ===========================================================================

@pytest.mark.django_db
def test_faq_create(client_admin):
    r = client_admin.post(
        reverse("panel:faq_new"),
        {"question": "سوال؟", "answer": "پاسخ", "order": 1, "is_published": "on"},
    )
    assert r.status_code == 302
    assert FAQ.objects.filter(question="سوال؟").exists()


# ===========================================================================
# نظرات مشتریان (سکشن Social Proof — فاز U5)
# ===========================================================================

@pytest.mark.django_db
def test_testimonial_crud(client_admin):
    # ساخت
    r = client_admin.post(
        reverse("panel:testimonial_new"),
        {
            "name": "علی محمدی",
            "company": "فروشگاه آنلاین",
            "text": "همکاری فوق‌العاده‌ای بود.",
            "rating": 5,
            "order": 1,
            "is_published": "on",
        },
    )
    assert r.status_code == 302
    t = Testimonial.objects.get(name="علی محمدی")
    assert t.rating == 5

    # لیست + ویرایش
    assert client_admin.get(reverse("panel:testimonial_list")).status_code == 200
    r = client_admin.post(
        reverse("panel:testimonial_edit", args=[t.pk]),
        {
            "name": t.name,
            "company": "فروشگاه آنلاین ۲",
            "text": t.text,
            "rating": 4,
            "order": 2,
            "is_published": "",
        },
    )
    assert r.status_code == 302
    t.refresh_from_db()
    assert t.company == "فروشگاه آنلاین ۲"
    assert t.rating == 4
    assert t.is_published is False

    # toggle (مخفی → نمایش)
    client_admin.get(reverse("panel:testimonial_toggle", args=[t.pk]))
    t.refresh_from_db()
    assert t.is_published is True

    # حذف
    client_admin.post(reverse("panel:testimonial_delete", args=[t.pk]))
    assert not Testimonial.objects.filter(pk=t.pk).exists()


# ===========================================================================
# متن‌های قابل ویرایش سایت
# ===========================================================================

@pytest.mark.django_db
def test_setting_list_and_edit_updates_homepage(client_admin):
    s = make_setting()
    assert client_admin.get(reverse("panel:setting_list")).status_code == 200

    r = client_admin.post(
        reverse("panel:setting_edit", args=[s.pk]),
        {
            "key": s.key,
            "label": s.label,
            "group": s.group,
            "is_textarea": "on" if s.is_textarea else "",
            "is_active": "on" if s.is_active else "",
            "value": "ساخت و توسعه (جدید)",
        },
    )
    assert r.status_code == 302
    s.refresh_from_db()
    assert s.value == "ساخت و توسعه (جدید)"

    # صفحه‌ی اصلی باید متن جدید را نشان دهد (context processor)
    home = client_admin.get(reverse("core:index")).content.decode("utf-8")
    assert "ساخت و توسعه (جدید)" in home


@pytest.mark.django_db
def test_setting_add(client_admin):
    r = client_admin.post(
        reverse("panel:setting_add"),
        {"key": "new_key", "label": "کلید جدید", "group": "other",
         "is_textarea": "", "is_active": "on", "value": "مقدار"},
    )
    assert r.status_code == 302
    assert SiteSetting.objects.filter(key="new_key").exists()


# ===========================================================================
# چند ادمین
# ===========================================================================

@pytest.mark.django_db
def test_user_list_shows_all_users(client_admin):
    make_user("ali")
    r = client_admin.get(reverse("panel:user_list"))
    assert r.status_code == 200
    assert "ali" in r.content.decode("utf-8")


# ===========================================================================
# آمار بازدید (PageView + middleware)
# ===========================================================================

@pytest.mark.django_db
def test_visit_tracking_logs_public_pages_only(client):
    """صفحات عمومی ثبت می‌شوند؛ پنل/ادمین/استاتیک نه."""
    client.get("/")
    client.get("/about/")
    client.get("/services/")
    client.get("/panel/")      # 302 + مسیر داخلی → ثبت نمی‌شود
    client.get("/admin/")      # مسیر داخلی → ثبت نمی‌شود
    client.get("/static/css/style.css")
    assert PageView.objects.count() == 3
    paths = set(PageView.objects.values_list("path", flat=True))
    assert paths == {"/", "/about/", "/services/"}


@pytest.mark.django_db
def test_visit_tracking_ignores_failed_and_post(client):
    """فقط GET موفق (200) ثبت می‌شود."""
    client.get("/this-page-does-not-exist/")  # 404
    client.post("/contact/")  # POST → ثبت نمی‌شود
    assert PageView.objects.count() == 0


@pytest.mark.django_db
def test_dashboard_shows_visit_stats(client_admin, client):
    client.get("/")
    client.get("/")
    client.get("/blog/")
    r = client_admin.get(reverse("panel:dashboard"))
    assert r.status_code == 200
    ctx = r.context
    assert ctx["visit_total"] == 3
    assert ctx["visit_today"] == 3
    assert ctx["visit_week"] == 3
    assert ctx["visit_month"] == 3
    # نمودار ۱۴ روزه — امروز باید ۳ بازدید داشته باشد و بقیه صفر
    assert len(ctx["visit_chart"]) == 14
    assert ctx["visit_chart"][-1]["count"] == 3
    assert ctx["visit_chart"][-1]["percent"] == 100
    html = r.content.decode("utf-8")
    assert "آمار بازدید" in html
    assert "پربازدیدترین صفحات" in html


@pytest.mark.django_db
def test_superuser_can_grant_and_revoke_staff(client_admin):
    u = make_user("ali")
    r = client_admin.post(reverse("panel:user_toggle_staff", args=[u.pk]))
    assert r.status_code == 302
    u.refresh_from_db()
    assert u.is_staff is True

    r = client_admin.post(reverse("panel:user_toggle_staff", args=[u.pk]))
    u.refresh_from_db()
    assert u.is_staff is False


@pytest.mark.django_db
def test_cannot_remove_own_admin(client_admin):
    me = User.objects.get(username="admin")
    r = client_admin.post(reverse("panel:user_toggle_staff", args=[me.pk]))
    assert r.status_code == 302
    me.refresh_from_db()
    assert me.is_staff is True


@pytest.mark.django_db
def test_regular_staff_cannot_grant_admin(client):
    admin = make_admin()
    # یک ادمین غیر سوپریوزر
    staff = User.objects.create_user(username="staff1", password="pass", is_staff=True)
    client.force_login(staff)
    u = make_user("ali")
    r = client.post(reverse("panel:user_toggle_staff", args=[u.pk]))
    assert r.status_code == 302
    u.refresh_from_db()
    assert u.is_staff is False

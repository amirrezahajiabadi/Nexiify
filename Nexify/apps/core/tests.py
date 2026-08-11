"""تست‌های اپ core — صفحات استاتیک، smoke تست و سرویس اعلان تلگرام."""

import pytest
from django.urls import reverse

from .services import send_telegram_notify

PAGE_PARAMS = [
    ("core:index", "index.html"),
    ("core:about", "about.html"),
    ("core:services", "services.html"),
]


@pytest.mark.django_db
@pytest.mark.parametrize("url_name,template_name", PAGE_PARAMS)
def test_static_pages_render(client, url_name, template_name):
    response = client.get(reverse(url_name))
    assert response.status_code == 200
    assert template_name in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.parametrize("url", ["/", "/about/", "/services/", "/projects/", "/blog/", "/contact/"])
def test_all_public_urls_return_200(client, url):
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_contains_rtl_lang_and_title(client):
    response = client.get(reverse("core:index"))
    content = response.content.decode("utf-8")
    assert 'lang="fa"' in content
    assert "Nexify" in content


# ===========================================================================
# فاز U5 — سکشن Social Proof: آمار واقعی + نظرات مشتریان
# ===========================================================================

@pytest.mark.django_db
def test_index_renders_real_stats_and_testimonials(client):
    from apps.blog.models import BlogPost
    from apps.panel.models import Testimonial
    from apps.projects.models import Project

    Project.objects.create(
        order=1, title="پروژه نمونه", categories="web",
        category_label="طراحی سایت", short_description="توضیح کوتاه",
    )
    BlogPost.objects.create(
        title="مقاله نمونه", slug="sample-post", category="توسعه",
        excerpt="خلاصه", published_at="2023-01-01",
    )
    Testimonial.objects.create(
        name="سارا محمدی", company="فروشگاه آنلاین",
        text="همکاری عالی بود", rating=5, order=1,
    )
    Testimonial.objects.create(
        name="رضا کریمی", company="فروشگاه آنلاین",
        text="نتیجه دقیق", rating=4, order=2,
    )

    content = client.get(reverse("core:index")).content.decode("utf-8")
    # نظرات + لوگو/نام مشتریان (شرکت‌های یکتا)
    assert "سارا محمدی" in content
    assert "فروشگاه آنلاین" in content
    # آمار واقعی: ۱ پروژه + ۱ مقاله + ۱ مشتری یکتا + رضایت ۹۰٪ (میانگین ۴.۵)
    assert "۱+" in content
    assert "۹۰٪" in content


@pytest.mark.django_db
def test_index_has_industry_solutions_and_path_select(client):
    """فاز U6: سکشن صنایع + ویجت مسیر انتخاب در صفحه‌ی اصلی."""
    content = client.get(reverse("core:index")).content.decode("utf-8")
    # ۶ کارت صنعت
    assert content.count("industry-card") == 6
    assert "فینتک" in content and "سلامت" in content and "فروشگاه آنلاین" in content
    # ویجت مسیر انتخاب
    assert "path-card" in content
    assert "من یک" in content and "و می‌خواهم" in content
    assert "دریافت مشاوره رایگان" in content
    # آیکون‌های صنعت SVG هستند نه ایموجی
    assert "industry-icon" in content


@pytest.mark.django_db
def test_index_hides_social_proof_when_empty(client):
    content = client.get(reverse("core:index")).content.decode("utf-8")
    # بدون داده، سکشن نظرات رندر نمی‌شود و آمار صفر است
    assert "testimonial-card" not in content
    assert "۰+" in content


# ===========================================================================
# سرویس اعلان تلگرام
# ===========================================================================


def test_telegram_notify_disabled_when_unconfigured(settings):
    """بدون توکن تنظیم‌شده → ارسال بی‌صدا غیرفعال است (بدون درخواست شبکه)."""
    settings.TELEGRAM_BOT_TOKEN = ""
    settings.TELEGRAM_CHAT_ID = ""
    assert send_telegram_notify("سلام") is False


def test_telegram_notify_disabled_with_placeholder_values(settings):
    """مقدار placeholder پیش‌فرض توسعه هم مانند «تنظیم‌نشده» رفتار می‌کند."""
    settings.TELEGRAM_BOT_TOKEN = "PASTE_BOT_TOKEN_HERE"
    settings.TELEGRAM_CHAT_ID = "PASTE_CHAT_ID_HERE"
    assert send_telegram_notify("سلام") is False


def test_telegram_notify_posts_to_api_when_configured(settings, monkeypatch):
    """با توکن تنظیم‌شده → POST به API تلگرام با متن و آیدی چت درست ارسال می‌شود."""
    settings.TELEGRAM_BOT_TOKEN = "TEST_TOKEN"
    settings.TELEGRAM_CHAT_ID = "12345"
    captured = {}

    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def fake_urlopen(request, timeout=10):  # noqa: ARG001
        captured["url"] = request.full_url
        captured["body"] = request.data.decode("utf-8")
        return FakeResponse()

    monkeypatch.setattr("apps.core.services.urllib.request.urlopen", fake_urlopen)

    assert send_telegram_notify("hello") is True
    assert captured["url"] == "https://api.telegram.org/botTEST_TOKEN/sendMessage"
    assert "12345" in captured["body"]
    assert "hello" in captured["body"]
    assert captured["body"].startswith("{")


def test_telegram_notify_returns_false_on_network_error(settings, monkeypatch):
    """خطای شبکه → fail-silent: False برمی‌گردد و خطا نمی‌دهد."""
    settings.TELEGRAM_BOT_TOKEN = "TEST_TOKEN"
    settings.TELEGRAM_CHAT_ID = "12345"

    def boom(*args, **kwargs):
        raise OSError("no internet")

    monkeypatch.setattr("apps.core.services.urllib.request.urlopen", boom)
    assert send_telegram_notify("hello") is False


def test_notify_contact_message_escapes_html(monkeypatch):
    """سازنده‌ی پیام تماس، محتوای کاربر را HTML-escape می‌کند (ضد تزریق)."""
    from apps.contact.models import ContactMessage

    from .services import notify_contact_message

    captured = {}
    monkeypatch.setattr(
        "apps.core.services.send_telegram_notify", lambda text: captured.update(text=text)
    )
    msg = ContactMessage(
        name="<b>علی</b>",
        email="ali@example.com",
        contact_method="phone",
        phone="09123456789",
        request_type="web-design",
        subject="<i>مهم</i>",
        message="پیام <script>alert(1)</script>",
    )
    notify_contact_message(msg)

    assert captured["text"].startswith("📩")
    assert "&lt;b&gt;" in captured["text"]
    assert "&lt;i&gt;" in captured["text"]
    assert "&lt;script&gt;" in captured["text"]

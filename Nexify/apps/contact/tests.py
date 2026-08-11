"""تست‌های اپ contact — فرم تماس، هانی‌پات (دولایه)، ویو و ایمیل اطلاع‌رسانی."""

import pytest
from django.core import mail
from django.urls import reverse

from .forms import ContactForm
from .models import ContactMessage, FAQ

# ---------------------------------------------------------------------------
# داده‌ی معتبر برای POST — مطابق فیلدهای فرم
# ---------------------------------------------------------------------------
VALID_DATA = {
    "name": "علی محمدی",
    "email": "ali@example.com",
    "contact_method": "phone",
    "phone": "09123456789",
    "request_type": "web-design",
    "subject": "طراحی سایت فروشگاهی",
    "message": "سلام، برای فروشگاه آنلاینم به طراحی سایت نیاز دارم.",
}


# ===========================================================================
# ContactForm — اعتبارسنجی و هانی‌پات
# ===========================================================================

def test_form_valid_data():
    form = ContactForm(data=VALID_DATA)
    assert form.is_valid()
    assert form.cleaned_data["website"] == ""


def test_form_rejects_missing_required_fields():
    form = ContactForm(data={})
    assert not form.is_valid()
    assert "name" in form.errors
    assert "email" in form.errors
    assert "request_type" in form.errors
    assert "message" in form.errors


def test_form_rejects_short_name():
    data = dict(VALID_DATA, name="ع")
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "name" in form.errors


def test_form_rejects_short_message():
    data = dict(VALID_DATA, message="کوتاه")
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "message" in form.errors


def test_phone_method_requires_phone():
    """روش «تماس تلفنی» بدون شماره → خطا روی فیلد phone."""
    data = dict(VALID_DATA, contact_method="phone", phone="")
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "phone" in form.errors


def test_telegram_method_requires_telegram_id():
    """روش «تلگرام» بدون آیدی → خطا روی فیلد telegram_id."""
    data = dict(VALID_DATA, contact_method="telegram", phone="", telegram_id="")
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "telegram_id" in form.errors


def test_telegram_method_valid_with_id():
    """روش «تلگرام» با آیدی معتبر → فرم معتبر است (شماره لازم نیست)."""
    data = dict(VALID_DATA, contact_method="telegram", phone="", telegram_id="@nexify_ai")
    form = ContactForm(data=data)
    assert form.is_valid()
    # «@» ابتدایی حذف می‌شود
    assert form.cleaned_data["telegram_id"] == "nexify_ai"


def test_telegram_method_rejects_invalid_format():
    """آیدی تلگرام با کاراکتر غیرمجاز (مثلاً فاصله یا فارسی) → خطا."""
    data = dict(VALID_DATA, contact_method="telegram", phone="", telegram_id="آیدی نادرست")
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "telegram_id" in form.errors


def test_phone_method_ignores_telegram_id():
    """روش «تماس تلفنی» → آیدی تلگرام می‌تواند خالی بماند."""
    data = dict(VALID_DATA, telegram_id="")
    form = ContactForm(data=data)
    assert form.is_valid()
    assert form.cleaned_data["telegram_id"] == ""


def test_form_rejects_invalid_email():
    data = dict(VALID_DATA, email="not-an-email")
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "email" in form.errors


def test_form_honeypot_clean_raises():
    """لایه‌ی دفاعی فرم: پر شدن هانی‌پات → فرم نامعتبر."""
    data = dict(VALID_DATA, website="http://spam.example")
    form = ContactForm(data=data)
    assert not form.is_valid()
    assert "__all__" in form.errors


def test_form_honeypot_never_in_meta_fields():
    """هانی‌پات عمداً در Meta.fields نیست تا هرگز در دیتابیس ذخیره نشود."""
    assert "website" not in ContactForm.Meta.fields
    # هیچ فیلدی از مدل هم به هانی‌پات نگاشت نمی‌شود
    model_fields = {f.name for f in ContactForm.Meta.model._meta.get_fields()}
    assert "website" not in model_fields


# ===========================================================================
# ویوی تماس — GET
# ===========================================================================

@pytest.mark.django_db
def test_get_renders_form_and_context(client):
    FAQ.objects.create(question="قیمت خدمات چقدر است؟", answer="بستگی به پروژه دارد.", order=1)
    FAQ.objects.create(
        question="مخفی؟", answer="نباید دیده شود", order=2, is_published=False
    )
    response = client.get(reverse("contact:index"))

    assert response.status_code == 200
    assert "contact.html" in [t.name for t in response.templates]
    assert isinstance(response.context["form"], ContactForm)
    # فقط FAQ های منتشرشده
    assert len(response.context["faqs"]) == 1
    # ۷ گزینه‌ی نوع درخواست
    assert len(response.context["options"]) == len(ContactMessage.REQUEST_TYPES)
    # CSRF توکن در فرم
    assert b"csrfmiddlewaretoken" in response.content


@pytest.mark.django_db
def test_get_preselects_type_and_subject_from_query(client):
    """فاز U6: ویجت مسیر انتخاب با ?type= و ?subject= فرم را پری‌سلکت می‌کند."""
    response = client.get(reverse("contact:index") + "?type=agent-ai&subject=استارتاپ — Agent هوشمند بسازم")
    assert response.status_code == 200
    form = response.context["form"]
    assert form.initial.get("request_type") == "agent-ai"
    assert form.initial.get("subject") == "استارتاپ — Agent هوشمند بسازم"

    # مقدار نامعتبر type نادیده گرفته می‌شود
    response2 = client.get(reverse("contact:index") + "?type=invalid-type&subject=x")
    assert response2.context["form"].initial.get("request_type") is None
    assert response2.context["form"].initial.get("subject") == "x"


# ===========================================================================
# دسترس‌پذیری (فاز U1): اتصال label ↔ input برای screen reader
# ===========================================================================

@pytest.mark.django_db
def test_form_labels_connected_to_inputs(client):
    """هر input فرم باید یک label با for داشته باشد و id آن تطبیق کند (U1)."""
    response = client.get(reverse("contact:index"))
    html = response.content.decode("utf-8")

    pairs = [
        ("id_name", "for=\"id_name\""),
        ("id_email", "for=\"id_email\""),
        ("id_phone", "for=\"id_phone\""),
        ("id_telegram", "for=\"id_telegram\""),
        ("id_request_type", "for=\"id_request_type\""),
        ("id_subject", "for=\"id_subject\""),
        ("id_message", "for=\"id_message\""),
    ]
    for input_id, label_for in pairs:
        assert f'id="{input_id}"' in html, f"input با id={input_id} وجود ندارد"
        assert label_for in html, f"label با {label_for} وجود ندارد"
    # سلکت مخفی باید id جدید (اتصال label) را داشته باشد نه id قدیمی
    assert 'id="id_request_type"' in html
    assert 'id="hiddenSelect"' not in html


# ===========================================================================
# ویوی تماس — POST
# ===========================================================================

@pytest.mark.django_db
def test_valid_post_saves_message_and_sends_email(client, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

    response = client.post(reverse("contact:index"), VALID_DATA)

    assert response.status_code == 200
    # حالت موفقیت در context و قالب
    assert response.context["success"] is True
    assert "پیامت با موفقیت ارسال شد" in response.content.decode("utf-8")
    # دقیقاً یک پیام در دیتابیس
    assert ContactMessage.objects.count() == 1
    msg = ContactMessage.objects.first()
    assert msg.name == VALID_DATA["name"]
    assert msg.email == VALID_DATA["email"]
    assert msg.request_type == "web-design"
    assert msg.is_read is False
    # ایمیل اطلاع‌رسانی ارسال شد
    assert len(mail.outbox) == 1
    assert VALID_DATA["name"] in mail.outbox[0].subject


@pytest.mark.django_db
def test_valid_post_triggers_telegram_notify(client, monkeypatch):
    """پس از ذخیره‌ی پیام، اعلان تلگرام هم صدا زده می‌شود (با خود پیام)."""
    calls = []
    monkeypatch.setattr(
        "apps.contact.views.notify_contact_message", lambda m: calls.append(m)
    )

    response = client.post(reverse("contact:index"), VALID_DATA)

    assert response.status_code == 200
    assert len(calls) == 1
    assert calls[0].name == VALID_DATA["name"]
    assert calls[0].email == VALID_DATA["email"]


@pytest.mark.django_db
def test_valid_post_with_telegram_method(client, settings):
    """ارسال با روش «تلگرام» → آیدی ذخیره می‌شود (با حذف @) و شماره لازم نیست."""
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    data = dict(VALID_DATA, contact_method="telegram", phone="", telegram_id="@amirreza")

    response = client.post(reverse("contact:index"), data)

    assert response.status_code == 200
    assert response.context["success"] is True
    msg = ContactMessage.objects.first()
    assert msg.contact_method == "telegram"
    assert msg.telegram_id == "amirreza"
    assert msg.phone == ""


@pytest.mark.django_db
def test_honeypot_does_not_trigger_telegram_notify(client, monkeypatch):
    """هانی‌پات پر شده → اعلان تلگرام هم نباید صدا زده شود."""
    calls = []
    monkeypatch.setattr(
        "apps.contact.views.notify_contact_message", lambda m: calls.append(m)
    )
    data = dict(VALID_DATA, website="http://bot.example")

    response = client.post(reverse("contact:index"), data)

    assert response.status_code == 200
    assert calls == []


@pytest.mark.django_db
def test_honeypot_filled_is_silently_dropped(client, settings):
    """هانی‌پات پر شده → ساکت رد: پیام موفقیت نمایش داده می‌شود ولی هیچ‌چیز ذخیره نمی‌شود."""
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    data = dict(VALID_DATA, website="http://bot.example")

    response = client.post(reverse("contact:index"), data)

    assert response.status_code == 200
    # ربات پیام موفقیت را می‌بیند (متوجه نمی‌شود رد شده است)
    assert response.context["success"] is True
    assert "پیامت با موفقیت ارسال شد" in response.content.decode("utf-8")
    # ولی هیچ پیامی ذخیره نشده و هیچ ایمیلی ارسال نشده
    assert ContactMessage.objects.count() == 0
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_invalid_post_shows_field_errors(client):
    data = dict(VALID_DATA, name="", email="bad-email", message="کوتاه")
    response = client.post(reverse("contact:index"), data)

    assert response.status_code == 200
    # حالت ناموفق: کلید success اصلاً در context نیست
    assert "success" not in response.context
    # خطاهای فیلد در قالب رندر می‌شوند
    content = response.content.decode("utf-8")
    assert "field-error" in content
    assert ContactMessage.objects.count() == 0


# ===========================================================================
# مدل‌ها
# ===========================================================================

@pytest.mark.django_db
def test_contact_message_str_and_ordering():
    first = ContactMessage.objects.create(**VALID_DATA)
    second = ContactMessage.objects.create(
        name="مریم", email="m@example.com", request_type="consulting", message="پیام دوم"
    )
    # مرتب‌سازی نزولی بر اساس تاریخ ایجاد
    assert list(ContactMessage.objects.all()) == [second, first]
    assert str(first) == "علی محمدی — طراحی سایت"


@pytest.mark.django_db
def test_faq_str_and_published_filter():
    faq = FAQ.objects.create(question="سوال؟", answer="جواب", order=0)
    assert str(faq) == "سوال؟"
    assert FAQ.objects.filter(is_published=True).count() == 1

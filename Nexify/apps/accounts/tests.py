"""تست‌های اپ accounts — ثبت‌نام، ورود، خروج، هانی‌پات و وضعیت نوبار."""

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

PASSWORD = "StrongPass123!"

REGISTER_DATA = {
    "username": "ali",
    "email": "ali@example.com",
    "password1": PASSWORD,
    "password2": PASSWORD,
}


# ===========================================================================
# ثبت‌نام
# ===========================================================================

@pytest.mark.django_db
def test_register_get_renders_form(client):
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 200
    assert "accounts/register.html" in [t.name for t in response.templates]
    assert b"csrfmiddlewaretoken" in response.content


@pytest.mark.django_db
def test_register_creates_user_and_logs_in(client):
    response = client.post(reverse("accounts:register"), REGISTER_DATA)
    assert response.status_code == 302
    assert response.url == reverse("core:index")
    # کاربر با ایمیل درست ساخته شد
    user = User.objects.get(username="ali")
    assert user.email == "ali@example.com"
    # ورود خودکار بعد از ثبت‌نام
    assert "_auth_user_id" in client.session
    assert client.session["_auth_user_id"] == str(user.pk)


@pytest.mark.django_db
def test_register_triggers_telegram_notify(client, monkeypatch):
    """پس از ساخت کاربر، اعلان تلگرام صدا زده می‌شود (با نام کاربری و IP)."""
    calls = []
    monkeypatch.setattr(
        "apps.accounts.views.notify_new_user",
        lambda user, ip: calls.append((user, ip)),
    )

    response = client.post(reverse("accounts:register"), REGISTER_DATA)

    assert response.status_code == 302
    assert len(calls) == 1
    assert calls[0][0].username == REGISTER_DATA["username"]


@pytest.mark.django_db
def test_register_rejects_mismatched_passwords(client):
    data = dict(REGISTER_DATA, password2="Different123!")
    response = client.post(reverse("accounts:register"), data)
    assert response.status_code == 200
    assert User.objects.count() == 0
    # خطای فیلد در قالب رندر شده
    assert "field-error" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_register_rejects_duplicate_username(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    response = client.post(reverse("accounts:register"), REGISTER_DATA)
    assert response.status_code == 200
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_honeypot_does_not_notify(client, monkeypatch):
    """هانی‌پات پر شده → اعلان تلگرام نباید صدا زده شود."""
    calls = []
    monkeypatch.setattr(
        "apps.accounts.views.notify_new_user", lambda user, ip: calls.append(user)
    )
    data = dict(REGISTER_DATA, website="http://bot.example")

    response = client.post(reverse("accounts:register"), data)

    assert response.status_code == 302
    assert calls == []


@pytest.mark.django_db
def test_register_honeypot_is_silently_dropped(client):
    """هانی‌پات پر شده → بی‌صدا مثل موفقیت هدایت می‌شود ولی هیچ کاربری ساخته نمی‌شود."""
    data = dict(REGISTER_DATA, website="http://bot.example")
    response = client.post(reverse("accounts:register"), data)
    assert response.status_code == 302
    assert response.url == reverse("core:index")
    assert User.objects.count() == 0
    assert "_auth_user_id" not in client.session


@pytest.mark.django_db
def test_register_honeypot_second_layer_clean_raises():
    """لایه‌ی دوم هانی‌پات: clean() خود فرم هم باید پر شدن را رد کند."""
    from .forms import RegisterForm

    form = RegisterForm(data=dict(REGISTER_DATA, website="http://bot.example"))
    assert not form.is_valid()
    assert "__all__" in form.errors


@pytest.mark.django_db
def test_register_next_redirects_back(client):
    """ثبت‌نام با ?next= → بعد از ورود خودکار به همان صفحه برمی‌گردد."""
    data = dict(REGISTER_DATA, next="/about/")
    response = client.post(reverse("accounts:register"), data)
    assert response.status_code == 302
    assert response.url == "/about/"
    assert User.objects.filter(username="ali").exists()


@pytest.mark.django_db
def test_register_blocks_external_next(client):
    """محافظت open-redirect: next خارجی در ثبت‌نام نادیده گرفته می‌شود."""
    data = dict(REGISTER_DATA, next="https://evil.example")
    response = client.post(reverse("accounts:register"), data)
    assert response.status_code == 302
    assert response.url == reverse("core:index")
    assert "evil.example" not in response.url


@pytest.mark.django_db
def test_authenticated_user_redirected_from_register(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    client.login(username="ali", password=PASSWORD)
    response = client.get(reverse("accounts:register"))
    assert response.status_code == 302


# ===========================================================================
# ورود
# ===========================================================================

@pytest.mark.django_db
def test_login_get_renders_form(client):
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 200
    assert "accounts/login.html" in [t.name for t in response.templates]
    assert b"csrfmiddlewaretoken" in response.content


@pytest.mark.django_db
def test_login_success_redirects_home(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    response = client.post(
        reverse("accounts:login"), {"username": "ali", "password": PASSWORD}
    )
    assert response.status_code == 302
    assert response.url == reverse("core:index")
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_login_invalid_credentials_shows_error(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    response = client.post(
        reverse("accounts:login"), {"username": "ali", "password": "wrong-pass"}
    )
    assert response.status_code == 200
    assert "_auth_user_id" not in client.session
    # پیام خطای عمومی در قالب رندر شده است
    assert "auth-errors" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_login_next_redirects_back(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    response = client.post(
        reverse("accounts:login"),
        {"username": "ali", "password": PASSWORD, "next": "/about/"},
    )
    assert response.status_code == 302
    assert response.url == "/about/"


@pytest.mark.django_db
def test_login_blocks_external_next(client):
    """محافظت در برابر open-redirect: next خارجی نادیده گرفته می‌شود."""
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    response = client.post(
        reverse("accounts:login"),
        {"username": "ali", "password": PASSWORD, "next": "https://evil.example"},
    )
    assert response.status_code == 302
    assert response.url != "https://evil.example"
    assert "evil.example" not in response.url


@pytest.mark.django_db
def test_authenticated_user_redirected_from_login(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    client.login(username="ali", password=PASSWORD)
    response = client.get(reverse("accounts:login"))
    assert response.status_code == 302


# ===========================================================================
# خروج
# ===========================================================================

@pytest.mark.django_db
def test_logout_requires_post(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    client.login(username="ali", password=PASSWORD)
    # GET → فقط به صفحه‌ی ورود هدایت می‌شود، کاربر وارد باقی می‌ماند
    response = client.get(reverse("accounts:logout"))
    assert response.status_code == 302
    assert response.url == reverse("accounts:login")
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_logout_post_logs_out(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    client.login(username="ali", password=PASSWORD)
    response = client.post(reverse("accounts:logout"))
    assert response.status_code == 302
    assert response.url == reverse("core:index")
    assert "_auth_user_id" not in client.session


# ===========================================================================
# وضعیت نوبار
# ===========================================================================

@pytest.mark.django_db
def test_navbar_shows_login_register_for_guest(client):
    response = client.get(reverse("core:index"))
    content = response.content.decode("utf-8")
    assert reverse("accounts:login") in content
    assert reverse("accounts:register") in content


@pytest.mark.django_db
def test_navbar_shows_username_and_logout_for_user(client):
    User.objects.create_user("ali", "ali@example.com", PASSWORD)
    client.login(username="ali", password=PASSWORD)
    response = client.get(reverse("core:index"))
    content = response.content.decode("utf-8")
    assert "auth-user-chip" in content
    assert reverse("accounts:logout") in content
    # دکمه‌های ورود/ثبت‌نام دیگر نمایش داده نمی‌شوند
    assert reverse("accounts:login") not in content

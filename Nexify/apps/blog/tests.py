"""تست‌های اپ blog — مدل BlogPost و صفحات لیست/جزئیات."""

from datetime import date

import pytest
from django.db.utils import IntegrityError
from django.urls import reverse

from .models import BlogPost


def make_post(title="مقاله", slug="article", is_published=True, **kwargs):
    defaults = dict(
        title=title,
        slug=slug,
        category="AI",
        excerpt="خلاصه‌ی مقاله",
        published_at=date.today(),
    )
    defaults.update(kwargs)
    return BlogPost.objects.create(**defaults, is_published=is_published)


# ===========================================================================
# مدل BlogPost
# ===========================================================================

@pytest.mark.django_db
def test_post_str():
    p = make_post(title="راهنمای جنگو")
    assert str(p) == "راهنمای جنگو"


@pytest.mark.django_db
def test_post_not_published_by_default():
    p = BlogPost.objects.create(
        title="پیش‌نویس", slug="draft", category="AI", excerpt="x",
        published_at=date.today(),
    )
    assert p.is_published is False


@pytest.mark.django_db
def test_post_slug_is_unique():
    make_post(slug="same-slug")
    # یکتایی slug در سطح دیتابیس — IntegrityError انتظار می‌رود
    with pytest.raises(IntegrityError):
        make_post(slug="same-slug")


@pytest.mark.django_db
def test_post_ordering_newest_first():
    make_post(title="قدیمی", slug="old", published_at=date(2024, 1, 1))
    make_post(title="جدید", slug="new", published_at=date(2025, 1, 1))
    assert [p.title for p in BlogPost.objects.all()] == ["جدید", "قدیمی"]


@pytest.mark.django_db
def test_post_read_time_default():
    p = make_post()
    assert p.read_time == 5


# ===========================================================================
# لیست مقالات
# ===========================================================================

@pytest.mark.django_db
def test_list_renders_svg_icons_not_emoji(client):
    """فاز U2: آیکون دیتابیس باید با SVG رندر شود نه ایموجی."""
    make_post(title="پست با آیکون", slug="icon-post", icon="🤖")
    response = client.get(reverse("blog:list"), HTTP_HOST="127.0.0.1")

    assert response.status_code == 200
    html = response.content.decode("utf-8")
    # SVG آیکون رندر شده (فیلتر icon_svg)
    assert 'class="icon-svg' in html
    # ایموجی به‌عنوان آیکون رندر نشده (فقط به‌عنوان کلید فیلتر در سورس است)
    assert html.count("🤖") == 0


@pytest.mark.django_db
def test_list_shows_only_published(client):
    make_post(title="منتشر شده", slug="published-post")
    make_post(title="پیش‌نویس", slug="draft-post", is_published=False)

    response = client.get(reverse("blog:list"))

    assert response.status_code == 200
    assert "blog/blog_list.html" in [t.name for t in response.templates]
    assert [p.title for p in response.context["posts"]] == ["منتشر شده"]
    content = response.content.decode("utf-8")
    assert "منتشر شده" in content
    # پیش‌نویس نباید در خروجی باشد
    assert "پیش‌نویس" not in content


# ===========================================================================
# جزئیات مقاله
# ===========================================================================

@pytest.mark.django_db
def test_detail_renders_published_post(client):
    post = make_post(title="جزئیات", slug="detail-post")
    response = client.get(reverse("blog:detail", args=[post.slug]))

    assert response.status_code == 200
    assert "blog/blog_detail.html" in [t.name for t in response.templates]
    assert response.context["post"] == post
    assert "جزئیات" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_detail_404_for_unpublished_post(client):
    post = make_post(slug="hidden-post", is_published=False)
    response = client.get(reverse("blog:detail", args=[post.slug]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_detail_404_for_unknown_slug(client):
    response = client.get(reverse("blog:detail", args=["does-not-exist"]))
    assert response.status_code == 404


# ===========================================================================
# کامنت‌ها
# ===========================================================================

from django.contrib.auth.models import User

from .models import Comment


@pytest.mark.django_db
def test_comment_str_and_ordering():
    post = make_post()
    user = User.objects.create_user("ali", "a@e.com", "StrongPass123!")
    first = Comment.objects.create(post=post, author=user, body="اول")
    second = Comment.objects.create(post=post, author=user, body="دوم")
    assert list(post.comments.all()) == [first, second]
    assert str(first) == "ali — مقاله"


@pytest.mark.django_db
def test_detail_shows_only_visible_comments(client):
    post = make_post()
    user = User.objects.create_user("ali", "a@e.com", "StrongPass123!")
    Comment.objects.create(post=post, author=user, body="نمایش داده می‌شود")
    Comment.objects.create(post=post, author=user, body="نباید دیده شود", is_visible=False)

    response = client.get(reverse("blog:detail", args=[post.slug]))
    content = response.content.decode("utf-8")
    assert "نمایش داده می‌شود" in content
    assert "نباید دیده شود" not in content
    # مهمان → فرم کامنت نیست ولی لینک ورود دارد
    assert "comment-login-hint" in content
    assert reverse("accounts:login") in content


@pytest.mark.django_db
def test_guest_cannot_post_comment(client):
    post = make_post()
    response = client.post(
        reverse("blog:detail", args=[post.slug]), {"body": "کامنت مهمان"}
    )
    assert response.status_code == 302
    assert Comment.objects.count() == 0


@pytest.mark.django_db
def test_authenticated_user_can_post_comment(client):
    post = make_post()
    User.objects.create_user("ali", "a@e.com", "StrongPass123!")
    client.login(username="ali", password="StrongPass123!")

    response = client.post(
        reverse("blog:detail", args=[post.slug]), {"body": "کامنت من"}
    )
    assert response.status_code == 302
    comment = Comment.objects.get()
    assert comment.body == "کامنت من"
    assert comment.author.username == "ali"
    assert comment.post == post
    assert comment.is_visible is True


@pytest.mark.django_db
def test_comment_short_body_rejected(client):
    post = make_post()
    User.objects.create_user("ali", "a@e.com", "StrongPass123!")
    client.login(username="ali", password="StrongPass123!")

    response = client.post(reverse("blog:detail", args=[post.slug]), {"body": "ک"})
    assert response.status_code == 200  # فرم با خطا دوباره رندر می‌شود
    assert Comment.objects.count() == 0

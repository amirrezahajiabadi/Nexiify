"""تست‌های اپ projects — مدل Project و صفحه‌ی نمونه‌کارها."""

import pytest
from django.urls import reverse

from .models import Project


def make_project(title="پروژه", order=0, is_published=True, **kwargs):
    defaults = dict(
        title=title,
        order=order,
        category_label="وب",
        short_description="توضیح کوتاه",
    )
    defaults.update(kwargs)
    return Project.objects.create(**defaults, is_published=is_published)


# ===========================================================================
# مدل Project
# ===========================================================================

@pytest.mark.django_db
def test_project_str():
    p = make_project(title="سایت فروشگاهی")
    assert str(p) == "Project-0 | سایت فروشگاهی"


@pytest.mark.django_db
def test_project_ordering_by_order():
    make_project(title="دوم", order=2)
    make_project(title="اول", order=1)
    make_project(title="سوم", order=3)
    assert [p.title for p in Project.objects.all()] == ["اول", "دوم", "سوم"]


@pytest.mark.django_db
def test_project_defaults():
    p = make_project()
    assert p.is_published is True
    assert p.tags == []
    assert p.gradient == "135deg,#1e1b4b,#7c3aed"
    assert p.icon == "🌐"
    assert p.categories == "web"


@pytest.mark.django_db
def test_project_json_tags():
    p = make_project(tags=["django", "postgres"])
    assert p.tags == ["django", "postgres"]


# ===========================================================================
# ویوی لیست پروژه‌ها
# ===========================================================================

@pytest.mark.django_db
def test_list_shows_only_published(client):
    visible = make_project(title="منتشر شده", order=1)
    make_project(title="پیش‌نویس", order=2, is_published=False)

    response = client.get(reverse("projects:list"))

    assert response.status_code == 200
    assert "projects.html" in [t.name for t in response.templates]
    projects = list(response.context["projects"])
    assert projects == [visible]
    content = response.content.decode("utf-8")
    # کارت پروژه‌ی منتشرشده رندر شده و پیش‌نویس نه
    assert "منتشر شده" in content
    assert "پیش‌نویس" not in content


@pytest.mark.django_db
def test_list_ordering_follows_model(client):
    make_project(title="اول", order=1)
    make_project(title="دوم", order=2)
    response = client.get(reverse("projects:list"))
    assert [p.title for p in response.context["projects"]] == ["اول", "دوم"]


@pytest.mark.django_db
def test_list_empty_when_nothing_published(client):
    make_project(is_published=False)
    response = client.get(reverse("projects:list"))
    assert response.status_code == 200
    assert list(response.context["projects"]) == []

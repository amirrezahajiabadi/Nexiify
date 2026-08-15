# -*- coding: utf-8 -*-
"""فرم‌های پنل ادمین."""

from django import forms

from apps.blog.models import BlogPost
from apps.contact.models import FAQ
from apps.projects.models import Project

from .models import SiteSetting, Testimonial


class PanelFormMixin:
    """کلاس‌های ورودی مشترک (form-input / form-textarea) را به ویجت‌های متنی اضافه می‌کند
    تا پنل از recipe مشترک style.css استفاده کند و CSS تکراری در panel.css نداشته باشیم."""

    TEXT_WIDGETS = (
        forms.TextInput,
        forms.EmailInput,
        forms.URLInput,
        forms.NumberInput,
        forms.DateInput,
        forms.SearchInput,
        forms.Select,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, forms.Textarea):
                cls = "form-textarea"
            elif isinstance(w, self.TEXT_WIDGETS):
                cls = "form-input"
            else:
                continue  # checkbox / file / hidden — استایل جداگانه‌ی خودشان را دارند
            existing = w.attrs.get("class", "")
            w.attrs["class"] = (existing + " " + cls).strip()


class BlogPostForm(PanelFormMixin, forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = [
            "title", "slug", "category", "icon", "cover_image", "gradient",
            "excerpt", "content", "read_time", "published_at", "is_published",
        ]
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 14, "class": "code-input"}),
            "published_at": forms.DateInput(attrs={"type": "date"}),
            "gradient": forms.TextInput(
                attrs={"placeholder": "مثلاً linear-gradient(135deg,#7c3aed,#312e81)"}
            ),
        }
        labels = {
            "slug": "اسلاگ (خالی بگذارید تا خودکار ساخته شود)",
            "gradient": "گرادیان آیکون",
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if not slug and self.cleaned_data.get("title"):
            from django.utils.text import slugify
            slug = slugify(self.cleaned_data["title"]) or "post"
        return slug


class ProjectForm(PanelFormMixin, forms.ModelForm):
    tags = forms.CharField(
        required=False,
        label="تکنولوژی‌ها (با ویرگول جدا کنید)",
        help_text="مثلاً: Python, Django, Docker",
        widget=forms.TextInput(attrs={"dir": "ltr", "placeholder": "Python, Django, Docker"}),
    )

    class Meta:
        model = Project
        fields = [
            "title", "order", "icon", "cover_image", "categories", "category_label",
            "short_description", "description", "tags", "duration", "role",
            "status", "github_url", "gradient", "is_published",
        ]
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 2}),
            "description": forms.Textarea(attrs={"rows": 8, "class": "code-input"}),
            "github_url": forms.URLInput(attrs={"dir": "ltr"}),
            "gradient": forms.TextInput(
                attrs={"placeholder": "مثلاً linear-gradient(135deg,#3b82f6,#1e3a8a)"}
            ),
        }
        labels = {
            "categories": "دسته‌ها (با ویرگول جدا کنید)",
            "category_label": "برچسب دسته (روی کارت)",
            "status": "وضعیت (متن آزاد)",
        }

    def clean_tags(self):
        raw = self.cleaned_data.get("tags", "")
        items = [t.strip() for t in raw.replace("\n", ",").split(",") if t.strip()]
        return items

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.tags:
            self.fields["tags"].initial = ", ".join(self.instance.tags)


class FAQForm(PanelFormMixin, forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer", "order", "is_published"]
        widgets = {"answer": forms.Textarea(attrs={"rows": 4})}
        labels = {"order": "ترتیب نمایش (کوچک‌تر = بالاتر)"}


class TestimonialForm(PanelFormMixin, forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "company", "text", "rating", "order", "is_published"]
        widgets = {"text": forms.Textarea(attrs={"rows": 4})}


class SiteSettingForm(PanelFormMixin, forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = ["key", "label", "value", "group", "is_textarea", "is_active"]
        widgets = {
            "value": forms.Textarea(attrs={"rows": 4}),
        }
        help_texts = {
            "key": "شناسه‌ی یکتا — بعد از ساخت قابل تغییر نیست",
        }

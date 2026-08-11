# -*- coding: utf-8 -*-
"""ویوهای اپ core — صفحات اصلی سایت (فاز U5: آمار واقعی + نظرات مشتریان)."""

from django.shortcuts import render

from apps.blog.models import BlogPost
from apps.panel.models import Testimonial
from apps.projects.models import Project


def index(request):
    # ---------- سکشن Social Proof (فاز U5) ----------
    testimonials = list(
        Testimonial.objects.filter(is_published=True).order_by("order", "id")
    )
    # لوگو/نام مشتریان — نام‌های یکتای شرکت‌ها با حفظ ترتیب
    client_logos = []
    seen = set()
    for t in testimonials:
        company = (t.company or "").strip()
        if company and company not in seen:
            seen.add(company)
            client_logos.append(company)

    # ---------- آمار واقعی از دیتابیس ----------
    avg_rating = (
        sum(t.rating for t in testimonials) / len(testimonials)
        if testimonials
        else 0
    )
    stats = {
        "projects": Project.objects.filter(is_published=True).count(),
        "posts": BlogPost.objects.filter(is_published=True).count(),
        "clients": len(seen) or len(testimonials),
        "satisfaction": round(avg_rating * 100 / 5) if avg_rating else 0,
    }

    ctx = {
        "testimonials": testimonials[:3],
        "client_logos": client_logos,
        "stats": stats,
    }
    return render(request, "index.html", ctx)


def about(request):
    return render(request, "about.html")


def services(request):
    return render(request, "services.html")

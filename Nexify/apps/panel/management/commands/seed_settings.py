# -*- coding: utf-8 -*-
"""seed متن‌های قابل ویرایش سایت — اجرای چندباره امن است (update_or_create)."""

from django.core.management.base import BaseCommand

from apps.panel.models import SiteSetting

DEFAULTS = [
    # صفحه اصلی — هیرو
    ("hero_title_1", "ساخت و توسعه", "خط اول عنوان هیرو", "home", False),
    ("hero_title_2", "سرویس‌های", "خط دوم عنوان هیرو (قبل از متن رنگی)", "home", False),
    ("hero_title_accent", "هوش مصنوعی", "بخش رنگی عنوان هیرو", "home", False),
    ("hero_subtitle", "Nexify پلی است میان ایده‌های شما و تکنولوژی‌های هوشمند. ما راه‌حل‌هایی می‌سازیم که تفاوت ایجاد می‌کنند.", "زیرعنوان هیرو", "home", True),

    # صفحه اصلی — دعوت به تماس
    ("cta_title_1", "آماده‌اید", "خط اول عنوان CTA", "home", False),
    ("cta_title_accent", "پروژه", "بخش رنگی عنوان CTA", "home", False),
    ("cta_title_2", "خود را شروع کنیم؟", "خط آخر عنوان CTA", "home", False),
    ("cta_subtitle", "یک گفتگوی کوتاه می‌تواند آغاز یک همکاری بزرگ باشد.", "زیرعنوان CTA", "home", True),

    # تماس
    ("contact_email", "amirrezahajiabadi480@gmail.com", "ایمیل نمایش داده‌شده در سایت", "contact", False),
    ("contact_telegram", "amirrezahajiabadi", "آیدی تلگرام", "contact", False),
]


class Command(BaseCommand):
    help = "ایجاد/به‌روزرسانی متن‌های پیش‌فرض قابل ویرایش سایت"

    def handle(self, *args, **options):
        for key, value, label, group, is_textarea in DEFAULTS:
            SiteSetting.objects.update_or_create(
                key=key,
                defaults={
                    "value": value,
                    "label": label,
                    "group": group,
                    "is_textarea": is_textarea,
                },
            )
        self.stdout.write(self.style.SUCCESS(f"✅ {len(DEFAULTS)} متن سایت آماده شد."))

# -*- coding: utf-8 -*-
"""Context processor — متن‌های قابل ویرایش سایت را به همه‌ی تمپلیت‌ها می‌دهد.

در تمپلیت با {{ site_settings.hero_subtitle }} استفاده می‌شود.
در صورت نبودن کلید، مقدار خالی برمی‌گردد (بدون خطا).
"""

from .models import SiteSetting


def site_settings(request):
    try:
        values = {
            s.key: s.value
            for s in SiteSetting.objects.filter(is_active=True)
        }
    except Exception:  # pragma: no cover — قبل از مایگریشن
        values = {}
    return {"site_settings": values}

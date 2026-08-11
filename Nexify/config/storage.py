"""ذخیره‌ساز استاتیک توسعه — cache-busting خودکار بر اساس mtime فایل.

در production این مشکل وجود ندارد: WhiteNoise + `CompressedManifestStaticFilesStorage`
نام فایل را هش می‌کند (مثل `style.abc123.css`) و مرورگر کاربر همیشه نسخه‌ی تازه را می‌گیرد.

در توسعه، فایل‌ها با نام ساده سرو می‌شوند و مرورگر ممکن است نسخه‌ی قدیمی را کش کند
(که باعث می‌شود بعد از تغییر CSS/JS «Ctrl+F5» لازم شود). این کلاس به هر URL استاتیک
یک `?v=<mtime>` اضافه می‌کند؛ وقتی فایل تغییر کند mtime تغییر می‌کند → URL جدید می‌شود
→ مرورگر نسخه‌ی تازه را می‌گیرد و وقتی فایل عوض نشده همان URL قبلی است → کش سالم.

فقط در `config/settings/development.py` فعال است — production دست‌نخورده می‌ماند.
"""

import os

from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import StaticFilesStorage


class MtimeStaticFilesStorage(StaticFilesStorage):
    """StaticFilesStorage توسعه که mtime فایل را به URL اضافه می‌کند."""

    def url(self, name):
        url = super().url(name)
        full_path = find(name)
        if full_path and os.path.exists(full_path):
            url += f"?v={int(os.path.getmtime(full_path))}"
        return url

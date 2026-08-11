"""
آیکون‌های SVG پروژه (فاز U2) — منبع واحد جایگزینی ایموجی‌ها.

همه‌ی آیکون‌ها stroke-based (سبک Lucide/Feather، viewBox 0 0 24 24) هستند تا با
تم تاریک/روشن (`currentColor`) و استایل شیشه‌ای کارت‌های خدمات هماهنگ بمانند.

نحوه‌ی استفاده در تمپلیت:
    {% load core_extras %}
    {{ "📞"|icon_svg }}            → <svg class="icon-svg" ...>...</svg>
    {{ "🌐"|icon_svg:"big" }}      → کلاس اضافه

برای داده‌ی دیتابیس (مثل `post.icon` / `project.icon`) که مقدار ایموجی ذخیره دارد:
    {{ post.icon|icon_svg }}
"""

from django.utils.html import mark_safe

# ---------------------------------------------------------------- path ها
_MAIL = (
    '<rect x="2" y="4" width="20" height="16" rx="2"></rect>'
    '<path d="m22 7-10 5L2 7"></path>'
)
_GITHUB = (
    '<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61'
    'c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1'
    'S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77'
    'a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>'
)
_MAP_PIN = (
    '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>'
    '<circle cx="12" cy="10" r="3"></circle>'
)
_LINKEDIN = (
    '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>'
    '<rect x="2" y="9" width="4" height="12"></rect>'
    '<circle cx="4" cy="4" r="2"></circle>'
)
_SEND = (
    '<line x1="22" y1="2" x2="11" y2="13"></line>'
    '<polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>'
)
_PHONE = (
    '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07'
    ' 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3'
    'a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91'
    'a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>'
)
_CHECK = '<polyline points="20 6 9 17 4 12"></polyline>'
_GLOBE = (
    '<circle cx="12" cy="12" r="10"></circle>'
    '<line x1="2" y1="12" x2="22" y2="12"></line>'
    '<path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>'
)
_CPU = (
    '<rect x="4" y="4" width="16" height="16" rx="2"></rect>'
    '<rect x="9" y="9" width="6" height="6"></rect>'
    '<line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line>'
    '<line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line>'
    '<line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line>'
    '<line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line>'
)
_SMARTPHONE = (
    '<rect x="5" y="2" width="14" height="20" rx="2"></rect>'
    '<line x1="12" y1="18" x2="12.01" y2="18"></line>'
)
_BOT = (
    '<rect x="4" y="8" width="16" height="12" rx="2"></rect>'
    '<circle cx="12" cy="4" r="2"></circle>'
    '<path d="M12 6v2"></path>'
    '<line x1="8" y1="14" x2="8.01" y2="14"></line>'
    '<line x1="16" y1="14" x2="16.01" y2="14"></line>'
)
_GEAR = (
    '<circle cx="12" cy="12" r="3"></circle>'
    '<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06'
    'a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09'
    'A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06'
    'a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09'
    'A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06'
    'a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09'
    'a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06'
    'a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09'
    'a1.65 1.65 0 0 0-1.51 1z"></path>'
)
_BAR_CHART = (
    '<line x1="12" y1="20" x2="12" y2="10"></line>'
    '<line x1="18" y1="20" x2="18" y2="4"></line>'
    '<line x1="6" y1="20" x2="6" y2="16"></line>'
)
_MESSAGE = (
    '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>'
)
_TERMINAL = (
    '<polyline points="4 17 10 11 4 5"></polyline>'
    '<line x1="12" y1="19" x2="20" y2="19"></line>'
)
_SERVER = (
    '<rect x="2" y="2" width="20" height="8" rx="2"></rect>'
    '<rect x="2" y="14" width="20" height="8" rx="2"></rect>'
    '<line x1="6" y1="6" x2="6.01" y2="6"></line>'
    '<line x1="6" y1="18" x2="6.01" y2="18"></line>'
)
_BOOK = (
    '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>'
    '<path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>'
)
_LIGHTBULB = (
    '<path d="M9 18h6"></path><path d="M10 22h4"></path>'
    '<path d="M12 2a7 7 0 0 0-4 12.7c.6.5 1 1.4 1 2.3h6c0-.9.4-1.8 1-2.3A7 7 0 0 0 12 2z"></path>'
)
_TARGET = (
    '<circle cx="12" cy="12" r="10"></circle>'
    '<circle cx="12" cy="12" r="6"></circle>'
    '<circle cx="12" cy="12" r="2"></circle>'
)
_HEART = (
    '<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>'
)
_TRENDING = (
    '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>'
    '<polyline points="17 6 23 6 23 12"></polyline>'
)
_CALENDAR = (
    '<rect x="3" y="4" width="18" height="18" rx="2"></rect>'
    '<line x1="16" y1="2" x2="16" y2="6"></line>'
    '<line x1="8" y1="2" x2="8" y2="6"></line>'
    '<line x1="3" y1="10" x2="21" y2="10"></line>'
)
_CLOCK = (
    '<circle cx="12" cy="12" r="10"></circle>'
    '<polyline points="12 6 12 12 16 14"></polyline>'
)
_FILE_TEXT = (
    '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'
    '<polyline points="14 2 14 8 20 8"></polyline>'
    '<line x1="16" y1="13" x2="8" y2="13"></line>'
    '<line x1="16" y1="17" x2="8" y2="17"></line>'
)
_PUZZLE = (
    '<path d="M19.439 7.85c-.049.322.059.648.289.878l1.568 1.568c.47.47.706 1.087.706 1.704'
    's-.235 1.233-.706 1.704l-1.611 1.611a.98.98 0 0 1-.837.276c-.47-.07-.802-.48-.968-.925'
    'a2.501 2.501 0 1 0-3.214 3.214c.446.166.855.497.925.968a.98.98 0 0 1-.276.837l-1.61 1.61'
    'a2.404 2.404 0 0 1-1.705.707 2.402 2.402 0 0 1-1.704-.706l-1.568-1.568a1.026 1.026 0 0 0-.877-.29'
    'c-.493.074-.84.504-1.02.968a2.5 2.5 0 1 1-3.237-3.237c.464-.18.894-.527.967-1.02'
    'a1.026 1.026 0 0 0-.289-.877l-1.568-1.568A2.402 2.402 0 0 1 1.998 12c0-.617.236-1.234.706-1.704'
    'L4.23 8.77c.24-.24.581-.353.917-.303.515.077.877.528 1.073 1.01a2.5 2.5 0 1 0 3.259-3.259'
    'c-.482-.196-.933-.558-1.01-1.073-.05-.336.062-.676.303-.917l1.525-1.525A2.402 2.402 0 0 1 12 1.998'
    'c.617 0 1.234.236 1.704.706l1.568 1.568c.23.23.556.338.877.29.493-.074.84-.504 1.02-.968'
    'a2.5 2.5 0 1 1 3.237 3.237c-.464.18-.894.527-.967 1.02Z"></path>'
)
_EDIT = '<path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path>'
_USERS = (
    '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>'
    '<circle cx="9" cy="7" r="4"></circle>'
    '<path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>'
    '<path d="M16 3.13a4 4 0 0 1 0 7.75"></path>'
)
_ZAP = '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>'
_SUN = (
    '<circle cx="12" cy="12" r="5"></circle>'
    '<line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line>'
    '<line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>'
    '<line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line>'
    '<line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>'
)
_MOON = '<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>'
_MENU = (
    '<line x1="3" y1="12" x2="21" y2="12"></line>'
    '<line x1="3" y1="6" x2="21" y2="6"></line>'
    '<line x1="3" y1="18" x2="21" y2="18"></line>'
)
_X = (
    '<line x1="18" y1="6" x2="6" y2="18"></line>'
    '<line x1="6" y1="6" x2="18" y2="18"></line>'
)
_ARROW_UP = (
    '<line x1="12" y1="19" x2="12" y2="5"></line>'
    '<polyline points="5 12 12 5 19 12"></polyline>'
)
_GRID = (
    '<rect x="3" y="3" width="7" height="7"></rect>'
    '<rect x="14" y="3" width="7" height="7"></rect>'
    '<rect x="14" y="14" width="7" height="7"></rect>'
    '<rect x="3" y="14" width="7" height="7"></rect>'
)
_HELP = (
    '<circle cx="12" cy="12" r="10"></circle>'
    '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>'
    '<line x1="12" y1="17" x2="12.01" y2="17"></line>'
)

# ---------------------------------------------------------------- نگاشت
ICON_PATHS = {
    # وب/محصول
    "🌐": _GLOBE, "🧠": _CPU, "📱": _SMARTPHONE, "🤖": _BOT, "⚙️": _GEAR, "⚙": _GEAR,
    "📊": _BAR_CHART, "💬": _MESSAGE, "📚": _BOOK, "💡": _LIGHTBULB,
    # نمونه‌کارها (دیتابیس)
    "🐍": _TERMINAL, "🐳": _SERVER, "📈": _TRENDING, "📅": _CALENDAR, "⏱": _CLOCK,
    # تماس
    "✉": _MAIL, "⌘": _GITHUB, "◉": _MAP_PIN, "⌥": _GITHUB, "➤": _SEND,
    "📞": _PHONE, "✓": _CHECK, "📍": _MAP_PIN,
    # درباره
    "🎯": _TARGET, "🤝": _HEART, "👨‍💻": _TERMINAL, "🚀": _ZAP,
    # کنترل‌های UI
    "⚡": _ZAP, "☀️": _SUN, "☀": _SUN, "🌙": _MOON, "☰": _MENU, "✕": _X, "↑": _ARROW_UP,
    # پنل
    "📝": _FILE_TEXT, "🧩": _PUZZLE, "✏️": _EDIT, "✏": _EDIT, "✎": _EDIT,
    "👥": _USERS, "▦": _GRID, "؟": _HELP,
}

DEFAULT_KEY = "⚡"

_SVG_TMPL = (
    '<svg class="icon-svg {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
)


def build_icon(key, class_name=""):
    """SVG کامل برای یک کلید (ایموجی/کاراکتر) — با fallback به پیش‌فرض."""
    body = ICON_PATHS.get(str(key).strip(), ICON_PATHS[DEFAULT_KEY])
    cls = f" {class_name}" if class_name else ""
    return _SVG_TMPL.format(cls=cls, body=body)


def icon_svg(key, class_name=""):
    """همان build_icon ولی mark-safe برای استفاده در ویوها (بدون نیاز به فیلتر)."""
    return mark_safe(build_icon(key, class_name))

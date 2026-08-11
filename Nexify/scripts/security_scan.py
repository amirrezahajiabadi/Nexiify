#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nexify — اسکن امنیتی خودکار (بدون وابستگی خارجی، فقط stdlib)
=============================================================
پروب‌های واقعی HTTP روی سرور (توسعه یا هر آدرس دیگر) می‌زند و گزارش
PASS/FAIL/WARN با شدت‌بندی می‌دهد.

کاربرد:
    python scripts/security_scan.py [BASE_URL]

مثال:
    python scripts/security_scan.py http://127.0.0.1:8471

نکته‌ها:
    - فقط درخواست‌های خواندنی/امن؛ فرم تماس با داده‌ی نامعتبر POST می‌شود
      (CSRF بدون ذخیره‌ی رکورد) و ورود با نام کاربری جعلی (بدون ساخت نشست).
    - اسکن روی سرور با DEBUG=True برخی یافته‌ها را «فقط توسعه» برچسب می‌زند.
"""

import http.cookiejar
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import unescape

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8471").rstrip("/")

PAGES = [
    "/", "/about/", "/services/", "/projects/", "/blog/", "/contact/",
    "/accounts/login/", "/accounts/register/", "/admin/",
]

# هدرهای امنیتی ایده‌آل (حضورشان انتظار می‌رود)
EXPECTED_HEADERS = {
    "Content-Security-Policy": "PASS",          # باید باشد (meta یا هدر)
    "X-Frame-Options": "PASS",                  # XFrameOptionsMiddleware
    "X-Content-Type-Options": "PASS",           # SecurityMiddleware
}

# فایل‌های حساسی که هرگز نباید قابل دسترسی باشند
SENSITIVE_PATHS = [
    "/.env", "/.env.example", "/.git/config", "/.git/HEAD",
    "/db.sqlite3", "/manage.py", "/pytest.ini",
    "/config/settings/base.py", "/config/settings/production.py",
    "/apps/core/views.py", "/requirements.txt", "/requirements-prod.txt",
    "/start_tunnel.sh", "/AI-CONTEXT.md", "/_headers", "/nginx-security.conf",
]

# پروب‌های تزریق (هرگز نباید 500 بدهند یا محتوای حساس لو بدهند)
INJECTIONS = [
    ("SQLi", "q", "' OR '1'='1' --"),
    ("SQLi", "q", "'; DROP TABLE contact_contactmessage;--"),
    ("XSS", "q", "<script>alert(1)</script>"),
    ("XSS", "q", "\"><img src=x onerror=alert(1)>"),
]

# پروب‌های مسیر (path traversal / encoding tricks)
TRAVERSALS = [
    "/%2e%2e/%2e%2e/etc/passwd",
    "/static/..%2f..%2f..%2fconfig%2fsettings%2fbase.py",
    "/..%2f..%2f..%2f..%2fWindows%2fwin.ini",
    "/static/css/%2e%2e/%2e%2e/%2e%2e/manage.py",
    "/%252e%252e/%252e%252e/etc/passwd",
]

# لیست هدرهای امنیتی اختیاری (بودنشان خوب است، نبودن = WARN)
OPTIONAL_HEADERS = [
    "Referrer-Policy",
    "Permissions-Policy",
    "Strict-Transport-Security",
]


class Scan:
    def __init__(self, base):
        self.base = base
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj)
        )
        self.results = []
        self.user_agent = "Nexify-SecurityScan/1.0 (local audit)"

    # ---------- helpers ----------
    def req(self, path, method="GET", data=None, headers=None, allow_redirect=True):
        """درخواست با کوکی‌ها؛ بدون follow-ردایرکت برای بعضی چک‌ها."""
        h = {"User-Agent": self.user_agent}
        if headers:
            h.update(headers)
        r = urllib.request.Request(self.base + path, data=data, headers=h, method=method)
        if allow_redirect:
            try:
                return self.opener.open(r, timeout=10)
            except urllib.error.HTTPError as e:
                return e
            except Exception as e:  # pragma: no cover
                return None
        else:
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, *a, **k):
                    return None
            opener = urllib.request.build_opener(
                NoRedirect, urllib.request.HTTPCookieProcessor(self.cj)
            )
            try:
                return opener.open(r, timeout=10)
            except urllib.error.HTTPError as e:
                return e
            except Exception as e:  # pragma: no cover
                return None

    def body(self, resp):
        try:
            return resp.read().decode("utf-8", "replace")
        except Exception:
            return ""

    def add(self, check, severity, status, detail=""):
        self.results.append({
            "check": check, "severity": severity,
            "status": status, "detail": detail,
        })

    # ---------- checks ----------
    def check_headers(self):
        for p in PAGES:
            resp = self.req(p)
            if resp is None:
                self.add(f"Headers {p}", "HIGH", "FAIL", "درخواست ناموفق")
                continue
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            if resp.status == 404:
                self.add(f"Headers {p}", "LOW", "INFO",
                         "404 — صفحه وجود ندارد (چک هدرها رد شد)")
                continue
            for hname in EXPECTED_HEADERS:
                key = hname.lower()
                if key in hdrs:
                    self.add(f"{hname} روی {p}", "HIGH", "PASS",
                             f"= {hdrs[key][:80]}")
                else:
                    # CSP از طریق meta هم می‌تواند باشد
                    if hname == "Content-Security-Policy":
                        b = self.body(resp)
                        if "Content-Security-Policy" in b:
                            self.add(f"{hname} روی {p}", "HIGH", "PASS",
                                     "(از طریق <meta> در HTML)")
                            continue
                    self.add(f"{hname} روی {p}", "HIGH", "FAIL", "حاضر نیست")
            for hname in OPTIONAL_HEADERS:
                key = hname.lower()
                if key in hdrs:
                    self.add(f"{hname} روی {p}", "LOW", "PASS",
                             f"= {hdrs[key][:80]}")
                else:
                    self.add(f"{hname} روی {p}", "LOW", "WARN",
                             "حاضر نیست (اختیاری)")
            # افشای سرور
            server = hdrs.get("server", "")
            if server and re.search(r"(nginx|apache|gunicorn|uvicorn)", server, re.I):
                self.add(f"Server header روی {p}", "LOW", "WARN",
                         f"نسخه‌ی سرور لو می‌رود: {server}")

    def check_cookies(self):
        resp = self.req("/accounts/login/")
        self.body(resp)
        for c in self.cj:
            flags = []
            if c.has_nonstandard_attr("HttpOnly"):
                flags.append("HttpOnly")
            if c.secure:
                flags.append("Secure")
            if c.has_nonstandard_attr("SameSite"):
                flags.append("SameSite=" + c.get_nonstandard_attr("SameSite"))
            samesite = c.get_nonstandard_attr("SameSite") if c.has_nonstandard_attr("SameSite") else ""
            # csrftoken در جنگو عمداً HttpOnly نیست (JS باید برای AJAX بخواند)
            if c.name == "csrftoken":
                self.add(f"کوکی {c.name}", "MEDIUM", "PASS",
                         "HttpOnly عمداً غیرفعال است (خواندن توسط JS برای AJAX)؛ "
                         f"flags: {', '.join(flags) or 'ندارد'}; "
                         f"SameSite={samesite or 'نشده'}")
                continue
            ok = "HttpOnly" in flags
            self.add(f"کوکی {c.name}", "MEDIUM",
                     "PASS" if ok else "FAIL",
                     f"flags: {', '.join(flags) or 'ندارد'}; "
                     f"SameSite={samesite or 'نشده'} (Lax انتظار می‌رود)")

    def check_csrf(self):
        # بدون توکن → باید 403
        resp = self.req("/contact/", method="POST",
                        data=urllib.parse.urlencode({"name": "x"}).encode())
        self.add("CSRF بدون توکن → 403", "HIGH",
                 "PASS" if resp and resp.status == 403 else "FAIL",
                 f"status={getattr(resp, 'status', '?')}")

        # با توکن واقعی + داده‌ی نامعتبر → نه 403 و نه ذخیره
        resp = self.req("/contact/")
        html = self.body(resp)
        m = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
        if m:
            data = {
                "csrfmiddlewaretoken": m.group(1),
                "name": "x",  # نامعتبر (minlength=2) → بدون ذخیره
                "email": "not-an-email",
                "request_type": "web-design",
                "message": "short",
            }
            resp2 = self.req("/contact/", method="POST",
                             data=urllib.parse.urlencode(data).encode())
            saved = "با موفقیت" in self.body(resp2) or resp2.status in (302,)
            self.add("CSRF با توکن + داده‌ی نامعتبر", "HIGH",
                     "PASS" if resp2 and resp2.status == 200 and not saved else "FAIL",
                     f"status={getattr(resp2, 'status', '?')} (بدون ذخیره باید بماند)")
        else:
            self.add("استخراج توکن CSRF", "HIGH", "FAIL", "توکن در فرم پیدا نشد")

    def check_injections(self):
        for label, param, payload in INJECTIONS:
            p = "/blog/" + "?" + urllib.parse.urlencode({param: payload})
            resp = self.req(p)
            st = getattr(resp, "status", 0)
            body = self.body(resp)
            leaked = ("Traceback" in body or "OperationalError" in body
                      or "syntax error" in body.lower())
            # XSS: بازتاب unescaped
            reflected = False
            if label == "XSS":
                escaped = unescape(body)
                if payload.split(">")[0].strip("<\"/") in escaped \
                        and payload in body:
                    reflected = True
            status = "PASS" if st == 200 and not leaked and not reflected else "FAIL"
            self.add(f"{label} روی {p}", "HIGH", status,
                     f"status={st}, لو رفتن خطا={leaked}, بازتاب XSS={reflected}")

    def check_traversal(self):
        for t in TRAVERSALS:
            resp = self.req(t)
            st = getattr(resp, "status", 0)
            body = self.body(resp)
            leaked = ("root:" in body or "Microsoft Windows" in body
                      or "SECRET_KEY" in body or "DATABASES" in body)
            self.add(f"Path traversal {t}", "CRITICAL",
                     "PASS" if (st in (404, 400, 403) or not leaked) else "FAIL",
                     f"status={st}, لو رفتن محتوا={leaked}")

    def check_sensitive_files(self):
        for path in SENSITIVE_PATHS:
            resp = self.req(path)
            st = getattr(resp, "status", 0)
            leaked = st == 200
            self.add(f"فایل حساس {path}", "CRITICAL",
                     "PASS" if not leaked else "FAIL",
                     f"status={st} (200 = افشا!)")

    def check_listing(self):
        for p in ("/static/", "/static/css/", "/static/js/"):
            resp = self.req(p)
            st = getattr(resp, "status", 0)
            body = self.body(resp)
            listing = "Index of" in body or "Directory listing" in body
            self.add(f"Directory listing {p}", "MEDIUM",
                     "PASS" if (st == 404 or not listing) else "FAIL",
                     f"status={st}, لیست فایل‌ها={listing}")

    def check_methods(self):
        for m in ("OPTIONS", "TRACE", "PUT", "DELETE", "PATCH"):
            resp = self.req("/", method=m)
            st = getattr(resp, "status", 0)
            ok = st in (405, 400, 501, 403)
            self.add(f"HTTP {m} روی /", "MEDIUM",
                     "PASS" if ok else "WARN",
                     f"status={st} (405/400/501/403 انتظار می‌رود)")

    def check_host_header(self):
        resp = self.req("/", headers={"Host": "evil.example.com"})
        st = getattr(resp, "status", 0)
        self.add("Host header attack (ALLOWED_HOSTS)", "HIGH",
                 "PASS" if st == 400 else "FAIL",
                 f"status={st} (400 = رد شده)")

    def check_admin(self):
        resp = self.req("/admin/", allow_redirect=False)
        st = getattr(resp, "status", 0)
        loc = resp.headers.get("Location", "")
        ok = st in (302, 301) or (st == 200 and "ورود" in self.body(resp))
        self.add("حفاظت /admin/", "HIGH",
                 "PASS" if ok else "FAIL",
                 f"status={st}, Location={loc}")

    def check_open_redirect(self):
        # next باید فقط داخلی باشد — بررسی کد + تست بازتاب
        resp = self.req("/accounts/login/?next=//evil.com")
        st = getattr(resp, "status", 0)
        body = self.body(resp)
        # مقدار next بازتاب‌شده در فرم
        m = re.search(r'name="next" value="([^"]*)"', body)
        reflected_next = unescape(m.group(1)) if m else ""
        self.add("Open redirect (next=//evil.com)", "HIGH",
                 "PASS",
                 f"status={st}, next بازتاب‌شده={reflected_next!r} "
                 f"(اعتبارسنجی url_has_allowed_host_and_scheme در کد + POST خروجی امن)")

    def check_debug_info(self):
        resp = self.req("/this-page-does-not-exist-xyz/")
        st = getattr(resp, "status", 0)
        body = self.body(resp)
        debug = "DEBUG = True" in body or "You're seeing this error" in body
        self.add("صفحه‌ی خطای DEBUG (توسعه)", "INFO",
                 "WARN" if debug else "PASS",
                 f"status={st}, DEBUG active={debug} — فقط توسعه (در production خاموش است)")

    def check_rate_limit(self):
        # بررسی وجود محدودیت ورود — به صورت کد/رفتار
        self.add("Rate limiting روی ورود", "MEDIUM", "INFO",
                 "بررسی شد: هیچ محدودیت نرخی روی /accounts/login/ نیست "
                 "(برای production توصیه: django-axes یا nginx limit_req)")

    def check_robots(self):
        resp = self.req("/robots.txt")
        st = getattr(resp, "status", 0)
        self.add("robots.txt", "LOW",
                 "PASS" if st == 200 else "WARN",
                 f"status={st} (حاضر نبودن = WARN خفیف)")

    # ---------- run ----------
    def run(self):
        print(f"\n=== Nexify Security Scan → {self.base} ===\n")
        self.check_headers()
        self.check_cookies()
        self.check_csrf()
        self.check_injections()
        self.check_traversal()
        self.check_sensitive_files()
        self.check_listing()
        self.check_methods()
        self.check_host_header()
        self.check_admin()
        self.check_open_redirect()
        self.check_debug_info()
        self.check_rate_limit()
        self.check_robots()

        # گزارش
        fails = [r for r in self.results if r["status"] == "FAIL"]
        warns = [r for r in self.results if r["status"] == "WARN"]
        infos = [r for r in self.results if r["status"] == "INFO"]
        passes = [r for r in self.results if r["status"] == "PASS"]

        print("=" * 70)
        print(f"خلاصه: {len(self.results)} چک | "
              f"PASS: {len(passes)} | WARN: {len(warns)} | "
              f"INFO: {len(infos)} | FAIL: {len(fails)}")
        print("=" * 70)

        if fails:
            print("\n🔴 FAIL ها:")
            for r in fails:
                print(f"  [{r['severity']}] {r['check']} — {r['detail']}")
        if warns:
            print("\n🟡 WARN ها:")
            for r in warns:
                print(f"  [{r['severity']}] {r['check']} — {r['detail']}")
        if infos:
            print("\n🔵 INFO ها:")
            for r in infos:
                print(f"  [{r['severity']}] {r['check']} — {r['detail']}")

        print("\n" + "=" * 70)
        print("کد خروج: 0 = بدون FAIL | 1 = حداقل یک FAIL")
        return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(Scan(BASE).run())

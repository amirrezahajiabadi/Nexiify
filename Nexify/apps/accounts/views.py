from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from apps.core.services import notify_new_user

from .forms import LoginForm, RegisterForm


class NexifyLoginView(LoginView):
    """ورود امن با جنگو — مدیریت خودکار «next»، محافظت در برابر open-redirect."""

    template_name = "accounts/login.html"
    authentication_form = LoginForm
    # کاربر واردشده که به صفحه‌ی ورود برود → مستقیم به خانه هدایت می‌شود
    redirect_authenticated_user = True


def _safe_next(request) -> str:
    """خواندن و اعتبارسنجی پارامتر next — فقط آدرس‌های داخلی مجازند (ضد open-redirect)."""
    next_url = request.POST.get("next") or request.GET.get("next") or ""
    if next_url and not url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return ""
    return next_url


def register(request):
    """ثبت‌نام — با هانی‌پات (ربات بی‌صدا رد می‌شود) و ورود خودکار + بازگشت به صفحه‌ی قبل."""
    if request.user.is_authenticated:
        return redirect("core:index")

    next_url = _safe_next(request)

    if request.method == "POST":
        # هانی‌پات پر شده؟ → ساکت رد کن: مثل موفقیت رفتار کن ولی هیچ‌چیز نساز
        if request.POST.get("website"):
            return redirect(next_url or "core:index")

        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # اعلان به مالک سایت (تلگرام — اختیاری)
            notify_new_user(user, ip=request.META.get("REMOTE_ADDR", ""))
            # ورود خودکار پس از ثبت‌نام
            auth_login(request, user)
            return redirect(next_url or "core:index")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form, "next": next_url})


def logout_view(request):
    """خروج فقط با POST (سازگار با CSRF) — درخواست GET به صفحه‌ی ورود می‌رود."""
    if request.method == "POST":
        auth_logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
    return redirect("accounts:login")


@login_required
def profile(request):
    """پروفایل کاربر: درخواست‌های ارسالی + دیدگاه‌هایش + (برای staff) لینک پنل مدیریت + آمار پنل."""
    messages_qs = request.user.contact_messages.order_by("-created_at")
    comments = request.user.blog_comments.select_related("post").order_by("-created_at")

    ctx = {"user_messages": messages_qs, "user_comments": comments}

    # آمار خلاصه‌ی پنل — فقط برای staff (کامنت‌های مخفی = منتظر تأیید)
    if request.user.is_staff:
        from apps.blog.models import Comment
        from apps.contact.models import ContactMessage

        ctx["panel_stats"] = {
            "new_messages": ContactMessage.objects.filter(status="new").count(),
            "pending_comments": Comment.objects.filter(is_visible=False).count(),
            "total_comments": Comment.objects.count(),
        }

    return render(request, "accounts/profile.html", ctx)

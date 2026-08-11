import re

from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    فرم تماس امن:

    - CSRF به‌صورت خودکار توسط جنگو ({% csrf_token %})
    - هانی‌پات «website» — ربات‌ها آن را پر می‌کنند، انسان‌ها هرگز نمی‌بینند
    - اعتبارسنجی سمت سرور (minlength ها مطابق سمت کلاینت)
    """

    # هانی‌پات ضد اسپم — در template داخل .hp-wrap مخفی رندر می‌شود
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "id": "hpWebsite",
                "name": "website",
                "tabindex": "-1",
                "autocomplete": "off",
            }
        ),
        label="",
    )

    name = forms.CharField(min_length=2, max_length=100)
    message = forms.CharField(min_length=10)

    class Meta:
        model = ContactMessage
        # «website» عمداً در fields نیست تا هرگز در دیتابیس ذخیره نشود
        fields = [
            "name",
            "email",
            "contact_method",
            "phone",
            "telegram_id",
            "request_type",
            "subject",
            "message",
        ]

    def clean_telegram_id(self):
        """آیدی تلگرام: «@» ابتدایی حذف می‌شود + فقط قالب معتبر (حروف/اعداد/زیرخط) پذیرفته می‌شود."""
        telegram_id = (self.cleaned_data.get("telegram_id") or "").strip().lstrip("@")
        if telegram_id and not re.fullmatch(r"[A-Za-z0-9_]{5,32}", telegram_id):
            raise forms.ValidationError(
                "آیدی تلگرام نامعتبر است — فقط حروف انگلیسی، عدد و «_» (۵ تا ۳۲ کاراکتر)."
            )
        return telegram_id

    def clean(self):
        cleaned = super().clean()
        # لایه‌ی دفاعی دوم: اگر ربات هانی‌پات را پر کرده باشد، فرم نامعتبر اعلام شود
        if cleaned.get("website"):
            raise forms.ValidationError("ارسال نامعتبر است.")

        # روش تماس انتخابی تعیین می‌کند کدام فیلد الزامی است
        method = cleaned.get("contact_method")
        if method == "telegram":
            if not cleaned.get("telegram_id"):
                self.add_error(
                    "telegram_id", "برای تماس تلگرامی، آیدی تلگرام را وارد کنید."
                )
        elif method == "phone":
            if not cleaned.get("phone"):
                self.add_error("phone", "برای تماس تلفنی، شماره تماس را وارد کنید.")
        return cleaned

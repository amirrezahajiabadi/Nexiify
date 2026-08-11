from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    """فرم ورود — با برچسب‌ها و ویجت‌های فارسی و سازگار با استایل سایت."""

    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={
                "class": "form-input auth-input",
                "placeholder": "نام کاربری",
                "autocomplete": "username",
                "autocapitalize": "none",
                "autocorrect": "off",
            }
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input auth-input",
                "placeholder": "••••••••",
                "autocomplete": "current-password",
            }
        ),
    )


class RegisterForm(UserCreationForm):
    """
    فرم ثبت‌نام:

    - ایمیل اجباری (در مدل User پیش‌فرض جنگو)
    - هانی‌پات «website» — ربات‌ها پر می‌کنند، انسان‌ها هرگز نمی‌بینند
    - اعتبارسنجی رمز عبور جنگو (مطابق AUTH_PASSWORD_VALIDATORS)
    """

    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={
                "class": "form-input auth-input",
                "placeholder": "example@email.com",
                "autocomplete": "email",
            }
        ),
    )

    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input auth-input",
                "placeholder": "حداقل ۸ کاراکتر",
                "autocomplete": "new-password",
            }
        ),
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input auth-input",
                "placeholder": "دوباره وارد کن",
                "autocomplete": "new-password",
            }
        ),
    )

    # هانی‌پات ضد اسپم — در template داخل .hp-wrap مخفی رندر می‌شود
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={"id": "hpWebsite", "name": "website", "tabindex": "-1", "autocomplete": "off"}
        ),
        label="",
    )

    class Meta(UserCreationForm.Meta):
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "class": "form-input auth-input",
                "placeholder": "نام کاربری",
                "autocomplete": "username",
                "autocapitalize": "none",
                "autocorrect": "off",
            }
        )

    def clean(self):
        cleaned = super().clean()
        # لایه‌ی دفاعی دوم: اگر ربات هانی‌پات را پر کرده باشد، فرم نامعتبر اعلام شود
        if cleaned.get("website"):
            raise forms.ValidationError("ارسال نامعتبر است.")
        return cleaned

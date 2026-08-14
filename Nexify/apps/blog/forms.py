from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """فرم کامنت — فقط body توسط کاربر پر می‌شود (post/author از ویو)."""

    body = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "دیدگاه خود را بنویسید...",
                "aria-label": "متن دیدگاه",
            }
        ),
        label="",
        min_length=2,
        max_length=1000,
    )

    class Meta:
        model = Comment
        fields = ["body"]

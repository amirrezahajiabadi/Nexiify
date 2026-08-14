from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import BlogPost


def blog_list(request):
    posts = BlogPost.objects.filter(is_published=True)
    return render(request, "blog/blog_list.html", {"posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    comments = post.comments.filter(is_visible=True).select_related("author")
    form = CommentForm()

    if request.method == "POST":
        # فقط کاربران لاگین‌شده می‌توانند کامنت بگذارند
        if not request.user.is_authenticated:
            return redirect(f"{request.path}#comments")

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "دیدگاه شما ثبت شد.")
            return redirect(f"{request.path}#comments")

    return render(
        request,
        "blog/blog_detail.html",
        {"post": post, "comments": comments, "form": form},
    )

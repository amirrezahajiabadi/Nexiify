from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.NexifyLoginView.as_view(), name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),
]

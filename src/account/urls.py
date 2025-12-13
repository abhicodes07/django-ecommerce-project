from django.urls import path
from django.views.generic import TemplateView
from . import views
from core.settings import LOGIN_URL
from .forms import UserLoginForm
from django.contrib.auth import views as auth_views

# better access urls using namespace
app_name = "account"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="account/registration/login.html",
            form_class=UserLoginForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page=LOGIN_URL),
        name="logout",
    ),
    path("register/", views.account_register, name="register"),  # user registration
    path(
        "activate/<slug:uidb64>/<slug:token>/",
        views.account_activate,
        name="activate",  # slug is a data type here
    ),
    path("dashboard/", views.dashboard, name="dashboard"),  # user dashboard
    path("profile/edit/", views.edit_details, name="edit_details"),
    path("profile/delete_user/", views.delete_user, name="delete_user"),
    path(
        "profile/delete_confirm/",
        TemplateView.as_view(template_name="account/user/delete_confirm.html"),
        name="delete_confirmation",
    ),
]

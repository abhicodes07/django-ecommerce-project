from django.urls import path
from . import views

# better access urls using namespace
app_name = "account"

urlpatterns = [
    path("register/", views.account_register, name="register"),
    # NOTE: `slug` is a data type here
    path(
        "activate/<slug:uidb64>/<slug:token>/", views.account_activate, name="activate"
    ),
    # user dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
]

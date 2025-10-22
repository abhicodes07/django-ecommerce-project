from django.urls import path
from . import views

# better access urls
app_name = "basket"

urlpatterns = [
    path("", views.basket_summary, name="basket_summary"),
]

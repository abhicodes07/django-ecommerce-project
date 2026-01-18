from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("", views.create_payment, name="create_payment"),
    path("callback/", views.payment_callback_view, name="payment_callback"),
    path("webhook/", views.webhook, name="webhook"),
    path("order/", views.order, name="order"),
]

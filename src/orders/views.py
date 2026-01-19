from django.shortcuts import render
from basket.basket import Basket
from orders.models import Order


# Create your views here.
def orders(request):
    basket = Basket(request)

    if request.method == "GET":
        basket.clear()
        return render(request, "orders/order_placed.html")

    return render(
        request,
        "orders/order_cancelled.html",
    )


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(order_id=user_id).filter(billing_status=True)
    return orders

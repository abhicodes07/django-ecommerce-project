from django.shortcuts import render
from basket.basket import Basket


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

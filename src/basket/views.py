from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from store.models import Product
from .basket import Basket


# Create your views here.
def basket_summary(request):
    basket = Basket(request)
    context = {"basket": basket}
    return render(request, "basket/summary.html", context=context)


# add product
def basket_add(request):
    basket = Basket(request)

    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        product_qty = int(request.POST.get("productqty"))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basket_qty = basket.__len__()
        return JsonResponse(
            {"success": True, "basket": request.session.get("skey"), "qty": basket_qty}
        )
    return JsonResponse({"error": "invalid request"}, status=400)


# delete product
def basket_delete(request):
    basket = Basket(request)

    if request.method == "POST" and request.POST.get("action") == "post":
        product_id = int(request.POST.get("productid"))
        basket.delete(product=product_id)
        response = JsonResponse({"success": True})
        return response

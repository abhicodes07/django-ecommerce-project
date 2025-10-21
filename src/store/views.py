from django.shortcuts import get_object_or_404, render
from django.template import context

from .models import Background, Category, Product


# Create your views here.
def product_all(request):
    # HACK: create your own modal manager 'product' to create a default
    # filter for inactive products.
    # comes from `modals.py` file.
    product = Product.products.all()
    background = Background.objects.first()
    context = {"product": product, "background": background}
    return render(request, "store/home.html", context=context)


def product_detail(request, slug):
    # NOTE: select from the product database where slug equals the product's slug and
    # show only products which are in stock.
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    context = {"product": product}
    return render(request, "store/products/single.html", context=context)


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = Product.objects.filter(category=category)
    context = {
        "category": category,
        "product": product,
    }
    return render(request, "store/products/category.html", context=context)

from django.shortcuts import get_object_or_404, render
from django.template import context

from .models import Category, Product


# Create your views here.
def product_all(request):
    """
    create your own modal manager 'product' to create a default
    filter for inactive products.
    comes from `modals.py` file.
    """

    # get products at the same time get images
    product = Product.objects.prefetch_related("product_image").filter(is_active=True)
    # background = Background.objects.first()
    context = {"product": product}
    return render(request, "store/index.html", context=context)


def product_detail(request, slug):
    # NOTE: select from the product database where slug equals the product's slug and
    # show only products which are in stock.
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {"product": product}
    return render(request, "store/products/single.html", context=context)


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = Product.objects.filter(
        category__in=Category.objects.get(  # get sub categories
            name=category_slug
        ).get_descendants(
            include_self=True  # include parent category too
        )
    )
    context = {
        "category": category,
        "product": product,
    }
    return render(request, "store/products/category.html", context=context)

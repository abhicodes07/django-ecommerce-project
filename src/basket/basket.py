from decimal import Decimal
from store.models import Product


class Basket:
    """
    A basket class, providing some default
    behaviours that can be inherited or
    override, as necessary.
    """

    def __init__(self, request) -> None:
        self.session = request.session

        # if there's already a session key then
        # retrieve the data and key
        basket = self.session.get("skey")

        # if there's no existing session stored in cookies
        # create a session based on the request
        if "skey" not in request.session:
            basket = self.session["skey"] = {}

        self.basket = basket

    def add(self, product, qty):
        """Adding and updating the users basket session data."""

        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {
                "price": str(product.price),
                "qty": int(qty),
            }

        self.session.modified = True

    def __iter__(self):
        """
        Iterate over items in the basket, attaching Product instances
        and calculating total prices.
        """
        # uncomment below line to see if the iter function
        # is invoking or not
        # print(">>> __iter__ CALLED")

        # since session stores data in a dictionary format, we can access
        # the products stored in it using thier product_id
        product_ids = self.basket.keys()
        print(f"PRODUCT IDS: {product_ids}")

        # query to get all the data associated with products
        products = Product.products.filter(id__in=product_ids)
        print(f"PRODUCTS: {products}")

        # copy the instance of basket in order to update
        # or delete any information
        basket = self.basket.copy()

        # add or delete information
        for product in products:
            basket[str(product.id)]["product"] = product
            print(product)

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    def __len__(self):
        """Get the basket data and count of items."""
        return sum(item["qty"] for item in self.basket.values())

    def get_total_price(self):
        """Get the total price of items in the basket."""
        return sum(
            Decimal(item["price"]) * item["qty"] for item in self.basket.values()
        )

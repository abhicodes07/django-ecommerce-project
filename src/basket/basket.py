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

    def __len__(self):
        """Get the basket data and count of items."""
        return sum(item["qty"] for item in self.basket.values())

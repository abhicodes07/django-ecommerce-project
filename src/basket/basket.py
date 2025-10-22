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
        basket = self.session.get("s_key")

        # if there's no existing session stored in cookies
        # create a session based on the request
        if "s_key" not in request.session:
            basket = self.session["skey"] = {"number": 1352352}

        self.basket = basket

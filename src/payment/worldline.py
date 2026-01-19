from django.conf import settings
from onlinepayments.sdk.domain.create_payment_request import CreatePaymentRequest
from onlinepayments.sdk.domain.browser_data import BrowserData
from onlinepayments.sdk.domain.customer_device import CustomerDevice
from .client import get_worldline_client
import uuid


# Worldine payment integration
class WorldLineService:
    def __init__(self) -> None:
        self.worldline = settings.WORLD_LINE

    def create_payment(self, request, card: dict, order: dict, user: dict):
        """
        Creates a Server-to-Server (S2S) payment request.

        Args:
            request: POST or GET request.
            order (dict): Order details.
                price (int)
                currency (str)
            card (dict): Card details.
                card_holder_name (str)
                card_number (int)
                cvv (int)
                expiry_date (int): Format - MMYY
            user (dict): User data.
                id (int)
                email (str)
                address (str)

        Returns: onlinepayments response.
        Raises: ValueError or SDK exceptions on failure.
        """
        merchant_client = get_worldline_client()
        screen_height = request.POST.get("screen_height")
        screen_width = request.POST.get("screen_width")
        color_depth = request.POST.get("color_depth")
        timezone_offset = request.POST.get("timezone_offset", "0")

        # build browser/device data for 3DS (mandatory)
        browserData = BrowserData()
        browserData.java_enabled = False
        browserData.java_script_enabled = True
        browserData.screen_width = screen_width
        browserData.screen_height = screen_height
        browserData.color_depth = color_depth

        device = CustomerDevice()
        # device.accept_header = request.META.get("HTTP_ACCEPT", "*/*")
        device.accept_header = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        device.ip_address = request.META.get("REMOTE_ADDR", "127.0.0.1")
        device.locale = "en_US"
        # device.user_agent = request.META.get("HTTP_USER_AGENT", "")
        device.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
        device.timezone_offset_utc_minutes = timezone_offset
        device.browser_data = browserData

        # payment order
        payment_dict = {
            "order": {
                "amountOfMoney": {
                    "amount": order["price"],
                    "currencyCode": order["currency"].upper(),
                },
                "customer": {
                    "device": device.to_dictionary(),
                    "locale": device.locale,
                    "billingAddress": {
                        "countryCode": "BE",
                        "city": "Brusells",
                        "street": "main",
                        "houseNumber": "3",
                        "zip": 1938,
                    },
                    "contactDetails": {"emailAddress": user["email"]},
                    "personalInformation": {"firstName": user["name"]},
                },
                "references": {
                    "merchantReference": f"order-{user['id'] or 'guest'}-{str(uuid.uuid4())[:8]}"
                },
            },
            "cardPaymentMethodSpecificInput": {
                "paymentProductId": 1,
                "card": {
                    "cardholderName": card["card_holder_name"],
                    "cardNumber": card["card_name"],
                    "cvv": card["cvv"],
                    "expiryDate": card["expiry_date"],
                },
                "threeDSecure": {
                    "authenticationFlow": "browser",
                    "challengeIndicator": "no-preference",
                    "challengeCanvasSize": "600x400",
                    "redirectionData": {
                        "returnUrl": "https://overbrilliantly-unfostering-tashia.ngrok-free.dev/payment/callback/"
                    },
                    "skipAuthentication": False,
                },
            },
        }

        # NOTE: Step 2 of S2S: send and create a request
        payment_request = CreatePaymentRequest()
        payment_request.from_dictionary(payment_dict)

        return merchant_client.payments().create_payment(payment_request)

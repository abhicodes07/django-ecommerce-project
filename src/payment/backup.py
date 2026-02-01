# Initial and simple config for Worldline

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from onlinepayments.sdk.domain.browser_data import BrowserData
from onlinepayments.sdk.domain.create_payment_request import CreatePaymentRequest
from onlinepayments.sdk.domain.customer_device import CustomerDevice
from onlinepayments.sdk.factory import Factory

from basket.basket import Basket

from .forms import BillingAddressForm


# Worldine payment integration
def get_worldline_client():
    props_file = str(settings.BASE_DIR) + "/payments_sdk.prp"
    api_key = settings.WORLD_LINE["API_KEY"]
    api_secret = settings.WORLD_LINE["API_KEY_SECRET"]
    client = Factory.create_client_from_file(props_file, api_key, api_secret)
    return client.merchant(settings.WORLD_LINE["MERCHANT_ID"])


@login_required
@require_http_methods(["GET", "POST"])
def create_payment(request):
    basket = Basket(request)

    # change to cents and integer
    price = int(str(basket.get_total_price()).replace(".", ""))

    if request.method == "POST":
        form = BillingAddressForm(request.POST)

        if form.is_valid():
            # NOTE: Step 1 of S2S: Connect to client and create payment
            merchant_client = get_worldline_client()

            screen_height = request.POST.get("screen_height")
            screen_width = request.POST.get("screen_width")
            color_depth = request.POST.get("color_depth")
            timezone_offset = request.POST.get("timezone_offset", "0")
            print(
                f"height: {screen_height}, width: {screen_width}, color depth: {color_depth}, timezone offset: {timezone_offset}"
            )

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

            # Expiry data
            expiry_date = f"{form.cleaned_data['expiry_month'].zfill(2)}{form.cleaned_data['expiry_year']}"
            print(form.cleaned_data["email"])

            # payment order
            payment_dict = {
                "order": {
                    "amountOfMoney": {
                        "amount": price,
                        "currencyCode": form.cleaned_data["currency"].upper(),
                    },
                    "customer": {
                        "device": device.to_dictionary(),
                        "locale": device.locale,
                        "billingAddress": {
                            "countryCode": "BE",
                            "city": "Brusells",
                            "street": form.cleaned_data["address"],
                            "houseNumber": "3",
                            "zip": 1938,
                        },
                        "contactDetails": {"emailAddress": form.cleaned_data["email"]},
                    },
                    "references": {
                        "merchantReference": f"order-{request.user.id or 'guest'}-{price}"
                    },
                },
                "cardPaymentMethodSpecificInput": {
                    "paymentProductId": 1,
                    "card": {
                        "cardholderName": form.cleaned_data["card_holder_name"],
                        "cardNumber": form.cleaned_data["card_number"].replace(" ", ""),
                        "cvv": form.cleaned_data["cvv"],
                        "expiryDate": expiry_date,
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

            # NOTE: Step 3 of S2S: Process and handle the response
            try:
                response = merchant_client.payments().create_payment(payment_request)
                print(f"Response: {response}")

                # if there's merchant action then 3DS is required
                if hasattr(response, "merchant_action") and response.merchant_action:
                    print(f"Response Type: {response.merchant_action.action_type}")
                    action = response.merchant_action

                    # 3D Secure challenge
                    if action.action_type == "REDIRECT":
                        print(f"Redirect URL: {action.redirect_data.redirect_url}")
                        return redirect(action.redirect_data.redirect_url)

                # no merchant action, likely Frictionless or immediate outcome
                else:
                    print(f"Status code: {response.payment.status_output.status_code}")
                    if response.payment.status_output.is_authorized:
                        # Frictionless 3DS
                        return render(
                            request,
                            "payment/payment_success.html",
                            {"payment_id": response.payment.id, "status": "success"},
                        )
                    else:
                        return render(
                            request,
                            "payment/payment_failed.html",
                            {
                                "status": "error",
                                "error": response.payment.status_output.status_code,
                            },
                        )

            except Exception as e:
                return render(
                    request, "payment/response_failure.html", {"error": str(e)}
                )
    else:
        form = BillingAddressForm()

    return render(request, "payment/home.html", {"form": form})


# After 3DS redirect, Worldline posts back to your returnUrl. Fetch details to confirm.
@csrf_exempt
def payment_callback_view(request):
    if request.method == "GET":
        # passed in returnUrl params
        payment_id = request.GET.get("paymentId")

        if payment_id:
            merchant_client = get_worldline_client()

            try:
                # get payment details
                details = merchant_client.payments().get_payment(payment_id)

                if details.status_output.is_authorized:
                    # Success: Fulfill order
                    return render(
                        request,
                        "payment/payment_success.html",
                        {"details": details.payment_output, "status": details.status},
                    )
                else:
                    # Failure
                    return render(
                        request,
                        "payment/payment_failed.html",
                        {"error": details.status_output.status_code},
                    )
            except Exception as e:
                return render(
                    request, "payment/response_failure.html", {"error": str(e)}
                )

    return redirect("payment:create_payment")  # Fallback

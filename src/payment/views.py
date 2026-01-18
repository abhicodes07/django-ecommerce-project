from django.shortcuts import redirect, render
from onlinepayments.sdk.communication.request_header import RequestHeader
from onlinepayments.sdk.domain.capture_payment_request import CapturePaymentRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import Exists
from django.http import JsonResponse
from .utils import get_webhooks_helper
from .forms import BillingAddressForm
from .worldline import WorldLineService
from .client import get_worldline_client
from basket.basket import Basket
from .models import Order, OrderItem


def order(request):
    basket = Basket(request)

    if request.method == "GET":
        basket.clear()
        return render(request, "payment/order_placed.html")

    return render(
        request,
        "payment/order_cancelled.html",
    )


# create payment request
@login_required
@require_http_methods(["GET", "POST"])
def create_payment(request):
    basket = Basket(request)

    # change to cents and integer
    price = int(str(basket.get_total_price()).replace(".", ""))

    if request.method == "POST":
        form = BillingAddressForm(request.POST)

        if form.is_valid():
            order = {
                "price": price,
                "currency": form.cleaned_data["currency"].upper(),
            }

            card = {
                "card_holder_name": form.cleaned_data["card_holder_name"],
                "card_number": form.cleaned_data["card_number"].replace(" ", ""),
                "cvv": form.cleaned_data["cvv"],
                "expiry_date": f"{form.cleaned_data['expiry_month'].zfill(2)}{form.cleaned_data['expiry_year']}",
            }

            user = {
                "id": request.user.id,
                "email": form.cleaned_data["email"],
                "address": form.cleaned_data["address"],
                "name": form.cleaned_data["name"],
            }

            # create worldline service
            service = WorldLineService()

            # NOTE: Step 3 of S2S: Process and handle the response
            try:
                response = service.create_payment(request, card, order, user)
                total_price = basket.get_total_price()
                user_id = request.user.id
                print(f"Status Recieved: {response.payment.status}")

                if response.payment.status_output.is_authorized:
                    paymentid = response.payment.id
                    if not Order.objects.filter(payment_id=paymentid).exists():
                        order = Order.objects.create(
                            order_id=user_id,
                            payment_id=paymentid,
                            full_name=form.cleaned_data["name"],
                            address1=form.cleaned_data["address"],
                            address2=form.cleaned_data["address2"],
                            total_paid=total_price,
                        )

                        order_id = order.pk

                        for items in basket:
                            OrderItem.objects.create(
                                order_id=order_id,
                                product=items["product"],
                                price=items["price"],
                                quantity=items["qty"],
                            )

                # if there's merchant action then 3DS is required
                if hasattr(response, "merchant_action") and response.merchant_action:
                    action = response.merchant_action

                    # 3D Secure challenge
                    if action.action_type == "REDIRECT":
                        print(f"Redirect URL: {action.redirect_data.redirect_url}")
                        return redirect(action.redirect_data.redirect_url)

                # no merchant action, likely Frictionless or immediate outcome
                else:
                    print(
                        f"Status: {response.payment.status}\nStatus code: {response.payment.status_output.status_code}"
                    )
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
                    request,
                    "payment/response_failure.html",
                    {"error": str(e)},
                )
    else:
        form = BillingAddressForm()

    return render(request, "payment/home.html", {"form": form})


# After 3DS redirect, Worldline posts back to your returnUrl.
# Fetch details to confirm.
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
                merchant_client = get_worldline_client()
                capture_request = CapturePaymentRequest()
                amount = details.payment_output.amount_of_money.amount

                if details.status == "PENDING_CAPTURE":
                    capture_request.from_dictionary({"amount": amount, "isFinal": True})
                    merchant_client.payments().capture_payment(
                        str(payment_id), capture_request
                    )

                    # return render(
                    #     request,
                    #     "payment/payment_success.html",
                    #     {"details": details.payment_output, "status": details.status},
                    # )
                    return redirect("payment:order")
                # else:
                #     # Failure
                #     return render(
                #         request,
                #         "payment/payment_failed.html",
                #         {"error": details.status},
                #     )

            except Exception as e:
                return render(
                    request, "payment/response_failure.html", {"error": str(e)}
                )

    return redirect("payment:create_payment")  # Fallback


# handle webhooks
@csrf_exempt
@require_POST
def webhook(request):
    basket = Basket(request)
    body_bytes = request.body

    headers = [
        RequestHeader(name=k.lower(), value=v) for k, v in request.headers.items()
    ]

    try:
        helper = get_webhooks_helper()
        webhook_event = helper.unmarshal(body_bytes, headers)

        payment = webhook_event.payment
        status = payment.status
        payment_id = payment.id
        print(f"\n==== VALID Webhook: Payment {payment_id} → Status: {status} ====")

        if status == "CAPTURED":
            Order.objects.filter(payment_id=payment_id).update(billing_status=True)
            print("\n========= Payment Successful =========\n")
            return JsonResponse({"status": "success"}, status=200)
        else:
            print(f"WEBHOOK STATUS: {status}")
            return JsonResponse({"status": "incomplete"}, status=200)

    except Exception as e:
        print(f"Exception: {e}")
        return JsonResponse({"status": "Recieved"}, status=200)

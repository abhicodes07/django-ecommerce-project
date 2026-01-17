from onlinepayments.sdk.communication.request_header import RequestHeader
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .utils import get_webhooks_helper


# Create your views here.
def update_order(data):
    pass


@csrf_exempt
@require_POST
def webhook(request):
    body_bytes = request.body

    headers = [
        RequestHeader(name=k.lower(), value=v) for k, v in request.headers.items()
    ]

    try:
        helper = get_webhooks_helper()
        webhook_event = helper.unmarshal(body_bytes, headers)
        print(webhook_event)

        payment = webhook_event.payment
        status = payment.status
        payment_id = payment.id

        print(f"VALID Webhook: Payment {payment_id} → Status: {status}")

        if status == "CREATED":
            print("Payment Created")
            return JsonResponse({"status": "success"}, status=200)
        else:
            print(f"WEBHOOK STATUS: {status}")
            return JsonResponse({"status": "success"}, status=200)

    except Exception as e:
        print(f"Exception: {e}")
        return JsonResponse({"status": "Recieved"}, status=200)

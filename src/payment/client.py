from django.conf import settings
from onlinepayments.sdk.factory import Factory


def get_worldline_client():
    """
    Initializes the Worldline client using dynamic properties.
    Returns: SDK Client instance
    """
    props_file = str(settings.BASE_DIR) + "/payments_sdk.prp"
    api_key = settings.WORLD_LINE["API_KEY"]
    api_secret = settings.WORLD_LINE["API_KEY_SECRET"]
    client = Factory.create_client_from_file(props_file, api_key, api_secret)

    return client.merchant(settings.WORLD_LINE["MERCHANT_ID"])

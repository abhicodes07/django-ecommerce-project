from onlinepayments.sdk.factory import DefaultMarshaller
from onlinepayments.sdk.webhooks.in_memory_secret_key_store import (
    InMemorySecretKeyStore,
)
from onlinepayments.sdk.webhooks.webhooks_helper import WebhooksHelper
from core.settings import WORLD_LINE_WEBHOOK_ID, WORLD_LINE_WEBHOOK_SECRET


webhook_key_store = InMemorySecretKeyStore()
webhook_key_store.store_secret_key(WORLD_LINE_WEBHOOK_ID, WORLD_LINE_WEBHOOK_SECRET)


def get_webhooks_helper():
    marshaller = DefaultMarshaller.instance()
    return WebhooksHelper(marshaller, webhook_key_store)

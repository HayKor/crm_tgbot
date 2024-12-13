import logging

from lib.schemas.product_group import ProductGroupSchema
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)


def get_product_groups(client: RetailClient) -> list[ProductGroupSchema]:
    response = client.product_groups(filters={"active": True}).get_response()
    groups = response["productGroup"]
    return [ProductGroupSchema.model_construct(**group) for group in groups]

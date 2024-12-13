import json
import logging

from lib.schemas.product import ProductSchema
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)


def get_products(client: RetailClient, group_id: int) -> list[ProductSchema]:
    response = client.products(filters={"active": True, "groups": [group_id]}).get_response()
    products = response["products"]
    return [ProductSchema.model_construct(**product) for product in products]

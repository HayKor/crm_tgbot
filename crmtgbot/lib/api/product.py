import logging

from lib.schemas.product import ProductSchema
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)


def get_products(client: RetailClient, group_id: int) -> list[ProductSchema]:
    response = client.products(filters={"active": True, "groups": [group_id]}).get_response()
    products = response["products"]
    return [ProductSchema.model_construct(**product) for product in products]


def get_product(client: RetailClient, product_id: int) -> ProductSchema:
    response = client.products(filters={"ids": [product_id]}).get_response()
    product = response["products"][0]
    return ProductSchema.model_construct(**product)

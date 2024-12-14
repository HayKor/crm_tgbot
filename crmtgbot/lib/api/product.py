import logging
from json import loads as json_loads

from lib.schemas.product import ProductSchema
from redis.asyncio import Redis
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)


def get_products(client: RetailClient, group_id: int) -> list[ProductSchema]:
    response = client.products(filters={"active": True, "groups": [group_id]}).get_response()
    products = response["products"]
    return [ProductSchema.model_construct(**product) for product in products]


async def get_product(client: RetailClient, redis: Redis, product_id: int) -> ProductSchema:
    if product := await redis.get(f"product:{product_id}"):
        return ProductSchema.model_construct(**json_loads(product))
    else:
        response = client.products(filters={"ids": [product_id]}).get_response()
        product = response["products"][0]
        product_schema = ProductSchema.model_construct(**product)
        await redis.set(
            f"product:{product_id}",
            product_schema.model_dump_json(),
            ex=60,
        )
        return product_schema


async def get_products_by_ids(client: RetailClient, redis: Redis, product_ids: list[int]) -> list[ProductSchema]:
    return [await get_product(client, redis, product_id) for product_id in product_ids]

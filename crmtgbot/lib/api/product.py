import logging
from json import dumps as json_dumps, loads as json_loads

from lib.schemas.product import ProductSchema
from redis.asyncio import Redis
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)


async def get_products(client: RetailClient, redis: Redis, group_id: int) -> list[ProductSchema]:
    if product_list := await redis.get(f"products_of_group:{group_id}"):
        data_list = json_loads(product_list)
        return [ProductSchema.model_construct(**item) for item in data_list]
    else:
        response = client.products(
            filters={
                # "active": True,
                "groups": [group_id],
                "minQuantity": 1,
            }
        ).get_response()
        products = response["products"]

        product_schemas = [ProductSchema.model_construct(**product) for product in products]
        product_schemas = list(
            filter(
                lambda product: product.quantity >= 1,
                product_schemas,
            )
        )
        serialized_products = [model.model_dump() for model in product_schemas]
        await redis.set(
            f"products_of_group:{group_id}",
            json_dumps(
                serialized_products,
                ensure_ascii=False,
            ),
            ex=60,
        )
        return product_schemas


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

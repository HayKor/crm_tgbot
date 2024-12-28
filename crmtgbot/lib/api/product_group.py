import logging
from json import dumps as json_dumps, loads as json_loads

from lib.schemas.product_group import ProductGroupSchema
from redis.asyncio import Redis
from retailcrm import v5 as RetailClient


logger = logging.getLogger(__name__)


async def get_product_groups(client: RetailClient, redis: Redis) -> list[ProductGroupSchema]:
    if product_groups := await redis.get("product_groups_redis"):
        data_list = json_loads(product_groups)
        return [ProductGroupSchema.model_construct(**item) for item in data_list]
    else:
        response = client.product_groups(filters={"maxLevel": 1, "active": True}).get_response()
        groups = response["productGroup"]
        product_groups = [ProductGroupSchema.model_construct(**group) for group in groups]
        serialized_product_groups = [model.model_dump() for model in product_groups]
        await redis.set(
            "product_groups_redis",
            json_dumps(
                serialized_product_groups,
                ensure_ascii=False,
            ),
            ex=60,
        )
        return product_groups


async def get_product_child_groups(client: RetailClient, redis: Redis, parentId: int) -> list[ProductGroupSchema]:
    if product_groups := await redis.get(f"product_groups_redis:{parentId}"):
        data_list = json_loads(product_groups)
        return [ProductGroupSchema.model_construct(**item) for item in data_list]
    else:
        response = client.product_groups(filters={"parentGroupId": parentId, "active": True}).get_response()
        groups = response["productGroup"]
        product_groups = [ProductGroupSchema.model_construct(**group) for group in groups]
        serialized_product_groups = [model.model_dump() for model in product_groups]
        await redis.set(
            f"product_groups_redis:{parentId}",
            json_dumps(
                serialized_product_groups,
                ensure_ascii=False,
            ),
            ex=60,
        )
        return product_groups

from enum import StrEnum


class BaseRedisKeyType(StrEnum):
    pass


class CartRedisKeyType(BaseRedisKeyType):
    _prefix = "user_cart"

    cart = f"{_prefix}:{{}}"

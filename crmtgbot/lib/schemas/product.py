from typing import Any

from pydantic import BaseModel


class ProductSchema(BaseModel):
    type: str
    minPrice: float
    maxPrice: float
    catalogId: int
    id: int
    name: str
    imageUrl: str
    groups: list[int]
    offers: list[dict[str, Any]]
    active: bool
    quantity: int
    markable: bool

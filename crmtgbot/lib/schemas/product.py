from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


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
    updatedAt: datetime = Field(alias="updatedAt")
    active: bool
    quantity: int
    markable: bool

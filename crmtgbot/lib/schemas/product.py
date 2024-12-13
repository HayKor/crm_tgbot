from datetime import datetime

from pydantic import BaseModel, Field


class PriceSchema(BaseModel):
    priceType: str
    price: float
    ordering: int
    currency: str


class OfferSchema(BaseModel):
    name: str
    price: float
    images: list[str]
    id: int
    prices: list[PriceSchema]
    purchasePrice: float
    quantity: int
    active: bool


class ProductSchema(BaseModel):
    type: str
    minPrice: float
    maxPrice: float
    catalogId: int
    id: int
    name: str
    imageUrl: str
    groups: list[int]
    offers: list[OfferSchema]
    updatedAt: datetime = Field(alias="updatedAt")
    active: bool
    quantity: int
    markable: bool

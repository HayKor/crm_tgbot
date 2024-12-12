from pydantic import BaseModel


class ProductGroup(BaseModel):
    id: int
    site: str
    name: str
    lvl: int
    active: bool

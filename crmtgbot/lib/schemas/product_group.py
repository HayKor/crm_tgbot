from pydantic import BaseModel


class ProductGroupSchema(BaseModel):
    id: int
    site: str
    name: str
    lvl: int
    active: bool

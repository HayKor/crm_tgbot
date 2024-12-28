from pydantic import BaseModel


class ProductGroupSchema(BaseModel):
    id: int
    parentId: int
    site: str
    name: str
    lvl: int
    active: bool

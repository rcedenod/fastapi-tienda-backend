from pydantic import BaseModel, Field

class BaseProduct(BaseModel):
    category_id: int
    name: str
    price: float
    summary: str = Field(default='N/A')
    description: str = Field(default='N/A')

class Product(BaseProduct):
    id: int
    code: str
    created_at: str
    is_actived: int
    is_deleted: int
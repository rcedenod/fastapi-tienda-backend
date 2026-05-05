from pydantic import BaseModel, Field

class BaseCategory(BaseModel):
    name: str
    summary: str = Field(default='N/A')

class Category(BaseCategory):
    id: int
    code: str = Field(min_length=3, max_length=3)
    is_actived: int
    created_at: str
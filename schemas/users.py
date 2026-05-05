from pydantic import BaseModel, EmailStr, Field

class BaseUser(BaseModel):
    fullname: str
    email: EmailStr

class User(BaseUser):
    id: int
    password: str = Field(min_length=8)
    role: int = Field(default=2, ge=1, le=2)
    is_actived: int = Field(default=1)
    is_deleted: int = Field(default=0)
    created_at: str

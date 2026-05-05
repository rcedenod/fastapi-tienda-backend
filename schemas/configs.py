from pydantic import BaseModel, EmailStr

class Config(BaseModel):
    host_address: str
    host_port: int
    email_address: EmailStr
    email_username: EmailStr
    email_password: str

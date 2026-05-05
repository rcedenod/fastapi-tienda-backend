from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    email: EmailStr
    password: str 

class PasswordRecovery(BaseModel):
    email: EmailStr

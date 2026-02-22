# app/schemas/user_schema.py

from pydantic import BaseModel, Field
from typing import Literal


# ---------------------------------------------------------
# 1️⃣ Register Schema
# ---------------------------------------------------------

class UserRegisterSchema(BaseModel):
    name: str = Field(..., min_length=2)
    phone: str = Field(..., min_length=10, max_length=15)
    password: str = Field(..., min_length=6)
    role: Literal["farmer", "buyer", "admin"]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Santosh",
                "phone": "9876543210",
                "password": "secure123",
                "role": "farmer"
            }
        }


# ---------------------------------------------------------
# 2️⃣ Login Schema
# ---------------------------------------------------------

class UserLoginSchema(BaseModel):
    phone: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "phone": "9876543210",
                "password": "secure123"
            }
        }


# ---------------------------------------------------------
# 3️⃣ Public User Response Schema
# ---------------------------------------------------------

class UserResponseSchema(BaseModel):
    id: str
    name: str
    phone: str
    role: str
    is_active: bool


# ---------------------------------------------------------
# 4️⃣ Token Response Schema
# ---------------------------------------------------------

class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: str
    name: str
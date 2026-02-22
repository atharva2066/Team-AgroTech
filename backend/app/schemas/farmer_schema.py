# app/schemas/farmer_schema.py

from pydantic import BaseModel, Field
from typing import Optional, List


# ---------------------------------------------------------
# 1️⃣ Farmer Profile Schema
# ---------------------------------------------------------

class FarmerProfileSchema(BaseModel):
    id: str
    name: str
    phone: str
    role: str


# ---------------------------------------------------------
# 2️⃣ Create Field Schema
# ---------------------------------------------------------

class FieldCreateSchema(BaseModel):
    size_acres: float = Field(..., gt=0)
    crop_type: str
    location_district: str

    class Config:
        json_schema_extra = {
            "example": {
                "size_acres": 5,
                "crop_type": "Wheat",
                "location_district": "Pune"
            }
        }


# ---------------------------------------------------------
# 3️⃣ Field Response Schema
# ---------------------------------------------------------

class FieldResponseSchema(BaseModel):
    id: str
    size_acres: float
    crop_type: str
    location_district: str


# ---------------------------------------------------------
# 4️⃣ Dashboard Summary Schema
# ---------------------------------------------------------

class FarmerDashboardSchema(BaseModel):
    total_fields: int
    total_advisories: int
    total_listings: int


# ---------------------------------------------------------
# 5️⃣ Earnings Schema
# ---------------------------------------------------------

class FarmerEarningsSchema(BaseModel):
    completed_orders: int
    total_earnings: float
# app/schemas/crop_schema.py

from pydantic import BaseModel, Field
from typing import Optional


# ---------------------------------------------------------
# 1️⃣ Create Crop Schema (Admin Use)
# ---------------------------------------------------------

class CropCreateSchema(BaseModel):
    name: str = Field(..., min_length=2)
    residue_ratio: float = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Wheat",
                "residue_ratio": 1.5
            }
        }


# ---------------------------------------------------------
# 2️⃣ Update Crop Schema
# ---------------------------------------------------------

class CropUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    residue_ratio: Optional[float] = Field(None, gt=0)


# ---------------------------------------------------------
# 3️⃣ Crop Response Schema
# ---------------------------------------------------------

class CropResponseSchema(BaseModel):
    id: str
    name: str
    residue_ratio: float
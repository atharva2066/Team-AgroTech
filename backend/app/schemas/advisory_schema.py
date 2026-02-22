# app/schemas/advisory_schema.py

from pydantic import BaseModel, Field
from typing import List


# ---------------------------------------------------------
# 1️⃣ Advisory Request Schema
# ---------------------------------------------------------

class AdvisoryRequestSchema(BaseModel):
    field_size_acres: float = Field(..., gt=0)
    crop_type: str
    location_district: str
    state: str


# ---------------------------------------------------------
# 2️⃣ Recommendation Schema
# ---------------------------------------------------------

class RecommendationSchema(BaseModel):
    type: str
    setup_cost: float
    expected_income: float
    break_even_months: int
    viability_score: float
    co2_saved_tons: float


# ---------------------------------------------------------
# 3️⃣ Advisory Response Schema
# ---------------------------------------------------------

class AdvisoryResponseSchema(BaseModel):
    residue_estimate_tons: float
    recommendations: List[RecommendationSchema]


# ---------------------------------------------------------
# 4️⃣ Advisory History Schema (Optional Future Use)
# ---------------------------------------------------------

class AdvisoryHistorySchema(BaseModel):
    id: str
    field_size_acres: float
    crop_type: str
    location_district: str
    state: str
    residue_estimate_tons: float
    recommendations: List[RecommendationSchema]
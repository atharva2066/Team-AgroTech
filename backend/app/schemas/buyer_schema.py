# app/schemas/buyer_schema.py

from pydantic import BaseModel, Field
from typing import List, Optional


# ---------------------------------------------------------
# Buyer Profile
# ---------------------------------------------------------

class BuyerProfileSchema(BaseModel):
    company_name: str
    district: str
    state: str
    preferred_types: List[str]


# ---------------------------------------------------------
# Listing Schema (Visible to Buyers)
# ---------------------------------------------------------

class ListingSchema(BaseModel):
    id: str
    farmer_id: str
    crop_type: str
    residue_type: str
    quantity_tons: float
    price_per_ton: float
    district: str
    status: str


# ---------------------------------------------------------
# Create Bid Schema
# ---------------------------------------------------------

class BidCreateSchema(BaseModel):
    listing_id: str
    price_per_ton: float = Field(..., gt=0)
    quantity_tons: float = Field(..., gt=0)


# ---------------------------------------------------------
# Order Schema
# ---------------------------------------------------------

class OrderSchema(BaseModel):
    id: str
    buyer_id: str
    farmer_id: str
    listing_id: str
    total_amount: float
    status: str
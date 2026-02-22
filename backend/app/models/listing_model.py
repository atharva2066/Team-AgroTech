# app/models/listing_model.py

from datetime import datetime
from typing import Dict, Any


class ListingModel:
    """
    Standardizes marketplace-related MongoDB documents.
    """

    # ---------------------------------------------------------
    # 1️⃣ Create Listing (Farmer Posts Residue)
    # ---------------------------------------------------------

    @staticmethod
    def create_listing(
        farmer_id: str,
        crop_type: str,
        residue_type: str,
        quantity_tons: float,
        price_per_ton: float,
        district: str,
    ) -> Dict[str, Any]:
        return {
            "farmer_id": farmer_id,
            "crop_type": crop_type,
            "residue_type": residue_type,
            "quantity_tons": quantity_tons,
            "price_per_ton": price_per_ton,
            "district": district,
            "status": "active",  # active | sold | cancelled
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 2️⃣ Create Bid (Buyer Bids on Listing)
    # ---------------------------------------------------------

    @staticmethod
    def create_bid(
        buyer_id: str,
        listing_id: str,
        price_per_ton: float,
        quantity_tons: float,
    ) -> Dict[str, Any]:
        return {
            "buyer_id": buyer_id,
            "listing_id": listing_id,
            "price_per_ton": price_per_ton,
            "quantity_tons": quantity_tons,
            "status": "pending",  # pending | accepted | rejected
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 3️⃣ Create Order (After Bid Accepted)
    # ---------------------------------------------------------

    @staticmethod
    def create_order(
        buyer_id: str,
        farmer_id: str,
        listing_id: str,
        quantity_tons: float,
        price_per_ton: float,
    ) -> Dict[str, Any]:

        total_amount = quantity_tons * price_per_ton

        return {
            "buyer_id": buyer_id,
            "farmer_id": farmer_id,
            "listing_id": listing_id,
            "quantity_tons": quantity_tons,
            "price_per_ton": price_per_ton,
            "total_amount": round(total_amount, 2),
            "status": "completed",  # completed | cancelled
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 4️⃣ Create Connection Request
    # ---------------------------------------------------------

    @staticmethod
    def create_connection(
        buyer_id: str,
        farmer_id: str,
        message: str | None = None,
    ) -> Dict[str, Any]:
        return {
            "buyer_id": buyer_id,
            "farmer_id": farmer_id,
            "message": message,
            "status": "pending",
            "created_at": datetime.utcnow(),
        }
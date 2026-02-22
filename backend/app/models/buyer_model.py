# app/models/buyer_model.py

from datetime import datetime
from typing import Dict, Any


class BuyerModel:
    """
    Standardizes Buyer-related MongoDB documents.
    """

    # ---------------------------------------------------------
    # 1️⃣ Buyer Profile Document
    # ---------------------------------------------------------

    @staticmethod
    def create_buyer_profile(
        user_id: str,
        company_name: str,
        district: str,
        state: str,
        preferred_types: list[str],
    ) -> Dict[str, Any]:
        return {
            "user_id": user_id,
            "company_name": company_name,
            "district": district,
            "state": state,
            "preferred_types": preferred_types,
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 2️⃣ Listing Document (Farmer Listing Visible to Buyers)
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
            "status": "active",
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 3️⃣ Bid Document
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
            "status": "pending",
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 4️⃣ Order Document (After Bid Accepted)
    # ---------------------------------------------------------

    @staticmethod
    def create_order(
        buyer_id: str,
        farmer_id: str,
        listing_id: str,
        total_amount: float,
    ) -> Dict[str, Any]:
        return {
            "buyer_id": buyer_id,
            "farmer_id": farmer_id,
            "listing_id": listing_id,
            "total_amount": total_amount,
            "status": "completed",
            "created_at": datetime.utcnow(),
        }
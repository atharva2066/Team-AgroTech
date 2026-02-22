# app/models/farmer_model.py

from datetime import datetime
from typing import Dict, Any


class FarmerModel:
    """
    Standardizes Farmer-related MongoDB documents.
    """

    # ---------------------------------------------------------
    # 1️⃣ Farmer Profile
    # ---------------------------------------------------------

    @staticmethod
    def create_farmer_profile(
        user_id: str,
        district: str,
        state: str,
    ) -> Dict[str, Any]:
        return {
            "user_id": user_id,
            "district": district,
            "state": state,
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 2️⃣ Field Document
    # ---------------------------------------------------------

    @staticmethod
    def create_field(
        farmer_id: str,
        size_acres: float,
        crop_type: str,
        location_district: str,
    ) -> Dict[str, Any]:
        return {
            "farmer_id": farmer_id,
            "size_acres": size_acres,
            "crop_type": crop_type,
            "location_district": location_district,
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 3️⃣ Farmer Listing (Marketplace)
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
    # 4️⃣ Advisory History Record
    # ---------------------------------------------------------

    @staticmethod
    def create_advisory_record(
        farmer_id: str,
        advisory_id: str,
    ) -> Dict[str, Any]:
        return {
            "farmer_id": farmer_id,
            "advisory_id": advisory_id,
            "created_at": datetime.utcnow(),
        }
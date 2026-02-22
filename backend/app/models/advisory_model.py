# app/models/advisory_model.py

from datetime import datetime
from typing import List, Dict, Any


class AdvisoryModel:
    """
    Represents an advisory document structure.
    This is NOT an ORM model.
    It simply standardizes MongoDB document format.
    """

    @staticmethod
    def create(
        farmer_id: str,
        field_size_acres: float,
        crop_type: str,
        location_district: str,
        state: str,
        residue_estimate_tons: float,
        recommendations: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Create advisory document dictionary.
        """

        return {
            "farmer_id": farmer_id,
            "field_size_acres": field_size_acres,
            "crop_type": crop_type,
            "location_district": location_district,
            "state": state,
            "residue_estimate_tons": residue_estimate_tons,
            "recommendations": recommendations,
            "created_at": datetime.utcnow(),
        }

    @staticmethod
    def recommendation(
        type: str,
        setup_cost: float,
        expected_income: float,
        break_even_months: int,
        viability_score: float,
        co2_saved_tons: float,
    ) -> Dict[str, Any]:
        """
        Create a single recommendation object.
        """

        return {
            "type": type,
            "setup_cost": setup_cost,
            "expected_income": expected_income,
            "break_even_months": break_even_months,
            "viability_score": viability_score,
            "co2_saved_tons": co2_saved_tons,
        }
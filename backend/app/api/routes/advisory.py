# app/api/routes/advisory.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.advisory_schema import AdvisoryRequestSchema
from app.core.dependencies import get_current_user
from app.core.database import get_database
from app.services.residue_service import calculate_residue
from app.services.financial_service import calculate_financials
from app.services.ranking_service import rank_alternatives
from app.models.advisory_model import AdvisoryModel
from typing import Dict, Optional

router = APIRouter()


async def require_farmer(user=Depends(get_current_user)):
    if user.get("role") != "farmer":
        raise HTTPException(status_code=403, detail="Farmer access required")
    return user


@router.post("/analyze")
async def analyze_advisory(
    payload: AdvisoryRequestSchema,
    user=Depends(require_farmer),
):
    field_size = payload.field_size_acres
    crop_type = payload.crop_type
    district = payload.location_district
    state = payload.state

    residue_tons = await calculate_residue(field_size, crop_type)

    financials = calculate_financials(
    residue_tons=residue_tons,
    district=district,
    demand_score=0.7,
)

    recommendations = []

    for alt, data in financials.items():
        rec = AdvisoryModel.recommendation(
            type=alt,
            setup_cost=data["setup_cost"],
            expected_income=data["expected_income"],
            break_even_months=data["break_even_months"],
            viability_score=0,  # ranking will compute final_score
            co2_saved_tons=data["co2_saved_tons"],
        )
        rec.update({
            "profit": data["profit"],
            "total_income": data["total_income"],
            "carbon_credit_income": data["carbon_credit_income"],
        })
        recommendations.append(rec)

    recommendations = rank_alternatives(
        recommendations=recommendations,
        district=district,
    )

    advisory_doc = AdvisoryModel.create(
        farmer_id=str(user["_id"]),
        field_size_acres=field_size,
        crop_type=crop_type,
        location_district=district,
        state=state,
        residue_estimate_tons=residue_tons,
        recommendations=recommendations,
    )

    db = get_database()
    await db.advisories.insert_one(advisory_doc)

    return {
        "residue_estimate_tons": residue_tons,
        "recommendations": recommendations,
    }
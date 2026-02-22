# app/api/routes/farmer.py

from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user
from app.services.buyer_service import get_dashboard_summary
from app.core.database import get_database
from app.schemas.farmer_schema import FieldCreateSchema
from app.models.farmer_model import FarmerModel
from app.utils.helpers import serialize_mongo_document

router = APIRouter()


async def require_farmer(user=Depends(get_current_user)):
    if user.get("role") != "farmer":
        raise HTTPException(status_code=403, detail="Farmer access required")
    return user


@router.get("/profile")
async def get_profile(user=Depends(require_farmer)):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "phone": user["phone"],
        "role": user["role"],
    }


@router.post("/fields")
async def add_field(payload: FieldCreateSchema, user=Depends(require_farmer)):
    db = get_database()

    field_doc = FarmerModel.create_field(
        farmer_id=str(user["_id"]),
        size_acres=payload.size_acres,
        crop_type=payload.crop_type,
        location_district=payload.location_district,
    )

    result = await db.fields.insert_one(field_doc)

    return {
        "message": "Field added",
        "field_id": str(result.inserted_id),
    }
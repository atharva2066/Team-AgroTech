# app/api/routes/crops.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime

from app.core.database import get_database
from app.core.dependencies import get_current_user

router = APIRouter()


# ---------------------------------------------------------
# 1️⃣ Get All Crops (Public)
# ---------------------------------------------------------

@router.get("/")
async def get_all_crops():
    """
    Returns all supported crop types.
    """

    db = get_database()

    cursor = db.crops.find({})

    crops = []
    async for doc in cursor:
        crops.append({
            "id": str(doc["_id"]),
            "name": doc.get("name"),
            "residue_ratio": doc.get("residue_ratio"),
        })

    return crops


# ---------------------------------------------------------
# 2️⃣ Add Crop (Admin Only)
# ---------------------------------------------------------

async def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user


@router.post("/")
async def add_crop(
    payload: dict,
    user=Depends(require_admin)
):
    """
    Add a new crop.
    Example:
    {
        "name": "Wheat",
        "residue_ratio": 1.5
    }
    """

    db = get_database()

    name = payload.get("name")
    residue_ratio = payload.get("residue_ratio")

    if not name or residue_ratio is None:
        raise HTTPException(
            status_code=400,
            detail="name and residue_ratio required"
        )

    existing = await db.crops.find_one({"name": name})
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Crop already exists"
        )

    crop_data = {
        "name": name,
        "residue_ratio": residue_ratio,
        "created_at": datetime.utcnow()
    }

    result = await db.crops.insert_one(crop_data)

    return {
        "message": "Crop added successfully",
        "crop_id": str(result.inserted_id)
    }
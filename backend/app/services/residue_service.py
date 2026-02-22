# app/services/residue_service.py

from app.core.database import get_database


async def calculate_residue(field_size_acres: float, crop_type: str) -> float:
    """
    Calculate residue in tons.
    residue = field_size_acres × residue_ratio
    """

    db = get_database()

    crop = await db.crops.find_one({"name": crop_type})

    if not crop:
        raise ValueError("Crop not supported")

    residue_ratio = crop.get("residue_ratio", 0)

    residue_tons = field_size_acres * residue_ratio

    return round(residue_tons, 2)
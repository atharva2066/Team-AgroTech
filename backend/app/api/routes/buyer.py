# app/api/routes/buyer.py

from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user
from app.services.buyer_service import (
    get_dashboard_summary,
    fetch_listings,
    submit_bid,
)

from app.schemas.buyer_schema import BidCreateSchema

router = APIRouter()


async def require_buyer(user=Depends(get_current_user)):
    if user.get("role") != "buyer":
        raise HTTPException(status_code=403, detail="Buyer access required")
    return user


@router.get("/dashboard-summary")
async def dashboard(user=Depends(require_buyer)):
    return await get_dashboard_summary(str(user["_id"]))


@router.get("/listings")
async def listings(user=Depends(require_buyer)):
    return await fetch_listings()


@router.post("/bid")
async def create_bid(payload: BidCreateSchema, user=Depends(require_buyer)):
    return await submit_bid(
        buyer_id=str(user["_id"]),
        listing_id=payload.listing_id,
        price_per_ton=payload.price_per_ton,
        quantity_tons=payload.quantity_tons,
    )
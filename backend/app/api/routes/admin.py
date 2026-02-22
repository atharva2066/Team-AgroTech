# app/api/routes/admin.py

from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_user
from app.services.analytics_service import (
    get_overview_metrics,
    get_monthly_advisory_trends,
    get_advisory_by_district,
    get_total_co2_saved,
    get_alternative_mix_distribution,
)

router = APIRouter()


async def require_admin(user=Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@router.get("/analytics/overview")
async def overview(user=Depends(require_admin)):
    return await get_overview_metrics()


@router.get("/analytics/monthly")
async def monthly(year: int, user=Depends(require_admin)):
    return await get_monthly_advisory_trends(year)


@router.get("/analytics/by-district")
async def by_district(user=Depends(require_admin)):
    return await get_advisory_by_district()


@router.get("/analytics/co2")
async def co2(user=Depends(require_admin)):
    return await get_total_co2_saved()


@router.get("/analytics/alternative-mix")
async def mix(user=Depends(require_admin)):
    return await get_alternative_mix_distribution()
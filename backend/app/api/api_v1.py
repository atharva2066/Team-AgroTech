# app/api/api_v1.py

from fastapi import APIRouter

# Import route modules (NOT router directly)
from app.api.routes import (
    auth,
    advisory,
    farmer,
    buyer,
    admin,
    crops,
)

api_router = APIRouter()

# -------------------------------
# Include Route Modules
# -------------------------------

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

api_router.include_router(
    advisory.router,
    prefix="/advisory",
    tags=["Advisory"],
)

api_router.include_router(
    farmer.router,
    prefix="/farmer",
    tags=["Farmer"],
)

api_router.include_router(
    buyer.router,
    prefix="/buyers",
    tags=["Buyer"],
)

api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"],
)

api_router.include_router(
    crops.router,
    prefix="/crops",
    tags=["Crops"],
)
from fastapi import APIRouter

# Import route modules (NOT the app)
from app.api.routes import (
    auth,
    advisory,
    farmer,
    buyer,
    admin,
    crops,
)

# Create versioned router
api_router = APIRouter()


# -----------------------------
# Auth Routes
# -----------------------------
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)


# -----------------------------
# Advisory Routes
# -----------------------------
api_router.include_router(
    advisory.router,
    prefix="/advisory",
    tags=["Advisory"],
)


# -----------------------------
# Farmer Routes
# -----------------------------
api_router.include_router(
    farmer.router,
    prefix="/farmer",
    tags=["Farmer"],
)


# -----------------------------
# Buyer Routes
# -----------------------------
api_router.include_router(
    buyer.router,
    prefix="/buyers",
    tags=["Buyer"],
)


# -----------------------------
# Admin Routes
# -----------------------------
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"],
)


# -----------------------------
# Crops Routes
# -----------------------------
api_router.include_router(
    crops.router,
    prefix="/crops",
    tags=["Crops"],
)
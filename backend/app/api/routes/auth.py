# app/api/routes/auth.py

from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import (
    UserRegisterSchema,
    UserLoginSchema,
    TokenResponseSchema,
)
from app.core.database import get_database
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user_model import UserModel


router = APIRouter()


# ---------------------------------------------------------
# Register
# ---------------------------------------------------------

@router.post("/register")
async def register_user(payload: UserRegisterSchema):
    db = get_database()

    # Check existing user
    existing_user = await db.users.find_one({"phone": payload.phone})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists with this phone number",
        )

    # Hash password
    hashed_password = hash_password(payload.password)

    # Create user document
    user_doc = UserModel.create_user(
        name=payload.name,
        phone=payload.phone,
        password_hash=hashed_password,
        role=payload.role,
    )

    # Insert into DB
    result = await db.users.insert_one(user_doc)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
    }


# ---------------------------------------------------------
# Login
# ---------------------------------------------------------

@router.post("/login", response_model=TokenResponseSchema)
async def login_user(payload: UserLoginSchema):
    db = get_database()

    # Find user
    user = await db.users.find_one({"phone": payload.phone})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone or password",
        )

    # Verify password
    if not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone or password",
        )

    # Create JWT token
    token = create_access_token(
        subject=str(user["_id"]),
        extra_data={"role": user["role"]},
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
        "user_id": str(user["_id"]),
        "name": user["name"],
    }
# app/core/security.py

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from typing import Optional, Dict, Any
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ------------------------------
# Password Hashing
# ------------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ------------------------------
# JWT Token Creation
# ------------------------------

def create_access_token(
    subject: str,
    extra_data: Optional[Dict[str, Any]] = None,
) -> str:

    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: Dict[str, Any] = {
        "sub": subject,
        "exp": expire,
    }

    if extra_data:
        payload.update(extra_data)

    # Type narrowing for Pylance
    secret_key: str = str(settings.JWT_SECRET)

    return jwt.encode(
        payload,
        secret_key,
        algorithm=settings.JWT_ALGORITHM,
    )
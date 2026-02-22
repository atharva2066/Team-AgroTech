# app/models/user_model.py

from datetime import datetime
from typing import Dict, Any


class UserModel:
    """
    Standardizes User-related MongoDB documents.
    """

    # ---------------------------------------------------------
    # 1️⃣ Base User Document
    # ---------------------------------------------------------

    @staticmethod
    def create_user(
        name: str,
        phone: str,
        password_hash: str,
        role: str,
    ) -> Dict[str, Any]:
        """
        role: 'farmer' | 'buyer' | 'admin'
        """

        return {
            "name": name,
            "phone": phone,
            "password_hash": password_hash,
            "role": role,
            "is_active": True,
            "created_at": datetime.utcnow(),
        }

    # ---------------------------------------------------------
    # 2️⃣ Public User Response (Sanitized)
    # ---------------------------------------------------------

    @staticmethod
    def to_public(user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove sensitive fields before returning to client.
        """

        return {
            "id": str(user.get("_id")),
            "name": user.get("name"),
            "phone": user.get("phone"),
            "role": user.get("role"),
            "is_active": user.get("is_active", True),
        }

    # ---------------------------------------------------------
    # 3️⃣ Update Profile Helper
    # ---------------------------------------------------------

    @staticmethod
    def update_profile(
        name: str | None = None,
        phone: str | None = None,
    ) -> Dict[str, Any]:

        update_data: Dict[str, Any] = {}

        if name:
            update_data["name"] = name

        if phone:
            update_data["phone"] = phone

        update_data["updated_at"] = datetime.utcnow()

        return update_data
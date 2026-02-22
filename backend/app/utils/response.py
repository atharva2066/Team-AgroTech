# app/utils/response.py

from typing import Any, Optional, Dict


# ---------------------------------------------------------
# 1️⃣ Standard Success Response
# ---------------------------------------------------------

def success_response(
    data: Any = None,
    message: str = "Success",
) -> Dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data,
    }


# ---------------------------------------------------------
# 2️⃣ Standard Error Response
# ---------------------------------------------------------

def error_response(
    message: str = "Something went wrong",
    errors: Optional[Any] = None,
) -> Dict[str, Any]:
    response = {
        "success": False,
        "message": message,
    }

    if errors is not None:
        response["errors"] = errors

    return response


# ---------------------------------------------------------
# 3️⃣ Pagination Response
# ---------------------------------------------------------

def paginated_response(
    items: list,
    total: int,
    page: int,
    page_size: int,
    message: str = "Success",
) -> Dict[str, Any]:

    return {
        "success": True,
        "message": message,
        "data": items,
        "pagination": {
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        },
    }


# ---------------------------------------------------------
# 4️⃣ Created Response
# ---------------------------------------------------------

def created_response(
    data: Any = None,
    message: str = "Created successfully",
) -> Dict[str, Any]:
    return {
        "success": True,
        "message": message,
        "data": data,
    }
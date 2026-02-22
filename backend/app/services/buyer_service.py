# app/services/buyer_service.py

from typing import Optional, List
from datetime import datetime
from bson import ObjectId

from app.core.database import get_database
from app.models.listing_model import ListingModel


# ---------------------------------------------------------
# 1️⃣ Dashboard Summary
# ---------------------------------------------------------

async def get_dashboard_summary(buyer_id: str) -> dict:
    db = get_database()

    total_orders = await db.orders.count_documents({"buyer_id": buyer_id})
    total_bids = await db.bids.count_documents({"buyer_id": buyer_id})

    return {
        "total_orders": total_orders,
        "total_bids": total_bids,
    }


# ---------------------------------------------------------
# 2️⃣ Get Listings with Filters
# ---------------------------------------------------------

async def fetch_listings(
    residue_type: Optional[str] = None,
    district: Optional[str] = None,
) -> List[dict]:

    db = get_database()

    query = {"status": "active"}

    if residue_type:
        query["residue_type"] = residue_type

    if district:
        query["district"] = district

    cursor = db.listings.find(query)

    listings = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        listings.append(doc)

    return listings


# ---------------------------------------------------------
# 3️⃣ Submit Bid
# ---------------------------------------------------------

async def submit_bid(
    buyer_id: str,
    listing_id: str,
    price_per_ton: float,
    quantity_tons: float,
) -> dict:

    db = get_database()

    # Check listing exists
    listing = await db.listings.find_one(
        {"_id": ObjectId(listing_id)}
    )

    if not listing:
        raise ValueError("Listing not found")

    bid_data = ListingModel.create_bid(
        buyer_id=buyer_id,
        listing_id=listing_id,
        price_per_ton=price_per_ton,
        quantity_tons=quantity_tons,
    )

    result = await db.bids.insert_one(bid_data)

    return {
        "message": "Bid submitted successfully",
        "bid_id": str(result.inserted_id),
    }


# ---------------------------------------------------------
# 4️⃣ Get Orders
# ---------------------------------------------------------

async def get_orders(
    buyer_id: str,
    status: Optional[str] = None,
) -> List[dict]:

    db = get_database()

    query = {"buyer_id": buyer_id}

    if status:
        query["status"] = status

    cursor = db.orders.find(query)

    orders = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        orders.append(doc)

    return orders


# ---------------------------------------------------------
# 5️⃣ Create Connection Request
# ---------------------------------------------------------

async def create_connection(
    buyer_id: str,
    farmer_id: str,
    message: Optional[str] = None,
) -> dict:

    db = get_database()

    connection_data = ListingModel.create_connection(
        buyer_id=buyer_id,
        farmer_id=farmer_id,
        message=message,
    )

    result = await db.connections.insert_one(connection_data)

    return {
        "message": "Connection request sent",
        "connection_id": str(result.inserted_id),
    }


# ---------------------------------------------------------
# 6️⃣ Get Alerts
# ---------------------------------------------------------

async def get_alerts(buyer_id: str) -> List[dict]:

    db = get_database()

    cursor = db.alerts.find({"buyer_id": buyer_id})

    alerts = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        alerts.append(doc)

    return alerts
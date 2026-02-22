# app/services/analytics_service.py

from datetime import datetime
from collections import defaultdict
from typing import List, Dict

from app.core.database import get_database


# ---------------------------------------------------------
# 1️⃣ Overview Metrics
# ---------------------------------------------------------

async def get_overview_metrics() -> Dict[str, int]:
    db = get_database()

    total_users = await db.users.count_documents({})
    total_farmers = await db.users.count_documents({"role": "farmer"})
    total_buyers = await db.users.count_documents({"role": "buyer"})
    total_advisories = await db.advisories.count_documents({})
    total_listings = await db.listings.count_documents({})

    return {
        "total_users": total_users,
        "total_farmers": total_farmers,
        "total_buyers": total_buyers,
        "total_advisories": total_advisories,
        "total_listings": total_listings,
    }


# ---------------------------------------------------------
# 2️⃣ Monthly Advisory Trends
# ---------------------------------------------------------

async def get_monthly_advisory_trends(year: int) -> List[Dict]:
    db = get_database()

    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)

    cursor = db.advisories.find({
        "created_at": {"$gte": start, "$lt": end}
    })

    monthly_data = defaultdict(int)

    async for doc in cursor:
        month = doc["created_at"].month
        monthly_data[month] += 1

    return [
        {"month": m, "advisories": monthly_data.get(m, 0)}
        for m in range(1, 13)
    ]


# ---------------------------------------------------------
# 3️⃣ Advisory Count by District
# ---------------------------------------------------------

async def get_advisory_by_district() -> List[Dict]:
    db = get_database()

    pipeline = [
        {
            "$group": {
                "_id": "$location_district",
                "count": {"$sum": 1}
            }
        }
    ]

    results = []
    async for doc in db.advisories.aggregate(pipeline):
        results.append({
            "district": doc["_id"],
            "advisories": doc["count"]
        })

    return results


# ---------------------------------------------------------
# 4️⃣ CO₂ Savings Aggregation
# ---------------------------------------------------------

async def get_total_co2_saved() -> Dict[str, float]:
    db = get_database()

    cursor = db.advisories.find({})

    total_co2_saved = 0.0

    async for doc in cursor:
        for rec in doc.get("recommendations", []):
            total_co2_saved += rec.get("co2_saved_tons", 0.0)

    return {
        "total_co2_saved_tons": round(total_co2_saved, 2)
    }


# ---------------------------------------------------------
# 5️⃣ Alternative Mix Distribution
# ---------------------------------------------------------

async def get_alternative_mix_distribution() -> List[Dict]:
    db = get_database()

    mix = defaultdict(int)

    cursor = db.advisories.find({})

    async for doc in cursor:
        for rec in doc.get("recommendations", []):
            alt_type = rec.get("type")
            if alt_type:
                mix[alt_type] += 1

    return [
        {"type": key, "count": value}
        for key, value in mix.items()
    ]
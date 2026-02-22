# app/ml/price_model.py

from typing import Optional
from datetime import datetime
import math


# ---------------------------------------------------------
# Base Price Map (Fallback)
# ---------------------------------------------------------

BASE_PRICE_MAP = {
    "biochar": 5500,
    "pellets": 4200,
    "compost": 2800,
    "direct_incorporation": 1500,
}


# ---------------------------------------------------------
# District Adjustment Multiplier
# ---------------------------------------------------------

DISTRICT_MULTIPLIER = {
    "Pune": 1.1,
    "Nagpur": 0.95,
    "Nashik": 1.05,
}


# ---------------------------------------------------------
# Demand-Based Adjustment (0–1 scale)
# ---------------------------------------------------------

def demand_adjustment(demand_score: float) -> float:
    """
    Increase price based on demand score.
    demand_score should be between 0 and 1.
    """

    return 1 + (demand_score * 0.15)


# ---------------------------------------------------------
# Seasonal Adjustment
# ---------------------------------------------------------

def seasonal_adjustment() -> float:
    """
    Simple seasonal multiplier based on month.
    Harvest months may reduce price slightly due to oversupply.
    """

    month = datetime.utcnow().month

    # Harvest-heavy months example
    if month in [3, 4, 10, 11]:
        return 0.9

    return 1.0


# ---------------------------------------------------------
# Final Price Prediction
# ---------------------------------------------------------

def predict_price(
    residue_type: str,
    district: Optional[str] = None,
    demand_score: float = 0.5,
) -> float:
    """
    Predict price per ton using:
    - Base price
    - District multiplier
    - Demand score
    - Seasonal adjustment
    """

    base_price = BASE_PRICE_MAP.get(residue_type, 3000)

    # District factor
    district_factor = 1.0
    if district and district in DISTRICT_MULTIPLIER:
        district_factor = DISTRICT_MULTIPLIER[district]

    # Demand factor
    demand_factor = demand_adjustment(demand_score)

    # Seasonal factor
    season_factor = seasonal_adjustment()

    predicted_price = (
        base_price
        * district_factor
        * demand_factor
        * season_factor
    )

    return round(predicted_price, 2)
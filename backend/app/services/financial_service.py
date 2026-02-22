# app/services/financial_service.py

from typing import Dict


# Basic cost assumptions (can move to DB later)
ALTERNATIVE_DATA = {
    "biochar": {
        "setup_cost_per_ton": 3000,
        "income_per_ton": 5500,
        "co2_saving_per_ton": 0.3,
    },
    "pellets": {
        "setup_cost_per_ton": 2000,
        "income_per_ton": 4200,
        "co2_saving_per_ton": 0.2,
    },
    "compost": {
        "setup_cost_per_ton": 1500,
        "income_per_ton": 2800,
        "co2_saving_per_ton": 0.1,
    },
    "direct_incorporation": {
        "setup_cost_per_ton": 800,
        "income_per_ton": 1500,
        "co2_saving_per_ton": 0.05,
    },
}


def calculate_financials(residue_tons: float) -> Dict[str, Dict]:
    """
    Calculate financial metrics for each alternative.
    """

    results = {}

    for alt, data in ALTERNATIVE_DATA.items():

        setup_cost = residue_tons * data["setup_cost_per_ton"]
        expected_income = residue_tons * data["income_per_ton"]
        profit = expected_income - setup_cost

        # Simple break-even formula
        break_even_months = 3 if profit > 0 else 12

        # Simple viability scoring
        viability_score = max(min((profit / 10000) * 10, 100), 10)

        results[alt] = {
            "setup_cost": round(setup_cost, 2),
            "expected_income": round(expected_income, 2),
            "profit": round(profit, 2),
            "break_even_months": break_even_months,
            "viability_score": round(viability_score, 2),
            "co2_saved_tons": round(
                residue_tons * data["co2_saving_per_ton"], 2
            ),
        }

    return results
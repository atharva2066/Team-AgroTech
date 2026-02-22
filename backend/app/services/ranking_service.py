# app/services/ranking_service.py

from typing import List, Dict


# ---------------------------------------------------------
# Configurable Weights
# ---------------------------------------------------------

WEIGHTS = {
    "profit": 0.4,
    "break_even": 0.2,
    "co2": 0.2,
    "demand": 0.2,
}


# Example district demand map (can move to DB later)
DISTRICT_DEMAND = {
    "Pune": {
        "biochar": 0.9,
        "pellets": 0.7,
        "compost": 0.5,
        "direct_incorporation": 0.4,
    }
}


# ---------------------------------------------------------
# Normalize helper
# ---------------------------------------------------------

def normalize(value: float, min_val: float, max_val: float) -> float:
    if max_val == min_val:
        return 1.0
    return (value - min_val) / (max_val - min_val)


# ---------------------------------------------------------
# Rank Alternatives
# ---------------------------------------------------------

def rank_alternatives(
    recommendations: List[Dict],
    district: str,
) -> List[Dict]:

    if not recommendations:
        return recommendations

    profits = [r["expected_income"] - r["setup_cost"] for r in recommendations]
    co2_vals = [r["co2_saved_tons"] for r in recommendations]
    break_evens = [r["break_even_months"] for r in recommendations]

    min_profit, max_profit = min(profits), max(profits)
    min_co2, max_co2 = min(co2_vals), max(co2_vals)
    min_be, max_be = min(break_evens), max(break_evens)

    for r in recommendations:
        profit = r["expected_income"] - r["setup_cost"]
        be = r["break_even_months"]
        co2 = r["co2_saved_tons"]

        # Normalize metrics
        norm_profit = normalize(profit, min_profit, max_profit)
        norm_co2 = normalize(co2, min_co2, max_co2)

        # Faster break-even = better score
        norm_be = 1 - normalize(be, min_be, max_be)

        # District demand weighting
        demand_score = 0.5  # default neutral
        if district in DISTRICT_DEMAND:
            demand_score = DISTRICT_DEMAND[district].get(r["type"], 0.5)

        final_score = (
            WEIGHTS["profit"] * norm_profit
            + WEIGHTS["break_even"] * norm_be
            + WEIGHTS["co2"] * norm_co2
            + WEIGHTS["demand"] * demand_score
        )

        r["final_score"] = round(final_score * 100, 2)

    # Sort by final_score descending
    recommendations.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return recommendations
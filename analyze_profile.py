# File: analyze_profile.py
import json
import os
from typing import Dict, Any

def analyze_profile(
    d: float,
    i: float,
    s: float,
    c: float,
    stage_label: str = "",
    remedy_file: str = "remedy_traits.json"
) -> Dict[str, Any]:
    """
    Analyze a DISC profile using Z9 continuum logic and return detailed metrics.

    Steps:
    1. Normalize raw DISC scores to percentages.
    2. Compute trait subtrait approximations.
    3. Identify negated traits (scores < 25%).
    4. Calculate harmony ratio and composite trait score.
    5. Apply recursive logic placeholder.
    6. Load remedy metadata per trait.

    Args:
        d: Dominance total score.
        i: Influence total score.
        s: Steadiness total score.
        c: Conscientiousness total score.
        stage_label: Current Z9 Spiral stage label (e.g., "Stage 4").
        remedy_file: Path to JSON file mapping traits to remedies.

    Returns:
        A dict containing:
            traits: Percentages for each DISC trait.
            subtraits: Approximate subtrait scores.
            negated: Traits with low scores needing development.
            harmony_ratio: Balance metric (0-100).
            trait_score: Composite development score.
            recursion_result: Placeholder Z9 recursion data.
            remedies: Loaded remedy metadata per trait.
            product_links: First product link for each remedy.
    """
    # 1. Normalize to percentages
    total = d + i + s + c
    if total <= 0:
        total = 1
    trait_percentages = {
        "D": round((d / total) * 100),
        "I": round((i / total) * 100),
        "S": round((s / total) * 100),
        "C": round((c / total) * 100)
    }

    # 2. Subtrait approximations
    subtraits = {
        "DD": round(d * 0.6),
        "DI": round((d + i) / 2),
        "DS": round((d + s) / 2),
        "DC": round((d + c) / 2),
        "II": round(i * 0.6),
        "ID": round((i + d) / 2),
        "IS": round((i + s) / 2),
        "IC": round((i + c) / 2),
        "SS": round(s * 0.6),
        "SD": round((s + d) / 2),
        "SI": round((s + i) / 2),
        "SC": round((s + c) / 2),
        "CC": round(c * 0.6),
        "CD": round((c + d) / 2),
        "CI": round((c + i) / 2),
        "CS": round((c + s) / 2)
    }

    # 3. Negated traits (under 25%)
    negated = {t: 100 - pct for t, pct in trait_percentages.items() if pct < 25}

    # 4. Harmony ratio and composite trait score
    values = list(trait_percentages.values())
    avg_pct = sum(values) / 4
    deviation = sum(abs(v - avg_pct) for v in values) / 4
    harmony_ratio = round(100 - deviation, 2)
    trait_score = round((avg_pct + harmony_ratio) / 2, 2)

    # 5. Recursive logic placeholder
    recursion_result = {
        "stable_score": round(trait_score / 10, 2),
        "iterations": 4
    }

    # 6. Load remedy metadata and product links
    remedies = {}
    product_links = []
    if os.path.exists(remedy_file):
        with open(remedy_file, "r") as f:
            remedy_data = json.load(f)
        for trait, data in remedy_data.items():
            if trait in trait_percentages:
                remedies[trait] = data
                products = data.get("products", [])
                if products:
                    product_links.append({"title": f"{trait} Remedy", "link": products[0]})

    return {
        "traits": trait_percentages,
        "subtraits": subtraits,
        "negated": negated,
        "harmony_ratio": harmony_ratio,
        "trait_score": trait_score,
        "recursion_result": recursion_result,
        "remedies": remedies,
        "product_links": product_links
    }

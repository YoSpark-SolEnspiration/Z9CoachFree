# File: z9_spiral_logic.py
import math
from typing import Tuple, Union


def map_disc_to_stage(
    d_score: float,
    i_score: float,
    s_score: float,
    c_score: float
) -> str:
    """
    Map DISC trait values to a Z9 Spiral stage (1–8) using normalized percentages.

    Args:
        d_score: Dominance metric (raw or percentage).
        i_score: Influence metric.
        s_score: Steadiness metric.
        c_score: Conscientiousness metric.

    Returns:
        A string label "Stage X" where X is between 1 and 8.
    """
    # Compute average of the four scores
    avg = (d_score + i_score + s_score + c_score) / 4.0

    # Determine normalization range: if scores appear as percentages (0-100), scale to 0-1
    if avg > 1:
        norm = avg / 100.0
    else:
        # Assume avg in 1-5 range, normalize to 0-1
        norm = (avg - 1.0) / 4.0

    norm = max(0.0, min(norm, 1.0))

    # Scale into 8 stages and clamp
    stage_index = math.floor(norm * 8) + 1
    stage_index = max(1, min(stage_index, 8))

    return f"Stage {stage_index}"

# File: fairy_coachfree.py
# Title: Fairy Session Snap Readback

import json
from typing import Any, Dict, Optional

from opportunity_loader import build_ptype_story_url
from z9_spiral_logic import map_disc_to_stage


DISC_NAMES = {
    "D": "Direction",
    "I": "Expression",
    "S": "Stability",
    "C": "Clarity",
}


def load_json(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_mood_missions(path="data/mood_missions.json") -> Dict:
    return load_json(path)


def load_stage_summaries(path="data/results_ee_stage_summaries.json") -> Dict:
    return load_json(path)


def _dominant_trait(traits: Dict[str, float]) -> str:
    if not traits:
        return "D"
    return max(traits.items(), key=lambda item: item[1])[0]


def _secondary_trait(traits: Dict[str, float], primary: str) -> str:
    ordered = sorted(traits.items(), key=lambda item: item[1], reverse=True)
    if len(ordered) > 1:
        return ordered[1][0]
    return primary


def _normalize_stage_number(stage_key: str) -> str:
    digits = "".join(ch for ch in str(stage_key) if ch.isdigit())
    return digits or "1"


def _mood_band(mood_score: int) -> str:
    if mood_score <= 3:
        return "low"
    if mood_score >= 8:
        return "elevated"
    return "steady"


def generate_fairy_whisper(traits: Dict[str, float], mood_state: int) -> str:
    """
    Legacy-safe function name.

    Returns a short Fairy Session Snap line instead of the old mystical/mood-whisper tone.
    """

    dominant = _dominant_trait(traits)
    doorway = DISC_NAMES.get(dominant, dominant)
    band = _mood_band(mood_state)

    if band == "low":
        readback = (
            f"The session may show the {doorway} state conserving energy before it can move cleanly."
        )
    elif band == "elevated":
        readback = (
            f"The session may show the {doorway} state accelerating before timing is fully checked."
        )
    else:
        readback = (
            f"The session may show the {doorway} state clearly enough to notice what it does under pressure."
        )

    return f"**Fairy Session Snap:** {readback}"


def generate_session_snap_readback(
    stage_key: str,
    dominant_trait: str,
    secondary_trait: str,
    mood_score: int,
    trait_scores: Dict[str, float],
    stage_data: Dict[str, dict],
    session_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, str]:
    """
    Generate a structured Fairy Session Snap.

    This is the game/render readback layer:
    - what the session showed
    - what shifted
    - where pressure tightened
    - what the Healthy PType story reveals next
    """

    stage_number = _normalize_stage_number(stage_key)
    subtype = f"{dominant_trait}{secondary_trait}"
    doorway = DISC_NAMES.get(dominant_trait, dominant_trait)
    secondary = DISC_NAMES.get(secondary_trait, secondary_trait)
    mood_band = _mood_band(mood_score)

    stage_info = stage_data.get(f"Stage {stage_number}", stage_data.get(stage_key, {}))
    stage_pressure = stage_info.get(
        "stage_pressure",
        "The session surfaced pressure around the current developmental state.",
    )
    resistance = stage_info.get("ptype_resistance", {}).get(
        dominant_trait,
        "This state may resist movement by protecting its familiar pattern.",
    )
    next_move = stage_info.get(
        "next_move",
        "This movement tends to stabilize when the state can be noticed without being forced.",
    )

    mapped_stage = map_disc_to_stage(
        d_score=trait_scores.get("D", 0),
        i_score=trait_scores.get("I", 0),
        s_score=trait_scores.get("S", 0),
        c_score=trait_scores.get("C", 0),
    )

    story_url = build_ptype_story_url(
        traits=trait_scores,
        stage=stage_number,
        ohu="Healthy",
    )

    if session_result:
        outcome = session_result.get("outcome") or session_result.get("summary") or "The session produced a visible state movement."
        changed = session_result.get("changed") or session_result.get("delta") or "The session made the current pattern easier to observe."
    else:
        outcome = "The session made the current state easier to see."
        changed = "The render showed how the state moves when pressure, choice, or uncertainty appears."

    if mood_band == "low":
        movement = (
            f"The {doorway} signal may be present, but the system appears to be conserving movement."
        )
    elif mood_band == "elevated":
        movement = (
            f"The {doorway} signal appears more active, with the state likely moving faster under pressure."
        )
    else:
        movement = (
            f"The {doorway} signal is visible enough to read without forcing a deeper conclusion."
        )

    return {
        "title": "Fairy Session Snap",
        "session_signal": outcome,
        "state_movement": movement,
        "change_readback": changed,
        "stage_pressure": stage_pressure,
        "ptype_resistance": resistance,
        "regulation_cue": next_move,
        "healthy_story": (
            f"Open the Healthy {subtype} PType story for Stage {stage_number}. "
            f"The story shows how the {doorway} doorway can regulate without losing its core strength."
        ),
        "ptype_url": story_url,
        "compact": (
            f"The session revealed a {doorway} state with {secondary} as the secondary signal. "
            f"{stage_pressure} {resistance} "
            f"The Healthy PType story shows the regulation path."
        ),
        "mapped_stage": mapped_stage,
    }


def generate_development_journey_output(
    stage_key: str,
    dominant_trait: str,
    mood_score: int,
    trait_scores: Dict[str, float],
    stage_data: Dict[str, dict],
    stage_details: Dict[str, str],
    opportunities: list,
    fairy_whisper: str,
) -> str:
    """
    Legacy-safe function name.

    Now returns the Z9CoachFree Fairy Session Snap instead of the old
    Development Journey Summary.
    """

    secondary_trait = _secondary_trait(trait_scores, dominant_trait)

    snap = generate_session_snap_readback(
        stage_key=stage_key,
        dominant_trait=dominant_trait,
        secondary_trait=secondary_trait,
        mood_score=mood_score,
        trait_scores=trait_scores,
        stage_data=stage_data,
        session_result=None,
    )

    output = f"""
### Fairy Session Snap

**Session Signal:** {snap["session_signal"]}

**State Movement:** {snap["state_movement"]}

**Stage Pressure:** {snap["stage_pressure"]}

**PType Resistance:** {snap["ptype_resistance"]}

**Regulation Cue:** {snap["regulation_cue"]}

**Healthy Narrative Path:**  
{snap["healthy_story"]}

{snap["ptype_url"]}

**Snapshot Note:**  
{snap["compact"]}

State made visible. DISC identifies the state pattern. PType reveals the same state through narrative movement.
"""

    return output
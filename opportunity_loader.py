from typing import Optional


PTYPE_BASE_URL = "https://z9coach.com/ptype/"


DISC_NAMES = {
    "D": "Direction",
    "I": "Expression",
    "S": "Stability",
    "C": "Clarity",
}


def _normalize_stage(stage: Optional[str]) -> str:
    """
    Convert incoming stage values into the numeric query value expected by the PType archive.
    Accepts values like:
    - "5"
    - "Stage 5"
    - "Stage 5 (Identity)"
    """

    if not stage:
        return "1"

    digits = "".join(ch for ch in str(stage) if ch.isdigit())

    if digits:
        return digits

    return "1"


def _get_primary_and_secondary(traits: dict[str, float]) -> tuple[str, str]:
    """
    Return primary and secondary DISC signals from the scored trait dictionary.
    """

    ordered = sorted(
        traits.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    primary = ordered[0][0] if ordered else "D"
    secondary = ordered[1][0] if len(ordered) > 1 else primary

    return primary, secondary


def build_ptype_story_url(
    traits: dict[str, float],
    stage: Optional[str] = None,
    ohu: str = "Healthy",
) -> str:
    """
    Build the canonical PType archive URL from the user's CoachFree result.

    CoachFree uses Healthy as the regulation-story CTA.
    Lite/Pro can later deepen into Overdeveloped/Underdeveloped routing.
    """

    if not traits:
        return f"{PTYPE_BASE_URL}?stage=1&type=D&subtype=DD&ohu=Healthy"

    primary, secondary = _get_primary_and_secondary(traits)
    subtype = f"{primary}{secondary}"
    stage_value = _normalize_stage(stage)

    return (
        f"{PTYPE_BASE_URL}"
        f"?stage={stage_value}"
        f"&type={primary}"
        f"&subtype={subtype}"
        f"&ohu={ohu}"
    )


def load_basic_opportunities(
    traits: dict[str, float],
    mood: int,
    stage: Optional[str] = None,
    location: Optional[str] = None,
) -> list[str]:
    """
    Return the Z9CoachFree narrative opportunity.

    This no longer generates generic action opportunities or product CTAs.
    The opportunity is the Healthy PType regulation story connected to the user's
    stage, primary DISC signal, and subtype path.
    """

    if not traits:
        return [
            "Complete the assessment to reveal the Healthy PType regulation story connected to your current state."
        ]

    primary, secondary = _get_primary_and_secondary(traits)
    subtype = f"{primary}{secondary}"
    stage_value = _normalize_stage(stage)
    story_url = build_ptype_story_url(
        traits=traits,
        stage=stage_value,
        ohu="Healthy",
    )

    primary_name = DISC_NAMES.get(primary, primary)
    secondary_name = DISC_NAMES.get(secondary, secondary)

    return [
        (
            f"Open the Healthy PType regulation story: {story_url}\n\n"
            f"Your current state is reading through the **{primary_name}** doorway "
            f"with **{secondary_name}** as the secondary signal. "
            f"That creates the **{subtype}** narrative path at Stage {stage_value}.\n\n"
            f"DISC identifies the state pattern. "
            f"PType reveals the same state through narrative movement. "
            f"The Healthy story shows how this pattern can regulate without losing its core strength."
        )
    ]
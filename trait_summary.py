from typing import Dict


DISC_LABELS = {
    "D": "Dominance",
    "I": "Influence",
    "S": "Steadiness",
    "C": "Conscientiousness",
}


TYPE_ARCHIVE_PATHS = {
    "D": "https://z9coach.com/ptype/d/",
    "I": "https://z9coach.com/ptype/i/",
    "S": "https://z9coach.com/ptype/s/",
    "C": "https://z9coach.com/ptype/c/",
}


SUMMARIES: Dict[str, Dict[str, str]] = {
    "D": {
        "doorway": "Direction",
        "ptype_name": "Donte",
        "expression_band": "Pressure, pace, decision-making, control, and forward motion.",
        "state": "This state moves toward action when pressure enters the room. It wants a decision, a direction, and a path forward.",
        "growth": "The cleanest first move is not more force. It is direction with timing.",
        "watch": "When this pattern tightens, urgency can make support look like resistance.",
        "ptype": "PType reveals this same state through Donte: the person carrying leadership load, control pressure, trust tension, and execution weight.",
        "first_move": "Choose one decision that can be moved forward without forcing the whole room to move with it.",
    },
    "I": {
        "doorway": "Expression",
        "ptype_name": "Isaac",
        "expression_band": "Connection, visibility, energy, attention, and emotional movement.",
        "state": "This state moves through the room by bringing life back into it. It looks for response, recognition, and a place for the spark to land.",
        "growth": "The cleanest first move is not louder expression. It is expression with a place to land.",
        "watch": "When this pattern tightens, performance can cover the quieter need to be known honestly.",
        "ptype": "PType reveals this same state through Isaac: the person carrying charm, belonging pressure, emotional visibility, and identity under attention.",
        "first_move": "Say the real idea out loud, then give it one clear container so it can become useful.",
    },
    "S": {
        "doorway": "Stability",
        "ptype_name": "Samantha",
        "expression_band": "Pacing, care, consistency, emotional safety, and relational steadiness.",
        "state": "This state protects the room from destabilizing. It listens for tension, tracks the emotional temperature, and tries to keep the rhythm intact.",
        "growth": "The cleanest first move is not more peacekeeping. It is care with self-inclusion.",
        "watch": "When this pattern tightens, harmony can become silence, over-responsibility, or delayed honesty.",
        "ptype": "PType reveals this same state through Samantha: the person carrying care, boundaries, belonging, sustainability, and quiet courage.",
        "first_move": "Name one need before adjusting yourself around everyone else’s needs.",
    },
    "C": {
        "doorway": "Clarity",
        "ptype_name": "Caleb",
        "expression_band": "Standards, precision, preparation, structure, and reliability.",
        "state": "This state searches for the clean line. It wants the system, the standard, the evidence, and the structure before the next move is trusted.",
        "growth": "The cleanest first move is not more analysis. It is clarity that stays connected to the human moment.",
        "watch": "When this pattern tightens, standards can become pressure and analysis can become distance.",
        "ptype": "PType reveals this same state through Caleb: the person carrying trust, control, perfection, systems, vulnerability, and completion.",
        "first_move": "Create the smallest useful structure, then act before the structure becomes another delay.",
    },
}


def summarize_trait(traits: dict, stage: str, mood: int) -> str:
    """Return the CoachFree state summary using the current Z9Coach DISC/PType language."""
    if not traits:
        return (
            "Your snapshot does not contain enough trait data yet. "
            "Complete the assessment to generate a state-visible summary."
        )

    top_trait = max(traits.keys(), key=lambda k: traits[k])
    data = SUMMARIES.get(top_trait)

    if not data:
        return (
            "Your snapshot shows a blended signal. The pattern is not absent; it is simply less singular. "
            "Use the 9-Pillar report to notice which state keeps stepping forward."
        )

    label = DISC_LABELS.get(top_trait, top_trait)
    archive_url = TYPE_ARCHIVE_PATHS.get(top_trait, "https://z9coach.com/ptype/")

    return (
        f"**State made visible — {label}.**  \n"
        f"**Primary Doorway:** {data['doorway']}  \n"
        f"**Expression Band:** {data['expression_band']}  \n\n"
        f"{data['state']}  \n\n"
        f"**Current stage context:** {stage}. **Mood input:** {mood}/10.  \n"
        f"Behavior is not random. It is shaped by history, pressure, and the stage of life you are moving through.  \n\n"
        f"**Best First Move:** {data['first_move']}  \n\n"
        f"**Watch for:** {data['watch']}  \n\n"
        f"**P-Type:** {data['ptype']}  \n"
        f"DISC identifies the state pattern. PType reveals the same state through narrative movement.  \n\n"
        f"[Open the matching PType narrative wing]({archive_url})"
    )
# File: visuals.py
# Title: Z9CoachFree Visual Stack

import math
from typing import Any, Dict, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


DISC_NAMES = {
    "D": "Direction",
    "I": "Expression",
    "S": "Stability",
    "C": "Clarity",
}

PILLAR_TITLES = [
    "DISC Identity",
    "Developmental Stages",
    "Motivation Systems",
    "Cognitive Dissonance",
    "Self-Actualization",
    "Social Learning",
    "Zone of Proximal Development",
    "Spiral Harmony",
    "Resonance & Recursion",
]


def _ordered_traits(traits: Dict[str, float]) -> list[tuple[str, float]]:
    return sorted(traits.items(), key=lambda item: item[1], reverse=True)


def _primary_secondary(traits: Dict[str, float]) -> tuple[str, str]:
    ordered = _ordered_traits(traits)
    primary = ordered[0][0] if ordered else "D"
    secondary = ordered[1][0] if len(ordered) > 1 else primary
    return primary, secondary


def generate_result_snapshot_card(snapshot: Dict[str, Any]) -> Figure:
    """
    Visual 1: Result Snapshot Card.

    Shows the immediate Z9CoachFree state readback.
    """

    fields = [
        "Primary Doorway",
        "Secondary Signal",
        "P-Type",
        "Expression Band",
        "Current Stage Context",
        "Best First Move",
    ]

    fig, ax = plt.subplots(figsize=(8, 5.2))
    ax.axis("off")

    ax.text(
        0.03,
        0.94,
        "Z9CoachFree State Snapshot",
        fontsize=17,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.03,
        0.88,
        "State made visible.",
        fontsize=11,
        transform=ax.transAxes,
    )

    y = 0.78
    for field in fields:
        value = snapshot.get(field, "-")
        ax.text(
            0.04,
            y,
            field,
            fontsize=10,
            fontweight="bold",
            transform=ax.transAxes,
        )
        value_x = 0.32

        # Long labels need extra spacing
        if field == "Current Stage Context":
            value_x = 0.40

        ax.text(
            value_x,
            y,
            str(value),
            fontsize=10,
            transform=ax.transAxes,
            wrap=True,
        )
        y -= 0.12

    return fig


def generate_radar_chart(
    traits: Dict[str, float],
    title: str = "DISC Identity Signal",
) -> Figure:
    """
    Visual 2: DISC Identity Signal.

    Keeps the radar chart but reframes it as the active state signal.
    """

    labels = list(traits.keys())
    values = list(traits.values())

    if not labels:
        labels = ["D", "I", "S", "C"]
        values = [0, 0, 0, 0]

    values = values + [values[0]]
    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    angles = angles + [angles[0]]

    primary, secondary = _primary_secondary(traits)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.22)

    ax.set_title(
        f"{title}\nPrimary: {DISC_NAMES.get(primary, primary)} | Secondary: {DISC_NAMES.get(secondary, secondary)}",
        pad=18,
    )
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])

    return fig


def generate_stage_pressure_map(
    stage: str,
    path_map: Dict[str, Dict[str, Any]],
    primary_trait: str,
    title: str = "Stage Pressure Map",
) -> Figure:
    """
    Visual 3: Stage Pressure Map.

    Uses the updated stage_path_map.json structure:
    - stage_pressure
    - ptype_resistance
    - stabilizes_through
    - watch_for
    - next_move
    """

    stage_data = path_map.get(stage, {})
    resistance = stage_data.get("ptype_resistance", {}).get(primary_trait, "-")

    rows = [
        ("Stage Pressure", stage_data.get("stage_pressure", "-")),
        ("PType Resistance", resistance),
        ("Stabilizes Through", stage_data.get("stabilizes_through", "-")),
        ("Watch For", stage_data.get("watch_for", "-")),
        ("Next Move", stage_data.get("next_move", "-")),
    ]

    fig, ax = plt.subplots(figsize=(9, 5.6))
    ax.axis("off")

    ax.text(
        0.03,
        0.94,
        title,
        fontsize=16,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.03,
        0.88,
        f"{stage} | {DISC_NAMES.get(primary_trait, primary_trait)} resistance path",
        fontsize=10,
        transform=ax.transAxes,
    )

    y = 0.76
    for label, value in rows:
        ax.text(
            0.04,
            y,
            label,
            fontsize=10,
            fontweight="bold",
            transform=ax.transAxes,
        )
        ax.text(
            0.28,
            y,
            str(value),
            fontsize=9.5,
            transform=ax.transAxes,
            wrap=True,
        )
        y -= 0.14

    return fig


def generate_ptype_narrative_cta(
    ptype_url: str,
    stage: str,
    primary_trait: str,
    secondary_trait: str,
    ohu: str = "Healthy",
) -> Figure:
    """
    Visual 4: Healthy PType Narrative CTA.

    Replaces old opportunity/product visuals.
    """

    subtype = f"{primary_trait}{secondary_trait}"

    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    ax.axis("off")

    ax.text(
        0.04,
        0.82,
        "Healthy PType Narrative Path",
        fontsize=16,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.04,
        0.68,
        "DISC identifies the state pattern. PType reveals the same state through narrative movement.",
        fontsize=10,
        transform=ax.transAxes,
        wrap=True,
    )
    ax.text(
        0.04,
        0.48,
        f"Stage: {stage}   |   P-Type: {subtype}   |   Read: {ohu}",
        fontsize=11,
        fontweight="bold",
        transform=ax.transAxes,
    )
    ax.text(
        0.04,
        0.31,
        "Start with the Healthy regulation story before moving into deeper archive or product pathways.",
        fontsize=10,
        transform=ax.transAxes,
        wrap=True,
    )

    return fig


def generate_pillar_mirror_strip(
    pillar_notes: Dict[str, str],
    title: str = "Light 9-Pillar State Mirror",
) -> Figure:
    """
    Optional CoachFree visual: compact 9-pillar readback strip.
    """

    fig, ax = plt.subplots(figsize=(9, 8))
    ax.axis("off")

    ax.text(
        0.03,
        0.96,
        title,
        fontsize=16,
        fontweight="bold",
        transform=ax.transAxes,
    )

    y = 0.88
    for index, pillar in enumerate(PILLAR_TITLES, start=1):
        note = pillar_notes.get(pillar, "This pillar is visible in the current state snapshot.")
        ax.text(
            0.04,
            y,
            f"{index}. {pillar}",
            fontsize=10,
            fontweight="bold",
            transform=ax.transAxes,
        )
        note_x = 0.33

        if pillar in {"Zone of Proximal Development", "Resonance & Recursion"}:
            note_x = 0.44

        ax.text(
            note_x,
            y,
            note,
            fontsize=9,
            transform=ax.transAxes,
            wrap=True,
        )
        y -= 0.085

    return fig


# Legacy-safe aliases.
# These keep older app calls from breaking while using the updated CoachFree naming.

def project_spiral(
    traits: Dict[str, float],
    recursion_score: float = 3.0,
    negated_traits: Optional[Dict[str, float]] = None,
    title: str = "Spiral State Projection",
) -> Figure:
    labels = list(traits.keys())
    base = [traits[t] / 100 * recursion_score for t in labels] if labels else [0, 0, 0, 0]
    labels = labels or ["D", "I", "S", "C"]
    base = base + [base[0]]
    angles = np.linspace(0, 2 * math.pi, len(labels) + 1)

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, base, linewidth=2, label="State signal")
    ax.fill(angles, base, alpha=0.18)

    if negated_traits:
        neg = [negated_traits.get(t, 0) / 100 * recursion_score for t in labels]
        neg = neg + [neg[0]]
        ax.plot(angles, neg, linestyle="--", label="Damped signal")
        ax.fill(angles, neg, alpha=0.08)

    ax.set_title(title)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.legend(loc="upper right")
    return fig


def plot_circular_stage_map(
    current_index: int,
    next_index: int,
    labels: Optional[list[str]] = None,
    title: str = "Developmental Stage Map",
) -> Figure:
    if labels is None:
        labels = [f"Stage {i + 1}" for i in range(8)]

    radius = 2.5
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axis("off")

    for i, label in enumerate(labels):
        angle = 2 * math.pi * i / len(labels)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        weight = "bold" if i in {current_index, next_index} else "normal"
        display = f"{label}"
        if i == current_index:
            display = f"{label}\nCurrent"
        elif i == next_index:
            display = f"{label}\nNext"

        ax.text(
            x,
            y,
            display,
            ha="center",
            va="center",
            fontsize=10,
            fontweight=weight,
        )

    ax.set_title(title)
    return fig


def plot_stage_histogram(traits: dict, stage_index: int) -> Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = list(traits.keys())
    values = list(traits.values())

    ax.bar(bars, values)
    ax.set_title(f"Primary State Signals for Stage {stage_index + 1}")
    ax.set_xlabel("DISC Signal")
    ax.set_ylabel("Score")
    ax.set_ylim(0, max(values) + 5 if values else 10)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    return fig


def plot_development_path(
    perceived_idx: int,
    auto_idx: int,
    ee_summaries: Dict[str, Any],
    path_map: Dict[str, Dict[str, Any]],
    dominant_trait: str,
) -> Figure:
    """
    Compatibility function for older app calls.

    Updated to read the new stage_path_map.json structure.
    """

    step = 1 if auto_idx >= perceived_idx else -1
    indices = list(range(perceived_idx, auto_idx + step, step))
    stages = [f"Stage {i + 1}" for i in indices]

    fig, ax = plt.subplots(figsize=(9, max(len(stages) * 1.7, 4)))
    ax.axis("off")

    y_positions = list(range(len(stages)))[::-1]

    for idx, (stage, y) in enumerate(zip(stages, y_positions)):
        stage_data = path_map.get(stage, {})
        resistance = stage_data.get("ptype_resistance", {}).get(dominant_trait, "-")

        ax.text(0.02, y, stage, fontsize=12, fontweight="bold")
        ax.text(0.18, y, f"Pressure: {stage_data.get('stage_pressure', '-')}", fontsize=9)
        ax.text(0.18, y - 0.28, f"Resistance: {resistance}", fontsize=9)
        ax.text(0.18, y - 0.56, f"Next Move: {stage_data.get('next_move', '-')}", fontsize=9)

        if idx < len(stages) - 1:
            ax.plot(
                [0.05, 0.05],
                [y - 0.1, y_positions[idx + 1] + 0.1],
                linewidth=1,
            )

    ax.set_ylim(-1, len(stages))
    ax.set_title("Stage Movement Path", pad=20)
    return fig
# File: z9CoachFree.py
# Title: Z9CoachFree State Snapshot App

import random
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from analyze_profile import analyze_profile
from fairy_coachfree import generate_fairy_whisper, generate_session_snap_readback
from opportunity_loader import build_ptype_story_url, load_basic_opportunities
from pdf_export import generate_simple_report
from style_helpers import (
    apply_z9_luxury_theme,
    render_card,
    render_hero,
    render_metadata,
    render_narrative_cta,
    render_section,
    render_snapshot_grid,
)
from trait_summary import summarize_trait
from utils import load_json_file, save_json_file
from visuals import (
    generate_pillar_mirror_strip,
    generate_ptype_narrative_cta,
    generate_radar_chart,
    generate_result_snapshot_card,
    generate_stage_pressure_map,
)
from z9_spiral_logic import map_disc_to_stage


DEFAULT_STAGE_SUMMARIES = {f"Stage {i}": "" for i in range(1, 9)}


def safe_load(path: str, default: Any) -> Any:
    try:
        return load_json_file(path)
    except FileNotFoundError:
        return default


def load_questions() -> List[Dict[str, Any]]:
    try:
        return load_json_file("master_disc_questions1.json")
    except FileNotFoundError:
        return load_json_file("master_disc_questions.json")


def initialize_questions(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if "coachfree_sampled_questions" not in st.session_state:
        sample_size = min(16, len(questions))
        st.session_state.coachfree_sampled_questions = random.sample(questions, sample_size)
    return st.session_state.coachfree_sampled_questions


def normalize_answer_score(answer: str) -> int:
    value = str(answer).strip()

    if value.startswith("Strongly Agree"):
        return 5
    if value.startswith("Agree"):
        return 4
    if value.startswith("Neutral"):
        return 3
    if value.startswith("Disagree"):
        return 2
    if value.startswith("Strongly Disagree"):
        return 1

    return 0


def dominant_trait(profile: Dict[str, Any]) -> str:
    return max(profile["traits"], key=profile["traits"].get)


def secondary_trait(traits: Dict[str, float], primary: str) -> str:
    ordered = sorted(traits.items(), key=lambda item: item[1], reverse=True)
    return ordered[1][0] if len(ordered) > 1 else primary


def stage_number(stage: str) -> str:
    digits = "".join(ch for ch in str(stage) if ch.isdigit())
    return digits or "1"


def log_profile(profile: dict, final_stage: str) -> None:
    entry = {
        "timestamp": pd.Timestamp.now().isoformat(),
        "traits": profile["traits"],
        "trait_score": profile["trait_score"],
        "harmony_ratio": profile["harmony_ratio"],
        "stage": final_stage,
    }
    log = safe_load("assessment_log.json", default=[])
    log.append(entry)
    save_json_file(log, "assessment_log.json")


def render_sidebar(stage_summaries: Dict[str, str]) -> None:
    st.sidebar.subheader("Stage Notes")
    for label, tip in stage_summaries.items():
        st.sidebar.markdown(f"**{label}**: {tip}")

    st.sidebar.markdown("---")
    st.sidebar.caption("Z9CoachFree is the recognition layer. Lite adds continuity.")


def render_assessment_form(
    questions: List[Dict[str, Any]],
    stage_summaries: Dict[str, str],
) -> tuple[bool, Dict[int, str], str]:
    sampled = initialize_questions(questions)

    with st.form("z9coachfree_assessment"):
        st.subheader("DISC State Assessment")
        st.caption(
            "Answer from your present state. This is a state snapshot, not a permanent identity label."
        )

        responses: Dict[int, str] = {}

        for idx, question in enumerate(sampled):
            responses[idx] = st.radio(
                question["question"],
                question["options"],
                key=f"q_{idx}",
                horizontal=False,
            )

        st.subheader("Developmental Stage Context")
        perceived = st.selectbox(
            "Select the stage that feels most active today:",
            list(stage_summaries.keys()),
        )

        submit = st.form_submit_button("Generate Z9CoachFree State Snapshot")

    return submit, responses, perceived


def score_assessment(
    sampled: List[Dict[str, Any]],
    responses: Dict[int, str],
) -> tuple[float, float, float, float]:
    d = i = s = c = 0.0

    for idx, question in enumerate(sampled):
        val = normalize_answer_score(responses[idx])
        trait = question.get("trait")

        if trait == "D":
            d += val
        elif trait == "I":
            i += val
        elif trait == "S":
            s += val
        elif trait == "C":
            c += val

    return d, i, s, c


def render_stage_pressure_cards(
    stage: str,
    path_map: Dict[str, Dict[str, Any]],
    primary: str,
) -> None:
    stage_key = f"Stage {stage_number(stage)}"
    stage_data = path_map.get(stage_key, {})

    render_card(
        "Stage Pressure",
        stage_data.get(
            "stage_pressure",
            "The current state is showing pressure through the mapped stage layer.",
        ),
    )

    resistance = stage_data.get("ptype_resistance", {}).get(
        primary,
        "This state may resist movement by protecting its familiar pattern.",
    )
    render_card("PType Resistance", resistance)

    render_card(
        "Regulation Cue",
        stage_data.get(
            "next_move",
            "This movement tends to stabilize when the state can be noticed without being forced.",
        ),
    )


def main() -> None:
    st.set_page_config(
        page_title="Z9CoachFree State Snapshot",
        layout="wide",
    )

    apply_z9_luxury_theme()

    render_hero(
        "Z9CoachFree",
        (
            "State made visible. Generate a first-read DISC snapshot, see the stage pressure "
            "beneath it, and open the Healthy PType narrative path connected to your current state."
        ),
    )

    stage_summaries = safe_load("stage_summaries.json", DEFAULT_STAGE_SUMMARIES)
    path_map = safe_load("stage_path_map.json", {})
    questions = load_questions()

    render_sidebar(stage_summaries)

    render_section(
        "Orientation",
        "CoachFree identifies the current state pattern. PType reveals the same state through narrative movement.",
    )
    render_metadata(
        {
            "Layer": "Recognition",
            "Output": "State Snapshot",
            "Narrative Route": "Healthy PType",
            "Next Depth": "Lite",
        }
    )

    render_section(
        "Mood / State Input",
        "This anchors the snapshot in the present moment.",
    )
    mood = st.slider("Current state input", 0, 10, 5, 1)
    st.markdown(f"**Current state:** {mood}/10")

    render_section(
        "Assessment",
        "The scoring logic remains preserved. The presentation layer is what has changed.",
    )
    submit, responses, perceived_stage = render_assessment_form(questions, stage_summaries)

    if not submit:
        render_section(
            "Snapshot Preview",
            "Complete the assessment to generate your Z9CoachFree State Snapshot.",
        )
        render_card(
            "What this creates",
            (
                "A recognition-level report with Primary Doorway, Secondary Signal, P-Type, "
                "Expression Band, Stage Pressure, Healthy PType path, and Light 9-Pillar Mirror."
            ),
        )
        return

    sampled = st.session_state.coachfree_sampled_questions

    # ========================= LOCKED ASSESSMENT LOGIC =========================
    # Scoring math and profile analysis remain protected. This block only normalizes
    # answer strings so both the old and updated question files score correctly.
    d, i, s, c = score_assessment(sampled, responses)
    profile = analyze_profile(d, i, s, c, stage_label=perceived_stage)
    auto_stage = map_disc_to_stage(d, i, s, c)

    if not auto_stage or not auto_stage.startswith("Stage "):
        auto_stage = "Stage 1"
    # ======================= END LOCKED ASSESSMENT LOGIC =======================

    primary = dominant_trait(profile)
    secondary = secondary_trait(profile["traits"], primary)
    subtype = f"{primary}{secondary}"
    current_stage_number = stage_number(auto_stage)

    trait_snapshot = summarize_trait(profile["traits"], auto_stage, mood)
    snapshot = trait_snapshot.get("snapshot", {})
    pillar_notes = trait_snapshot.get("pillar_notes", {})

    ptype_url = build_ptype_story_url(
        traits=profile["traits"],
        stage=current_stage_number,
        ohu="Healthy",
    )

    fairy_snap = generate_session_snap_readback(
        stage_key=auto_stage,
        dominant_trait=primary,
        secondary_trait=secondary,
        mood_score=mood,
        trait_scores=profile["traits"],
        stage_data=path_map,
        session_result=None,
    )

    opportunities = load_basic_opportunities(
        traits=profile["traits"],
        mood=mood,
        stage=auto_stage,
    )

    log_profile(profile, auto_stage)

    render_section(
        "Z9CoachFree State Snapshot",
        "The immediate recognition layer generated from the Z9Coach matrix system.",
    )
    render_metadata(
        {
            "Primary": snapshot.get("Primary Doorway", primary),
            "Secondary": snapshot.get("Secondary Signal", secondary),
            "P-Type": snapshot.get("P-Type", subtype),
            "Stage": snapshot.get("Current Stage Context", auto_stage),
            "Mood": f"{mood}/10",
        }
    )
    render_snapshot_grid(snapshot)

    st.pyplot(generate_result_snapshot_card(snapshot))

    render_section(
        "Current State Readback",
        "The state is being reflected, not fixed into a permanent label.",
    )
    render_card("State Readback", trait_snapshot.get("state_readback", ""))
    render_card("Watch For", trait_snapshot.get("watch_for", ""))

    render_section(
        "DISC Identity Signal",
        "DISC identifies the state pattern.",
    )
    st.pyplot(generate_radar_chart(profile["traits"]))

    render_section(
        "Stage Pressure Map",
        "Stage context shows where the pressure gathers and how this type may resist movement.",
    )
    render_stage_pressure_cards(auto_stage, path_map, primary)
    st.pyplot(
        generate_stage_pressure_map(
            stage=f"Stage {current_stage_number}",
            path_map=path_map,
            primary_trait=primary,
        )
    )

    render_section(
        "Fairy Session Snap",
        "The Fairy voice now reads the session/render movement instead of giving generic encouragement.",
    )
    render_card("Session Signal", fairy_snap["session_signal"])
    render_card("State Movement", fairy_snap["state_movement"])
    render_card("Change Readback", fairy_snap["change_readback"])
    render_card("Regulation Cue", fairy_snap["regulation_cue"])

    render_section(
        "Healthy PType Narrative Path",
        "The app now routes from product CTA to narrative CTA.",
    )
    render_narrative_cta(
        "Open the Healthy Regulation Story",
        (
            "Start with the Healthy PType narrative. It shows how this state can regulate "
            "without losing its core strength."
        ),
        ptype_url,
        f"Open Stage {current_stage_number} / {subtype} / Healthy",
    )
    st.pyplot(
        generate_ptype_narrative_cta(
            ptype_url=ptype_url,
            stage=f"Stage {current_stage_number}",
            primary_trait=primary,
            secondary_trait=secondary,
            ohu="Healthy",
        )
    )

    if opportunities:
        render_card("Narrative Opportunity", opportunities[0])

    render_section(
        "Light 9-Pillar State Mirror",
        "This is the recognition-level pillar readback. Lite, Pro, and Plus deepen this same structure.",
    )
    st.pyplot(generate_pillar_mirror_strip(pillar_notes))

    for index, (title, note) in enumerate(pillar_notes.items(), start=1):
        render_card(f"Pillar {index}: {title}", note)

    render_section(
        "Download Snapshot",
        "Export the Z9CoachFree State Snapshot as a PDF.",
    )

    report_data = {
        "trait_summary": trait_snapshot,
        "dominant_trait": primary,
        "secondary_trait": secondary,
        "ptype": subtype,
        "stage": auto_stage,
        "mood": mood,
        "alignment_cue": fairy_snap["compact"],
        "pillars": [],
    }

    pdf_bytes = generate_simple_report(report_data)

    st.download_button(
        "Download Z9CoachFree State Snapshot",
        pdf_bytes,
        "Z9CoachFree_State_Snapshot.pdf",
        "application/pdf",
    )

    render_section(
        "Next Path",
        "CoachFree recognizes. Lite adds profile/session continuity. Pro adds recursive interpretation. Plus adds longitudinal integration.",
    )
    render_card(
        "Next Depth",
        (
            "Return later to compare the state again, or continue into Lite when you are ready "
            "for Profile Snap, Session/Game Snap, 9-Pillar perspective, Combined Report, and update reports."
        ),
    )

    st.markdown("---")
    st.caption(
        "Z9CoachFree. State made visible. DISC identifies the state pattern. "
        "PType reveals the same state through narrative movement."
    )


if __name__ == "__main__":
    main()
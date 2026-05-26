# File: pdf_export.py
# Title: Z9CoachFree State Snapshot PDF Export

from typing import Any, Dict

from fpdf import FPDF


SLATE = (17, 24, 39)
NAVY = (23, 32, 51)
GOLD = (201, 162, 74)
GOLD_SOFT = (234, 217, 157)
IVORY = (251, 247, 239)
INK = (31, 41, 55)

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

PILLAR_FALLBACKS = {
    "DISC Identity": "The report begins by identifying the dominant state signal.",
    "Developmental Stages": "The state is read inside its current developmental pressure.",
    "Motivation Systems": "The next move should create motion without forcing the whole system.",
    "Cognitive Dissonance": "This names where visible behavior and inner pressure may split.",
    "Self-Actualization": "The state is reflected as movement, not a fixed identity.",
    "Social Learning": "The pattern may have been practiced before it was consciously chosen.",
    "Zone of Proximal Development": "The next step should stretch the state without overwhelming it.",
    "Spiral Harmony": "The snapshot shows one point in a larger movement pattern.",
    "Resonance & Recursion": "The state should be revisited later, not judged permanently.",
}


def clean_text(text: Any) -> str:
    if text is None:
        return ""
    return (
        str(text)
        .replace("’", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
        .replace("•", "-")
        .replace("\xa0", " ")
        .replace("\u200b", "")
        .strip()
    )


class Z9ReportPDF(FPDF):
    def header(self) -> None:
        if self.page_no() == 1:
            return
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*GOLD)
        self.cell(0, 8, "Z9CoachFree State Snapshot", align="R", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")


def _usable_width(pdf: FPDF) -> float:
    return pdf.w - pdf.l_margin - pdf.r_margin


def _section_title(pdf: FPDF, title: str) -> None:
    pdf.set_text_color(*GOLD)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 9, clean_text(title), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*GOLD)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(5)


def _body(pdf: FPDF, text: Any, size: int = 10, line_height: int = 6) -> None:
    if not text:
        return
    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(_usable_width(pdf), line_height, clean_text(text))
    pdf.ln(2)


def _metadata_strip(pdf: FPDF, metadata: Dict[str, Any]) -> None:
    pdf.set_fill_color(*NAVY)
    pdf.set_draw_color(*GOLD)
    pdf.set_text_color(*IVORY)
    pdf.set_font("Helvetica", "B", 9)

    labels = list(metadata.items())
    col_width = _usable_width(pdf) / max(len(labels), 1)
    y = pdf.get_y()
    x = pdf.l_margin

    for label, value in labels:
        pdf.set_xy(x, y)
        pdf.cell(col_width, 8, clean_text(label).upper(), border=1, fill=True)
        pdf.set_xy(x, y + 8)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*IVORY)
        pdf.cell(col_width, 9, clean_text(value), border=1, fill=True)
        pdf.set_font("Helvetica", "B", 9)
        x += col_width

    pdf.set_y(y + 22)
    pdf.ln(2)


def _snapshot_table(pdf: FPDF, snapshot: Dict[str, Any]) -> None:
    label_w = 56
    value_w = _usable_width(pdf) - label_w

    pdf.set_draw_color(222, 203, 145)

    for label, value in snapshot.items():
        if value in ("", None, "-"):
            continue

        y_start = pdf.get_y()
        if y_start > 250:
            pdf.add_page()
            y_start = pdf.get_y()

        text = clean_text(value)
        line_h = 7
        row_h = max(10, 7 * (len(text) // 70 + 1))

        pdf.set_xy(pdf.l_margin, y_start)
        pdf.set_fill_color(*GOLD_SOFT)
        pdf.set_text_color(*INK)
        pdf.set_font("Helvetica", "B", 9)
        pdf.multi_cell(label_w, row_h, clean_text(label), border=1, fill=True)

        pdf.set_xy(pdf.l_margin + label_w, y_start)
        pdf.set_fill_color(246, 240, 226)
        pdf.set_text_color(*INK)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(value_w, line_h, text, border=1, fill=True)

        pdf.set_y(max(pdf.get_y(), y_start + row_h))


def _pillar_card(pdf: FPDF, title: str, note: str, number: int) -> None:
    if pdf.get_y() > 245:
        pdf.add_page()

    width = _usable_width(pdf)

    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "B", 10)
    pdf.multi_cell(width, 6, f"{number}. {clean_text(title)}", border=0)

    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "", 9)
    pdf.multi_cell(width, 5.5, clean_text(note), border=0)

    pdf.ln(3)


def _coerce_snapshot(data: Dict[str, Any]) -> Dict[str, Any]:
    trait_summary = data.get("trait_summary", {})
    if isinstance(trait_summary, dict):
        return trait_summary

    return {
        "title": "Z9CoachFree State Snapshot",
        "headline": f"State made visible - {data.get('dominant_trait', '-')}",
        "snapshot": {
            "Primary Doorway": data.get("dominant_trait", "-"),
            "Secondary Signal": data.get("secondary_trait", "-"),
            "P-Type": data.get("ptype", "-"),
            "Expression Band": data.get("expression_band", "-"),
            "Current Stage Context": data.get("stage", "-"),
            "Best First Move": data.get("best_first_move", "Open the Healthy PType regulation story."),
        },
        "state_readback": "",
        "watch_for": data.get("alignment_cue", ""),
        "ptype_bridge": data.get(
            "ptype_bridge",
            "DISC identifies the state pattern. PType reveals the same state through narrative movement.",
        ),
        "pillar_notes": {},
        "next_path": {},
    }


def _pdf_bytes(pdf: FPDF) -> bytes:
    output = pdf.output()
    if isinstance(output, bytes):
        return output
    if isinstance(output, bytearray):
        return bytes(output)
    return str(output).encode("latin-1", errors="replace")


def generate_simple_report(data: Dict[str, Any]) -> bytes:
    snapshot_payload = _coerce_snapshot(data)
    snapshot = snapshot_payload.get("snapshot", {})

    if not snapshot:
        snapshot = {
            "Primary Doorway": data.get("dominant_trait", "-"),
            "Secondary Signal": data.get("secondary_trait", "-"),
            "P-Type": data.get("ptype", "-"),
            "Expression Band": data.get("expression_band", "-"),
            "Current Stage Context": data.get("stage", "-"),
            "Best First Move": data.get(
                "best_first_move",
                "Open the Healthy PType regulation story and notice how this state stabilizes.",
            ),
        }

    pillar_notes = snapshot_payload.get("pillar_notes", {}) or {}
    next_path = snapshot_payload.get("next_path", {}) or {}

    pdf = Z9ReportPDF()
    pdf.set_auto_page_break(auto=True, margin=16)
    pdf.add_page()

    pdf.set_fill_color(*SLATE)
    pdf.rect(0, 0, pdf.w, pdf.h, style="F")

    pdf.set_text_color(*GOLD)
    pdf.set_font("Helvetica", "B", 25)
    pdf.set_xy(18, 32)
    pdf.multi_cell(0, 12, "Z9CoachFree\nState Snapshot")

    pdf.set_text_color(*IVORY)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_x(18)
    pdf.multi_cell(
        170,
        7,
        "State made visible. A first-read mirror generated from the Z9Coach matrix system.",
    )

    pdf.set_y(112)
    _metadata_strip(
        pdf,
        {
            "Primary": snapshot.get("Primary Doorway", data.get("dominant_trait", "-")),
            "P-Type": snapshot.get("P-Type", data.get("ptype", "-")),
            "Stage": snapshot.get("Current Stage Context", data.get("stage", "-")),
            "Mood": f"{data.get('mood', '-')}/10",
        },
    )

    pdf.set_y(162)
    pdf.set_text_color(*IVORY)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Opening Readback", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(
        _usable_width(pdf),
        6,
        clean_text(
            "This report reflects the current visible state. It is not a permanent identity. "
            "CoachFree is the recognition layer: state first, deeper continuity later."
        ),
    )

    pdf.add_page()
    _section_title(pdf, "Result Snapshot")
    _snapshot_table(pdf, snapshot)

    state_readback = snapshot_payload.get("state_readback", "")
    watch_for = snapshot_payload.get("watch_for", "")

    if state_readback:
        _section_title(pdf, "Current State Readback")
        _body(pdf, state_readback)

    if watch_for:
        _section_title(pdf, "Watch For")
        _body(pdf, watch_for)

    pdf.add_page()
    _section_title(pdf, "DISC / PType Bridge")

    primary = snapshot.get("Primary Doorway", data.get("dominant_trait", "-"))
    secondary = snapshot.get("Secondary Signal", data.get("secondary_trait", "-"))
    ptype = snapshot.get("P-Type", data.get("ptype", "-"))
    stage = snapshot.get("Current Stage Context", data.get("stage", "-"))

    bridge_text = f"""
DISC identifies the visible state pattern.

Your current snapshot is reading through the {primary} doorway with {secondary} as the secondary signal.
That creates the {ptype} narrative pathway inside {stage} pressure.

The DISC matrix explains the structure of the state.
The PType narrative shows how that same state tends to move through relationships, pressure, responsibility, emotion, and self-protection.

The Healthy narrative route does not replace the DISC pattern.
It shows how the pattern can regulate without losing its core strength.

This is where classification becomes lived movement.
"""
    _body(pdf, bridge_text)

    ptype_url = ""
    if isinstance(next_path, dict):
        ptype_url = next_path.get("ptype_archive", "")

    if ptype_url:
        pdf.ln(2)
        pdf.set_text_color(*GOLD)
        pdf.set_font("Helvetica", "U", 10)
        pdf.cell(
            0,
            7,
            "Open the Healthy PType regulation story",
            new_x="LMARGIN",
            new_y="NEXT",
            link=ptype_url,
        )

    pdf.add_page()
    _section_title(pdf, "Light 9-Pillar State Mirror")

    for index, title in enumerate(PILLAR_TITLES, start=1):
        note = pillar_notes.get(title, PILLAR_FALLBACKS.get(title, "This pillar supports the current readback."))
        _pillar_card(pdf, title, note, index)

    pdf.add_page()
    _section_title(pdf, "Best First Move")
    _body(
        pdf,
        snapshot.get(
            "Best First Move",
            "Choose one small movement that makes the current state easier to see and easier to revisit.",
        ),
        size=11,
        line_height=7,
    )

    _section_title(pdf, "Next Path")
    _body(
        pdf,
        "Continue through the DISC matrix to understand the classification layer. "
        "Then use the Healthy PType narrative path to see the same state in motion. "
        "When ready, move toward self-guided programs for deeper structured application.",
    )

    return _pdf_bytes(pdf)
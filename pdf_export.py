from typing import Any, Dict, Iterable

from fpdf import FPDF


SLATE = (17, 24, 39)
NAVY = (23, 32, 51)
GOLD = (201, 162, 74)
IVORY = (251, 247, 239)
INK = (31, 41, 55)
MUTED = (91, 100, 116)


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
        .replace("•", "*")
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
        self.cell(
            0,
            8,
            "Z9CoachFree State Snapshot",
            align="R",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(2)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")


def _section_title(pdf: FPDF, title: str) -> None:
    pdf.set_text_color(*GOLD)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 9, clean_text(title), new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(*GOLD)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(5)


def _body(pdf: FPDF, text: Any, size: int = 10, line_height: int = 6) -> None:
    pdf.set_text_color(*INK)
    pdf.set_font("Helvetica", "", size)
    pdf.multi_cell(0, line_height, clean_text(text))
    pdf.ln(2)


def _metadata_strip(pdf: FPDF, metadata: Dict[str, Any]) -> None:
    pdf.set_fill_color(*NAVY)
    pdf.set_draw_color(*GOLD)
    pdf.set_text_color(*IVORY)
    pdf.set_font("Helvetica", "B", 9)

    labels = list(metadata.items())
    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_width = usable_width / max(len(labels), 1)
    y = pdf.get_y()
    x = pdf.l_margin

    for label, value in labels:
        pdf.set_xy(x, y)
        pdf.cell(col_width, 8, clean_text(label).upper(), border=1, fill=True)
        pdf.set_xy(x, y + 8)
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(col_width, 9, clean_text(value), border=1, fill=True)
        pdf.set_font("Helvetica", "B", 9)
        x += col_width

    pdf.set_y(y + 22)
    pdf.ln(2)


def _snapshot_table(pdf: FPDF, snapshot: Dict[str, Any]) -> None:
    pdf.set_fill_color(246, 240, 226)
    pdf.set_draw_color(222, 203, 145)

    for label, value in snapshot.items():
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*GOLD)
        pdf.cell(48, 7, clean_text(label), border=1, fill=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, 7, clean_text(value), border=1)


def _pillar_card(pdf: FPDF, title: str, note: str, number: int) -> None:
    if pdf.get_y() > 235:
        pdf.add_page()

    pdf.set_fill_color(246, 240, 226)
    pdf.set_draw_color(222, 203, 145)
    pdf.set_text_color(*INK)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(
        0,
        8,
        f"Pillar {number}: {clean_text(title)}",
        border=1,
        fill=True,
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*INK)
    pdf.multi_cell(0, 6, clean_text(note), border=1)
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
            "Best First Move": data.get("best_first_move", "-"),
        },
        "state_readback": trait_summary,
        "watch_for": data.get("alignment_cue", ""),
        "ptype_bridge": data.get(
            "ptype_bridge",
            "DISC identifies the state pattern. PType reveals the same state through narrative movement.",
        ),
        "pillar_notes": {},
        "next_path": {},
    }


def _as_pdf_bytes(output: Any) -> bytes:
    if isinstance(output, bytes):
        return output
    if isinstance(output, bytearray):
        return bytes(output)
    return str(output).encode("latin-1")


def generate_simple_report(data: Dict[str, Any]) -> bytes:
    snapshot_payload = _coerce_snapshot(data)
    snapshot = snapshot_payload.get("snapshot", {})
    pillar_notes = snapshot_payload.get("pillar_notes", {})
    next_path = snapshot_payload.get("next_path", {})

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
        clean_text(
            "State made visible. A first-read mirror generated from the Z9Coach matrix system."
        ),
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
        0,
        6,
        clean_text(
            "This report does not define the person. It reflects the current visible state. "
            "CoachFree is the elementary layer of the reporting ladder: recognition first, "
            "deeper continuity later."
        ),
    )

    pdf.add_page()
    _section_title(pdf, "Result Snapshot")
    _snapshot_table(pdf, snapshot)

    pdf.ln(4)
    _section_title(pdf, "Current State Readback")
    _body(pdf, snapshot_payload.get("state_readback", ""))

    watch_for = snapshot_payload.get("watch_for", "")
    if watch_for:
        _section_title(pdf, "Watch For")
        _body(pdf, watch_for)

    pdf.add_page()
    _section_title(pdf, "DISC / PType Bridge")
    _body(
        pdf,
        snapshot_payload.get(
            "ptype_bridge",
            "DISC identifies the state pattern. PType reveals the same state through narrative movement.",
        ),
    )

    ptype_url = ""
    if isinstance(next_path, dict):
        ptype_url = next_path.get("ptype_archive", "")

    if ptype_url:
        pdf.set_text_color(*GOLD)
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, clean_text(f"Matching PType Archive: {ptype_url}"))
        pdf.ln(2)

    pdf.add_page()
    _section_title(pdf, "Light 9-Pillar State Mirror")

    if pillar_notes:
        for index, title in enumerate(PILLAR_TITLES, start=1):
            _pillar_card(
                pdf,
                title,
                pillar_notes.get(title, "This pillar is visible in the current state snapshot."),
                index,
            )
    else:
        pillars: Iterable[Dict[str, Any]] = data.get("pillars", [])
        for pillar in pillars:
            _pillar_card(
                pdf,
                pillar.get("title", "Untitled Pillar"),
                pillar.get("summary") or pillar.get("means") or pillar.get("shows", ""),
                int(pillar.get("number", 0) or 0),
            )

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
        "Open the matching PType narrative path to see the same state in motion. "
        "Continue into Lite when you are ready for Profile Snap, Session/Game Snap, "
        "9-Pillar perspective, Combined Report, and future update reports.",
    )

    return _as_pdf_bytes(pdf.output(dest="S"))
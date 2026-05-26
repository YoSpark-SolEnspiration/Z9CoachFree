# File: style_helpers.py
# Title: Z9CoachFree Presentation Helpers

import html
from typing import Iterable, Mapping

import streamlit as st


BLUE = "#1f2937"
GOLD = "#c9a24a"
IVORY = "#f8f3ea"


def _render_html(markup: str) -> None:
    """Render trusted app-owned HTML without exposing raw markup in the UI."""
    if hasattr(st, "html"):
        st.html(markup)
    else:
        st.markdown(markup, unsafe_allow_html=True)


def apply_z9_luxury_theme() -> None:
    _render_html(
        """
        <style>
        :root {
            --z9-slate: #111827;
            --z9-navy: #172033;
            --z9-gold: #c9a24a;
            --z9-gold-soft: #ead99d;
            --z9-ivory: #fbf7ef;
            --z9-card: #f8f3ea;
            --z9-ink: #1f2937;
            --z9-line: rgba(201, 162, 74, 0.34);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(201, 162, 74, 0.14), transparent 28rem),
                linear-gradient(135deg, #101725 0%, #172033 42%, #0d1320 100%);
            color: var(--z9-ivory) !important;
        }

        .block-container {
            max-width: 1060px;
            padding-top: 2.25rem;
            padding-bottom: 4rem;
        }

        section[data-testid="stSidebar"] {
            background: #0d1320;
            border-right: 1px solid var(--z9-line);
        }

        section[data-testid="stSidebar"] * {
            color: var(--z9-ivory) !important;
            opacity: 1 !important;
        }

        .z9-hero {
            border: 1px solid var(--z9-line);
            background: linear-gradient(135deg, rgba(251,247,239,0.98), rgba(241,231,205,0.96));
            color: var(--z9-ink) !important;
            padding: 2.1rem;
            border-radius: 10px;
            box-shadow: 0 22px 70px rgba(0,0,0,0.24);
            margin-bottom: 1.5rem;
        }

        .z9-hero,
        .z9-hero * {
            color: var(--z9-ink) !important;
            opacity: 1 !important;
        }

        .z9-eyebrow {
            color: #7a6225 !important;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .z9-hero h1 {
            margin: 0 0 0.75rem 0;
            font-size: clamp(2rem, 4vw, 3.8rem);
            line-height: 1;
        }

        .z9-hero p {
            max-width: 760px;
            font-size: 1.05rem;
            line-height: 1.65;
        }

        .z9-section {
            margin: 2rem 0 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid var(--z9-line);
        }

        .z9-section h2 {
            color: #d7b45a !important;
            font-size: 1.55rem;
            font-weight: 850;
            margin-bottom: 0.25rem;
            opacity: 1 !important;
        }

        .z9-section p {
            color: var(--z9-ivory) !important;
            margin-top: 0;
            opacity: 1 !important;
        }

        .z9-card,
        .z9-snapshot-item,
        .z9-meta-item {
            border: 1px solid rgba(201,162,74,0.34);
            background: var(--z9-card) !important;
            color: var(--z9-ink) !important;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.75rem 0;
            box-shadow: 0 14px 34px rgba(15,23,42,0.14);
            opacity: 1 !important;
        }

        .z9-card,
        .z9-card *,
        .z9-snapshot-item,
        .z9-snapshot-item *,
        .z9-meta-item,
        .z9-meta-item * {
            color: var(--z9-ink) !important;
            opacity: 1 !important;
        }

        .z9-card h3 {
            color: #111827 !important;
            margin-top: 0;
            margin-bottom: 0.4rem;
        }

        .z9-card p {
            color: var(--z9-ink) !important;
            line-height: 1.55;
            margin-bottom: 0;
        }

        .z9-snapshot-grid,
        .z9-metadata,
        .z9-cta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 0.85rem;
            margin: 1rem 0;
        }

        .z9-snapshot-label,
        .z9-meta-label {
            color: #7a6225 !important;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            font-weight: 900;
            margin-bottom: 0.35rem;
        }

        .z9-snapshot-value,
        .z9-meta-value {
            color: #111827 !important;
            font-size: 1.02rem;
            font-weight: 800;
            line-height: 1.35;
        }

        .z9-cta {
            display: block;
            text-decoration: none;
            color: #111827 !important;
            background: linear-gradient(135deg,#f2d98a,#c9a24a) !important;
            border: 1px solid rgba(255,255,255,0.38);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            font-weight: 800;
            text-align: center;
            box-shadow: 0 12px 26px rgba(0,0,0,0.2);
            opacity: 1 !important;
        }

        .z9-cta,
        .z9-cta * {
            color: #111827 !important;
            opacity: 1 !important;
        }

        div.stButton > button,
        div[data-testid="stDownloadButton"] button,
        div[data-testid="stLinkButton"] a {
            background: linear-gradient(135deg,#f2d98a,#c9a24a) !important;
            color: #111827 !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 800 !important;
            min-height: 2.8rem !important;
            box-shadow: 0 12px 26px rgba(0,0,0,0.2);
            opacity: 1 !important;
        }

        div.stButton > button *,
        div[data-testid="stDownloadButton"] button *,
        div[data-testid="stLinkButton"] a * {
            color: #111827 !important;
            opacity: 1 !important;
        }

        [data-testid="stFormSubmitButton"] button,
        [data-testid="stFormSubmitButton"] button * {
            color: #111827 !important;
            background: linear-gradient(135deg,#f2d98a,#c9a24a) !important;
            font-weight: 800 !important;
        }

        [data-testid="stForm"] {
            background: rgba(9,16,28,0.92) !important;
            border: 1px solid rgba(201,162,74,0.32) !important;
            border-radius: 14px !important;
            padding: 1.25rem !important;
            opacity: 1 !important;
        }

        [data-testid="stForm"] *,
        [data-testid="stRadio"] *,
        [data-baseweb="radio"] * {
            color: var(--z9-ivory) !important;
            opacity: 1 !important;
        }

        [data-testid="stForm"] h1,
        [data-testid="stForm"] h2,
        [data-testid="stForm"] h3 {
            color: var(--z9-gold-soft) !important;
            opacity: 1 !important;
        }

        [data-testid="stSelectbox"] *,
        [data-baseweb="select"] *,
        [data-testid="stSlider"] * {
            opacity: 1 !important;
        }

        section.main .block-container * {
            opacity: 1 !important;
        }
        </style>
        """
    )


def render_section(title: str, subtitle: str = "") -> None:
    subtitle_html = f"<p>{html.escape(subtitle)}</p>" if subtitle else ""
    _render_html(
        f"""
        <div class="z9-section">
            <h2>{html.escape(title)}</h2>
            {subtitle_html}
        </div>
        """
    )


def render_hero(
    title: str,
    body: str,
    eyebrow: str = "Z9CoachFree State Snapshot",
) -> None:
    _render_html(
        f"""
        <div class="z9-hero">
            <div class="z9-eyebrow">{html.escape(eyebrow)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(body)}</p>
        </div>
        """
    )


def render_metadata(items: Mapping[str, object]) -> None:
    blocks = []
    for label, value in items.items():
        blocks.append(
            f"""
            <div class="z9-meta-item">
                <div class="z9-meta-label">{html.escape(str(label))}</div>
                <div class="z9-meta-value">{html.escape(str(value))}</div>
            </div>
            """
        )

    _render_html(f"<div class=\"z9-metadata\">{''.join(blocks)}</div>")


def render_snapshot_grid(items: Mapping[str, object]) -> None:
    clean_items = {k: v for k, v in items.items() if v not in ("", None, "-")}

    if not clean_items:
        st.info("Complete the assessment to generate the Z9CoachFree State Snapshot.")
        return

    blocks = []
    for label, value in clean_items.items():
        blocks.append(
            f"""
            <div class="z9-snapshot-item">
                <div class="z9-snapshot-label">{html.escape(str(label))}</div>
                <div class="z9-snapshot-value">{html.escape(str(value))}</div>
            </div>
            """
        )

    _render_html(f"<div class=\"z9-snapshot-grid\">{''.join(blocks)}</div>")


def render_card(title: str, body: str) -> None:
    if not body:
        return

    _render_html(
        f"""
        <div class="z9-card">
            <h3>{html.escape(str(title))}</h3>
            <p>{html.escape(str(body))}</p>
        </div>
        """
    )


def render_narrative_cta(title: str, body: str, href: str, label: str) -> None:
    _render_html(
        f"""
        <div class="z9-card">
            <h3>{html.escape(str(title))}</h3>
            <p>{html.escape(str(body))}</p>
            <div class="z9-cta-grid">
                <a class="z9-cta" href="{html.escape(href, quote=True)}" target="_blank">
                    {html.escape(str(label))}
                </a>
            </div>
        </div>
        """
    )


def render_cta_grid(items: Iterable[Mapping[str, str]]) -> None:
    links = []
    for item in items:
        label = html.escape(item["label"])
        href = html.escape(item["href"], quote=True)
        variant = " secondary" if item.get("variant") == "secondary" else ""
        links.append(
            f'<a class="z9-cta{variant}" href="{href}" target="_blank">{label}</a>'
        )

    _render_html(f"<div class=\"z9-cta-grid\">{''.join(links)}</div>")

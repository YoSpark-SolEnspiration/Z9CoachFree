# File: style_helpers.py
# Title: Z9CoachFree Presentation Helpers

import html
from typing import Iterable, Mapping

import streamlit as st


def apply_z9_luxury_theme() -> None:
    st.markdown(
        """
        <style>
        :root {
            --z9-slate: #111827;
            --z9-navy: #172033;
            --z9-gold: #c9a24a;
            --z9-gold-soft: #ead99d;
            --z9-ivory: #fbf7ef;
            --z9-ink: #1d2433;
            --z9-muted: #5f6675;
            --z9-line: rgba(201, 162, 74, 0.28);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(201, 162, 74, 0.14), transparent 28rem),
                linear-gradient(135deg, #101725 0%, #172033 42%, #0d1320 100%);
            color: var(--z9-ivory);
        }

        section[data-testid="stSidebar"] {
            background: #0d1320;
            border-right: 1px solid var(--z9-line);
        }

        .block-container {
            max-width: 1060px;
            padding-top: 2.25rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            letter-spacing: 0;
        }

        .z9-hero {
            border: 1px solid var(--z9-line);
            background: linear-gradient(135deg, rgba(251,247,239,0.98), rgba(241,231,205,0.96));
            color: var(--z9-ink);
            padding: 2.1rem;
            border-radius: 8px;
            box-shadow: 0 22px 70px rgba(0,0,0,0.24);
            margin-bottom: 1.5rem;
        }

        .z9-eyebrow {
            color: #7a6225;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
        }

        .z9-hero h1 {
            margin: 0 0 0.75rem 0;
            color: var(--z9-ink);
            font-size: clamp(2rem, 4vw, 3.8rem);
            line-height: 1;
        }

        .z9-hero p {
            color: #384152;
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
            color: var(--z9-gold-soft);
            font-size: 1.55rem;
            margin-bottom: 0.25rem;
        }

        .z9-section p {
            color: #d7deea;
            margin-top: 0;
        }

        .z9-card {
            border: 1px solid rgba(201, 162, 74, 0.32);
            background: rgba(251,247,239,0.96);
            color: var(--z9-ink);
            border-radius: 8px;
            padding: 1.2rem;
            margin: 0.75rem 0;
            box-shadow: 0 14px 36px rgba(0,0,0,0.16);
        }

        .z9-card h3 {
            color: #141b2b;
            margin-top: 0;
        }

        .z9-card p,
        .z9-card li {
            color: #3f4858;
        }

        .z9-snapshot-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 0.75rem;
            margin: 1rem 0;
        }

        .z9-snapshot-item {
            border: 1px solid rgba(201,162,74,0.34);
            background: rgba(251,247,239,0.97);
            color: var(--z9-ink);
            border-radius: 8px;
            padding: 1rem;
        }

        .z9-snapshot-label {
            color: #7a6225;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            font-weight: 800;
            margin-bottom: 0.3rem;
        }

        .z9-snapshot-value {
            color: #182033;
            font-size: 1rem;
            font-weight: 700;
            line-height: 1.4;
        }

        .z9-metadata {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 0.65rem;
            margin: 1rem 0;
        }

        .z9-meta-item {
            border: 1px solid rgba(201,162,74,0.36);
            background: rgba(13,19,32,0.64);
            border-radius: 8px;
            padding: 0.9rem;
        }

        .z9-meta-label {
            color: #cfd7e6;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .z9-meta-value {
            color: var(--z9-gold-soft);
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 0.2rem;
        }

        .z9-cta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            gap: 0.85rem;
            margin-top: 1rem;
        }

        .z9-cta {
            display: block;
            text-decoration: none;
            color: #111827 !important;
            background: linear-gradient(135deg, #f7e8b0, #c9a24a);
            border: 1px solid rgba(255,255,255,0.38);
            border-radius: 8px;
            padding: 0.9rem 1rem;
            font-weight: 800;
            text-align: center;
            box-shadow: 0 12px 26px rgba(0,0,0,0.2);
        }

        .z9-cta.secondary {
            color: var(--z9-ivory) !important;
            background: rgba(17,24,39,0.82);
            border-color: var(--z9-line);
        }

        div.stButton > button,
        div[data-testid="stDownloadButton"] button {
            background: linear-gradient(135deg, #f7e8b0, #c9a24a);
            color: #111827;
            border: 0;
            border-radius: 8px;
            font-weight: 800;
            min-height: 2.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_section(title: str, subtitle: str = "") -> None:
    subtitle_html = f"<p>{html.escape(subtitle)}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="z9-section">
            <h2>{html.escape(title)}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(
    title: str,
    body: str,
    eyebrow: str = "Z9CoachFree State Snapshot",
) -> None:
    st.markdown(
        f"""
        <div class="z9-hero">
            <div class="z9-eyebrow">{html.escape(eyebrow)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metadata(items: Mapping[str, object]) -> None:
    blocks = []
    for label, value in items.items():
        blocks.append(
            f"""
            <div class="z9-meta-item">
                <div class="z9-meta-label">{html.escape(label)}</div>
                <div class="z9-meta-value">{html.escape(str(value))}</div>
            </div>
            """
        )

    st.markdown(
        f"<div class=\"z9-metadata\">{''.join(blocks)}</div>",
        unsafe_allow_html=True,
    )


def render_snapshot_grid(items: Mapping[str, object]) -> None:
    blocks = []
    for label, value in items.items():
        blocks.append(
            f"""
            <div class="z9-snapshot-item">
                <div class="z9-snapshot-label">{html.escape(label)}</div>
                <div class="z9-snapshot-value">{html.escape(str(value))}</div>
            </div>
            """
        )

    st.markdown(
        f"<div class=\"z9-snapshot-grid\">{''.join(blocks)}</div>",
        unsafe_allow_html=True,
    )


def render_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="z9-card">
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_narrative_cta(title: str, body: str, href: str, label: str) -> None:
    st.markdown(
        f"""
        <div class="z9-card">
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(body)}</p>
            <div class="z9-cta-grid">
                <a class="z9-cta" href="{html.escape(href, quote=True)}" target="_blank">
                    {html.escape(label)}
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
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

    st.markdown(
        f"<div class=\"z9-cta-grid\">{''.join(links)}</div>",
        unsafe_allow_html=True,
    )
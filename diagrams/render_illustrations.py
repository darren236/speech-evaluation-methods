#!/usr/bin/env python3
"""Render the README's small, self-contained SVG illustrations."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT = "Inter,Segoe UI,Arial,sans-serif"
INK = "#18304d"
MUTED = "#52647b"


def text(x, y, value, size=18, color=INK, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">{escape(value)}</text>'
    )


def rect(x, y, w, h, fill, radius=20, stroke="none", sw=1):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def icon(kind, cx, cy, color):
    parts = [f'<circle cx="{cx}" cy="{cy}" r="42" fill="{color}" opacity=".12"/>']
    if kind == "text":
        parts.extend([
            rect(cx - 23, cy - 24, 46, 48, "#ffffff", 6, color, 3),
            f'<path d="M {cx - 14} {cy - 10} H {cx + 14} M {cx - 14} {cy} H {cx + 8} '
            f'M {cx - 14} {cy + 10} H {cx + 12}" stroke="{color}" stroke-width="4" stroke-linecap="round"/>',
        ])
    elif kind == "people":
        parts.extend([
            f'<circle cx="{cx - 12}" cy="{cy - 9}" r="9" fill="none" stroke="{color}" stroke-width="4"/>',
            f'<circle cx="{cx + 15}" cy="{cy - 9}" r="9" fill="none" stroke="{color}" stroke-width="4"/>',
            f'<path d="M {cx - 29} {cy + 19} Q {cx - 12} {cy - 2} {cx + 4} {cy + 19} '
            f'M {cx - 1} {cy + 19} Q {cx + 15} {cy - 2} {cx + 31} {cy + 19}" '
            f'fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round"/>',
        ])
    elif kind == "clock":
        parts.extend([
            f'<circle cx="{cx}" cy="{cy}" r="26" fill="#ffffff" stroke="{color}" stroke-width="4"/>',
            f'<path d="M {cx} {cy - 16} V {cy} L {cx + 13} {cy + 8}" '
            f'fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
        ])
    else:
        parts.extend([
            f'<circle cx="{cx}" cy="{cy}" r="26" fill="#ffffff" stroke="{color}" stroke-width="4"/>',
            f'<path d="M {cx - 14} {cy} L {cx - 3} {cy + 11} L {cx + 17} {cy - 12}" '
            f'fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
        ])
    return "\n".join(parts)


def metric_lenses():
    cards = [
        ("TEXT", "What was said?", "WER · CER · entity recall", "Words, scripts, and critical names", "#2563eb", "text"),
        ("SPEAKERS", "Who said it?", "DER · cpWER · tcpWER", "Speaker turns and assigned words", "#0d9488", "people"),
        ("TIMING", "When was it ready?", "Endpoint · latency · RTF", "Live delay and offline speed", "#c26a16", "clock"),
        ("RESULT", "Did it work?", "Task success · error review", "User goals and failure patterns", "#7c3aed", "result"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="460" '
        'viewBox="0 0 1500 460" role="img" aria-labelledby="title desc">',
        '<title id="title">Four questions for speech evaluation</title>',
        '<desc id="desc">Transcript, speaker, timing, and outcome metrics answer different questions.</desc>',
        rect(0, 0, 1500, 460, "#f7f9fd", 0),
        text(50, 58, "One system, different questions", 34, INK, 750),
        text(50, 90, "Choose measures for the parts of the experience you need to judge.", 18, MUTED),
    ]
    for index, (tag, question, metrics, detail, color, symbol) in enumerate(cards):
        x = 50 + index * 365
        parts.extend([
            rect(x, 139, 340, 270, "#dce5f0", 24),
            rect(x, 135, 340, 270, "#ffffff", 24, "#e2e9f2", 2),
            rect(x, 135, 340, 9, color, 4),
            icon(symbol, x + 72, 206, color),
            text(x + 132, 187, tag, 16, color, 750),
            text(x + 132, 223, question, 23, INK, 700),
            f'<path d="M {x + 32} 270 H {x + 308}" stroke="#dce5f0" stroke-width="2"/>',
            text(x + 32, 310, metrics, 18, color, 700),
            text(x + 32, 344, detail, 17, MUTED),
        ])
    parts.append("</svg>")
    (ASSETS / "metric-lenses.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def evaluation_flow():
    steps = [
        ("1", "Match the data", "Use speech the product will hear.", "#2563eb"),
        ("2", "Freeze the rules", "Fix references and token policies.", "#0d9488"),
        ("3", "Score by condition", "Show counts, rates, uncertainty.", "#c26a16"),
        ("4", "Review failures", "Inspect names, turns, and cut-offs.", "#7c3aed"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="360" '
        'viewBox="0 0 1500 360" role="img" aria-labelledby="title desc">',
        '<title id="title">Four-step evaluation workflow</title>',
        '<desc id="desc">Match data, freeze scoring rules, score by condition, and review failures.</desc>',
        rect(0, 0, 1500, 360, "#f7f9fd", 0),
        text(50, 60, "From metric choice to a useful score", 34, INK, 750),
    ]
    for index, (number, heading, detail, color) in enumerate(steps):
        x = 50 + index * 365
        parts.extend([
            rect(x, 105, 340, 205, "#ffffff", 24, "#e2e9f2", 2),
            rect(x, 105, 340, 9, color, 4),
            f'<circle cx="{x + 64}" cy="164" r="32" fill="{color}"/>',
            text(x + 64, 174, number, 28, "#ffffff", 750, "middle"),
            text(x + 32, 235, heading, 23, INK, 700),
            text(x + 32, 271, detail, 17, MUTED),
        ])
        if index < 3:
            parts.append(
                f'<path d="M {x + 346} 207 H {x + 357} M {x + 352} 201 L {x + 358} 207 L {x + 352} 213" '
                f'fill="none" stroke="#71849d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            )
    parts.append("</svg>")
    (ASSETS / "evaluation-flow.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    metric_lenses()
    evaluation_flow()

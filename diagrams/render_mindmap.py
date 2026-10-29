#!/usr/bin/env python3
"""Render the README's self-contained speech-evaluation mind map."""

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "evaluation-map.svg"

INK = "#18304d"
MUTED = "#52647b"
FONT = "Inter,Segoe UI,Arial,sans-serif"

GROUPS = [
    {
        "title": "TRANSCRIPT ACCURACY",
        "subtitle": "What words or characters were produced?",
        "color": "#2563eb",
        "soft": "#eff6ff",
        "x": 70,
        "y": 150,
        "rows": [
            ("WER", "Standard for English words"),
            ("CER", "Common for Mandarin text"),
            ("Entity recall", "Names, places, amounts"),
            ("Mixed-unit", "Code-switched scripts"),
            ("MER / WIL", "Extra alignment views"),
        ],
    },
    {
        "title": "SPEAKERS",
        "subtitle": "Who spoke, and which words were theirs?",
        "color": "#0d9488",
        "soft": "#ecfdf9",
        "x": 70,
        "y": 475,
        "rows": [
            ("DER", "Speaker-time errors"),
            ("cpWER", "Words + speaker labels"),
            ("tcpWER", "Words + speaker + time"),
            ("Report", "Miss / false / confusion"),
        ],
    },
    {
        "title": "DETECTION & SPEED",
        "subtitle": "Was speech found and processed in time?",
        "color": "#c26a16",
        "soft": "#fff7ed",
        "x": 70,
        "y": 800,
        "rows": [
            ("Detection", "Miss + false-alarm rates"),
            ("Endpoint", "Delay + early cut-offs"),
            ("Streaming", "First / stable / final text"),
            ("RTF", "Offline processing speed"),
        ],
    },
    {
        "title": "TRANSLATION",
        "subtitle": "Was the meaning carried across?",
        "color": "#7c3aed",
        "soft": "#f5f3ff",
        "x": 1070,
        "y": 150,
        "rows": [
            ("BLEU", "Matching word sequences"),
            ("chrF", "Matching character spans"),
            ("COMET", "Model-based quality"),
            ("Human review", "Meaning + critical details"),
        ],
    },
    {
        "title": "AUDIO QUALITY",
        "subtitle": "How did the speech sound to listeners?",
        "color": "#db2777",
        "soft": "#fdf2f8",
        "x": 1070,
        "y": 475,
        "rows": [
            ("MOS", "Average listener rating"),
            ("Intelligibility", "Words listeners recover"),
            ("PESQ", "Telephone / codec quality"),
            ("Report", "Question + listening setup"),
        ],
    },
    {
        "title": "TASK OUTCOMES",
        "subtitle": "Did the user reach the intended goal?",
        "color": "#0284c7",
        "soft": "#f0f9ff",
        "x": 1070,
        "y": 800,
        "rows": [
            ("Task success", "Correct completion rate"),
            ("Repair", "Repeat or correction needed?"),
            ("Breakdown", "Failures by scenario"),
            ("Pair with", "WER + latency to explain"),
        ],
    },
]


def text(x, y, value, size=18, color=INK, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        f'font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
        f'fill="{color}">{escape(value)}</text>'
    )


def rect(x, y, w, h, fill, radius=20, stroke="none", sw=1):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def group_card(group):
    x, y, c = group["x"], group["y"], group["color"]
    parts = [
        rect(x, y + 5, 460, 280, "#dce5f0", 24),
        rect(x, y, 460, 280, "#ffffff", 24, "#e2e9f2", 2),
        rect(x, y, 10, 280, c, 5),
        rect(x + 28, y + 22, 402, 62, group["soft"], 14),
        text(x + 44, y + 49, group["title"], 24, c, 700),
        text(x + 44, y + 73, group["subtitle"], 15, MUTED),
    ]
    for index, (name, meaning) in enumerate(group["rows"]):
        baseline = y + 115 + 32 * index
        parts.extend([
            f'<circle cx="{x + 45}" cy="{baseline - 5}" r="4" fill="{c}"/>',
            text(x + 61, baseline, name, 17, INK, 700),
            text(x + 213, baseline, meaning, 16, MUTED),
        ])
    return "\n".join(parts)


def main():
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1250" '
        'viewBox="0 0 1600 1250" role="img" aria-labelledby="title desc">',
        '<title id="title">Speech evaluation metric mind map</title>',
        '<desc id="desc">Six branches cover transcript accuracy, speakers, detection and speed, '
        'translation, audio quality, and task outcomes. A footer lists evaluation rules.</desc>',
        rect(0, 0, 1600, 1250, "#f7f9fd", 0),
        f'<circle cx="805" cy="610" r="445" fill="#eef3fa"/>',
        text(800, 67, "Speech evaluation, by task", 42, INK, 750, "middle"),
        text(800, 104, "Start with one primary measure. Add metrics for failures that matter.", 20, MUTED, 400, "middle"),
    ]
    for group in GROUPS:
        left = group["x"] < 800
        start_x = 600 if left else 1000
        end_x = 530 if left else 1070
        start_y = 530 if group["y"] < 300 else 600 if group["y"] < 700 else 680
        end_y = group["y"] + 140
        bend = -35 if left else 35
        parts.append(
            f'<path d="M {start_x} {start_y} C {start_x + bend} {start_y}, '
            f'{end_x - bend} {end_y}, {end_x} {end_y}" '
            f'fill="none" stroke="{group["color"]}" stroke-width="5" stroke-linecap="round"/>'
        )
        parts.append(f'<circle cx="{end_x}" cy="{end_y}" r="6" fill="{group["color"]}"/>')
    for group in GROUPS:
        parts.append(group_card(group))
    parts.extend([
        rect(600, 455, 400, 295, "#d2dce9", 32),
        rect(600, 449, 400, 295, INK, 32),
        text(800, 511, "SPEECH", 35, "#ffffff", 750, "middle"),
        text(800, 553, "EVALUATION", 35, "#ffffff", 750, "middle"),
        f'<path d="M 670 583 H 930" stroke="#86a9d2" stroke-width="2"/>',
        text(800, 619, "Choose the task first", 22, "#dceaf8", 600, "middle"),
        text(800, 658, "Primary metric + failure check", 19, "#ffffff", 400, "middle"),
        text(800, 694, "Same data · same scoring rules", 19, "#ffffff", 400, "middle"),
        rect(70, 1120, 1460, 100, "#eaf0f8", 22),
        text(105, 1159, "STUDY RULES", 20, INK, 750),
    ])
    rules = [
        ("01", "Match the data"),
        ("02", "Freeze references + rules"),
        ("03", "Compare paired systems"),
        ("04", "Report by condition"),
    ]
    for index, (number, rule) in enumerate(rules):
        x = 300 + index * 300
        parts.extend([
            f'<circle cx="{x}" cy="1170" r="25" fill="{INK}"/>',
            text(x, 1177, number, 18, "#ffffff", 700, "middle"),
            text(x + 38, 1177, rule, 18, INK, 600),
        ])
    parts.append("</svg>")
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate the self-contained SVG mind map shown in the README."""

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "evaluation-map.svg"

GROUPS = [
    {
        "side": "left", "y": 190, "color": "#2563eb",
        "label": ["TEXT OUTPUT"],
        "leaves": ["WER and CER", "Names and particles", "Code-switch errors", "Edit counts"],
        "leaf_y": [75, 135, 195, 255],
    },
    {
        "side": "left", "y": 600, "color": "#078466",
        "label": ["SPEAKER AND TIME"],
        "leaves": ["Diarization error", "Speaker-attributed WER", "VAD and endpointing", "Streaming latency"],
        "leaf_y": [480, 540, 600, 660],
    },
    {
        "side": "right", "y": 190, "color": "#b45309",
        "label": ["USER OUTCOMES"],
        "leaves": ["Task completion", "Translation adequacy", "Listening tests", "Intelligibility"],
        "leaf_y": [75, 135, 195, 255],
    },
    {
        "side": "right", "y": 600, "color": "#7c3aed",
        "label": ["STUDY DESIGN"],
        "leaves": ["Dataset fit", "Reference policy", "Source overlap", "Paired uncertainty", "Per-condition scorecard"],
        "leaf_y": [470, 525, 580, 635, 690],
    },
]


def label(x: int, y: int, value: str, *, size: int = 19, color: str = "#263447",
          weight: int = 500, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
        'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{color}">'
        f'{escape(value)}</text>'
    )


def render_group(group: dict) -> str:
    left = group["side"] == "left"
    cy, color = group["y"], group["color"]
    cat_start, cat_end = (275, 490) if left else (790, 1005)
    attach = cat_end if left else cat_start
    root_edge = 510 if left else 770
    root_y = 380 if cy < 400 else 440
    dot_x = 250 if left else 1030
    text_x = 235 if left else 1045
    leaf_start = cat_start if left else cat_end
    parts = [
        f'<path d="M {root_edge} {root_y} C '
        f'{root_edge + (-70 if left else 70)} {root_y}, '
        f'{attach + (55 if left else -55)} {cy}, {attach} {cy}" '
        f'fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round"/>',
        f'<circle cx="{attach}" cy="{cy}" r="5" fill="{color}"/>',
    ]
    for leaf, y in zip(group["leaves"], group["leaf_y"]):
        parts.append(
            f'<path d="M {leaf_start} {cy} C '
            f'{leaf_start + (-20 if left else 20)} {cy}, '
            f'{dot_x + (20 if left else -20)} {y}, {dot_x} {y}" '
            f'fill="none" stroke="{color}" stroke-opacity=".72" '
            'stroke-width="2.5" stroke-linecap="round"/>'
        )
        parts.append(f'<circle cx="{dot_x}" cy="{y}" r="4.5" fill="{color}"/>')
        parts.append(label(text_x, y + 6, leaf, anchor="end" if left else "start"))
    parts.append(label(cat_start, cy - 17, group["label"][0], size=21, color=color, weight=700))
    parts.append(
        f'<path d="M {cat_start} {cy + 13} H {cat_end}" '
        f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
    )
    return "\n".join(parts)


def main() -> None:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="780" '
        'viewBox="0 0 1280 780" role="img" aria-labelledby="title desc">',
        '<title id="title">Speech evaluation methods mind map</title>',
        '<desc id="desc">Four branches categorize text output, speaker and timing, '
        'user outcomes, and evaluation study design.</desc>',
        '<rect width="1280" height="780" fill="#ffffff"/>',
    ]
    parts.extend(render_group(group) for group in GROUPS)
    parts.extend([
        '<rect x="510" y="350" width="260" height="120" rx="26" fill="#17324f"/>',
        label(640, 395, "SPEECH", size=26, color="#ffffff", weight=700, anchor="middle"),
        label(640, 429, "EVALUATION", size=26, color="#ffffff", weight=700, anchor="middle"),
        '</svg>',
    ])
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

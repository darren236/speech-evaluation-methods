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


def evidence_routes():
    cards = [
        ("HUMAN", "Listen or review", "A/B · MOS · adequacy", "Tone · pronunciation", "Listener judgments", "#db2777"),
        ("CALCULATED", "Compare references", "WER · CER · DER", "BLEU · PESQ", "Fixed labels or audio", "#2563eb"),
        ("MODEL-ASSISTED", "Run a pinned evaluator", "COMET · TTS ASR", "Speaker similarity", "Inspect model errors", "#7c3aed"),
        ("SERVICE / OUTCOME", "Read logs + pass rules", "First audio · RTF", "Task success", "Some need human labels", "#c26a16"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="740" '
        'viewBox="0 0 1500 740" role="img" aria-labelledby="title desc">',
        '<title id="title">Four sources of speech evaluation evidence</title>',
        '<desc id="desc">One test set branches to human judgments, calculated scores, model-assisted checks, '
        'and service or outcome measures. Each route has different requirements.</desc>',
        rect(0, 0, 1500, 740, "#f7f9fd", 0),
        text(50, 60, "How a result is obtained", 34, INK, 750),
        text(50, 93, "The same test set can support four kinds of evidence.", 19, MUTED),
        rect(550, 127, 400, 69, INK, 19),
        text(750, 171, "SAME TEST SET", 24, "#ffffff", 750, "middle"),
        '<path d="M 750 196 V 235 H 220 M 750 235 H 1315" fill="none" '
        'stroke="#9aabc0" stroke-width="4" stroke-linecap="round"/>',
    ]
    for index, (heading, action, metric_a, metric_b, need, color) in enumerate(cards):
        x = 50 + index * 365
        cx = x + 170
        parts.extend([
            f'<path d="M {cx} 235 V 274 M {cx - 7} 266 L {cx} 274 L {cx + 7} 266" '
            f'fill="none" stroke="{color}" stroke-width="4" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
            rect(x, 281, 340, 345, "#dce5f0", 24),
            rect(x, 276, 340, 345, "#ffffff", 24, "#e2e9f2", 2),
            rect(x, 276, 10, 345, color, 4),
            text(x + 31, 326, heading, 21, color, 750),
            f'<path d="M {x + 30} 354 H {x + 310}" stroke="#e2e9f2" stroke-width="2"/>',
            text(x + 31, 397, action, 22, INK, 700),
            text(x + 31, 447, metric_a, 19, MUTED),
            text(x + 31, 479, metric_b, 19, MUTED),
            rect(x + 27, 535, 286, 54, color, 13),
            text(cx, 569, need, 17, "#ffffff", 700, "middle"),
        ])
    parts.extend([
        text(750, 689, "A calculated score can still depend on labels made by people.", 19, MUTED, 500, "middle"),
        "</svg>",
    ])
    (ASSETS / "evidence-routes.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def tts_quality_routes():
    cards = [
        ("HUMAN LISTENING", "A/B preference · MOS", "Tone · pronunciation", "Intelligibility · voice match", "Needs listeners", "#db2777", "people"),
        ("MODEL CHECKS", "ASR WER / CER", "Speaker similarity", "Review model mistakes", "Needs audio + references", "#7c3aed", "text"),
        ("SERVICE MEASURES", "Time to first audio", "Generation failures", "Compare under the same load", "Needs timed requests", "#c26a16", "clock"),
    ]
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="760" '
        'viewBox="0 0 1500 760" role="img" aria-labelledby="title desc">',
        '<title id="title">Three routes for evaluating text-to-speech</title>',
        '<desc id="desc">Generate matching clips from the same text and target voice, then assess them '
        'with human listening, model-based checks, and service measurements. Report each result separately.</desc>',
        rect(0, 0, 1500, 760, "#f7f9fd", 0),
        text(50, 60, "TTS quality needs more than one score", 34, INK, 750),
        text(50, 92, "Use the same prompts and voice setup for every system.", 19, MUTED),
        rect(451, 130, 598, 80, INK, 20),
        text(750, 179, "TEXT + TARGET VOICE → GENERATED CLIPS", 22, "#ffffff", 750, "middle"),
        '<path d="M 750 210 V 252 H 255 M 750 252 H 1245" fill="none" '
        'stroke="#9aabc0" stroke-width="4" stroke-linecap="round"/>',
    ]
    for index, (heading, line_a, line_b, line_c, need, color, symbol) in enumerate(cards):
        x = 50 + index * 495
        cx = x + 205
        parts.extend([
            f'<path d="M {cx} 252 V 294 M {cx - 7} 286 L {cx} 294 L {cx + 7} 286" '
            f'fill="none" stroke="{color}" stroke-width="4" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
            rect(x, 304, 410, 312, "#dce5f0", 24),
            rect(x, 299, 410, 312, "#ffffff", 24, "#e2e9f2", 2),
            rect(x, 299, 10, 312, color, 4),
            text(x + 31, 351, heading, 23, color, 750),
            f'<path d="M {x + 30} 373 H {x + 380}" stroke="#e2e9f2" stroke-width="2"/>',
            icon(symbol, x + 77, 454, color),
            text(x + 137, 414, line_a, 18, INK, 700),
            text(x + 137, 448, line_b, 18, MUTED),
            text(x + 137, 482, line_c, 18, MUTED),
            rect(x + 27, 538, 356, 50, color, 13),
            text(cx, 571, need, 18, "#ffffff", 700, "middle"),
            f'<path d="M {cx} 616 V 652 M {cx - 7} 644 L {cx} 652 L {cx + 7} 644" '
            f'fill="none" stroke="{color}" stroke-width="4" '
            'stroke-linecap="round" stroke-linejoin="round"/>',
        ])
    parts.extend([
        rect(50, 667, 1400, 66, "#eaf0f8", 20),
        text(750, 708, "Choose for the target audience; report each result separately.", 22, INK, 700, "middle"),
        "</svg>",
    ])
    (ASSETS / "tts-quality-routes.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    metric_lenses()
    evaluation_flow()
    evidence_routes()
    tts_quality_routes()

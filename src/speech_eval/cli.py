"""Score two JSONL manifests by exact utterance ID."""

import argparse
import json
from pathlib import Path
import sys

from .scoring import Counts, POLICIES, score_pair


def read_manifest(path: Path, field: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
            if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]:
                raise ValueError(f"{path}:{line_number}: expected a nonempty string id")
            if not isinstance(row.get(field), str):
                raise ValueError(f"{path}:{line_number}: expected string {field}")
            if row["id"] in rows:
                raise ValueError(f"{path}:{line_number}: duplicate id {row['id']!r}")
            rows[row["id"]] = row
    if not rows:
        raise ValueError(f"{path}: no utterances")
    return rows


def score(reference_path: Path, hypothesis_path: Path, policy: str) -> dict:
    references = read_manifest(reference_path, "reference")
    hypotheses = read_manifest(hypothesis_path, "hypothesis")
    missing = sorted(references.keys() - hypotheses.keys())
    extra = sorted(hypotheses.keys() - references.keys())
    if missing or extra:
        raise ValueError(f"ID mismatch: {len(missing)} missing predictions {missing[:5]}; "
                         f"{len(extra)} unexpected predictions {extra[:5]}")

    total = {unit: Counts() for unit in ("word", "character")}
    groups: dict[str, dict[str, Counts]] = {}
    empty = {unit: 0 for unit in total}
    for utterance_id, row in references.items():
        group = row.get("group", "all")
        if not isinstance(group, str) or not group:
            raise ValueError(f"reference id {utterance_id!r}: group must be a nonempty string")
        bucket = groups.setdefault(group, {unit: Counts() for unit in total})
        for unit in total:
            counts = score_pair(row["reference"], hypotheses[utterance_id]["hypothesis"], unit, policy)
            total[unit] = total[unit] + counts
            bucket[unit] = bucket[unit] + counts
            empty[unit] += counts.reference_units == 0

    return {
        "schema_version": 1,
        "normalization": policy,
        "utterances": len(references),
        "empty_reference_utterances": empty,
        "overall": {unit: counts.as_dict() for unit, counts in total.items()},
        "groups": {name: {unit: counts.as_dict() for unit, counts in bucket.items()}
                   for name, bucket in sorted(groups.items())},
        "notes": [
            "Rates are corpus micro averages: total edit operations divided by total reference units.",
            "Character scoring removes whitespace; word scoring splits on whitespace.",
            "Empty-reference utterances contribute insertions but no denominator. A zero denominator yields null.",
            "Groups are descriptive strata and may not represent independent source recordings.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score paired ASR JSONL manifests")
    parser.add_argument("references", type=Path)
    parser.add_argument("hypotheses", type=Path)
    parser.add_argument("--normalization", choices=POLICIES, default="basic")
    parser.add_argument("--output", type=Path, help="write JSON report to a file")
    args = parser.parse_args(argv)
    try:
        report = score(args.references, args.hypotheses, args.normalization)
        payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.write_text(payload, encoding="utf-8")
        else:
            sys.stdout.write(payload)
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(2, f"speech-eval: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())

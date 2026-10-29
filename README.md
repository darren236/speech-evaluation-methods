# Speech evaluation methods

A practical guide to evaluating speech systems, with a small, auditable ASR scorer. The starting point is the companion [Singapore and Southeast Asian ASR dataset survey](https://github.com/darren236/singapore-asr-datasets). That survey found that transcript quality, recording independence, and speech style vary substantially across public datasets. A single pooled WER can hide those differences.

## Start here

| Question | Read | Measure |
| --- | --- | --- |
| How accurately are words transcribed? | [ASR metrics](docs/metrics.md) | WER with substitution, deletion, insertion counts |
| How does a mixed-script transcript score? | [ASR metrics](docs/metrics.md) | CER and a declared mixed-unit rule; report WER only where tokenization is meaningful |
| Does a gain generalize to Singapore speech? | [Evaluation protocol](docs/protocol.md) | Per-source, per-style scores and paired uncertainty |
| Are speakers assigned correctly? | [Other speech tasks](docs/other-tasks.md) | DER or speaker-attributed WER with a stated collar and overlap policy |
| Does a real product work well? | [Other speech tasks](docs/other-tasks.md) | Latency, endpointing, manual review, and task outcomes |

## Score a paired ASR manifest

Python 3.10+; the scorer has no runtime dependencies. Run it directly from the repo:

```bash
PYTHONPATH=src python3 -m speech_eval.cli examples/references.jsonl examples/hypotheses.jsonl --output report.json
```

If `pip` is available, `pip install -e .` also installs the `speech-eval` command.

Each reference line has `id`, `reference`, and optional `group`; each prediction line has the same `id` and `hypothesis`. IDs must match exactly. The scorer fails on missing, extra, or duplicate IDs. It reports corpus-level micro WER and CER, plus descriptive group breakdowns. `--normalization strict` scores the original text; the default `basic` policy applies Unicode NFKC, case folding, punctuation removal, and whitespace normalization. Neither policy deletes fillers or local particles such as `lah`, `ah`, or `liao`. Save the normalization policy alongside every score.

The executable intentionally does not claim to score diarization, mixed-unit error rate, semantic equivalence, or uncertainty. Those need task-specific alignment and annotation rules. See the guides before comparing model rankings.

## Evaluation checklist

1. Define the product task and the target population before selecting recordings.
2. Record dataset version, split, rights, reference provenance, speaker/recording IDs, and possible training overlap.
3. Freeze reference and prediction manifests, system version, decoding settings, normalization, and tokenization.
4. Check every prediction ID; never silently omit failed or missing outputs.
5. Report edit counts and corpus micro rates by dataset and speech condition. Keep pooled scores secondary.
6. Review errors on names, Singlish particles, switches, disfluencies, noise, and speaker turns.
7. For model comparisons, use paired recordings and resample by independent speaker or source recording where possible.

## Scope and references

This repo scores reference text against ASR hypotheses; it does not download or redistribute any audio or transcripts. Dataset examples and rights are documented in the [survey](https://github.com/darren236/singapore-asr-datasets). The scorer uses the familiar edit-distance WER/CER definitions also implemented by [JiWER](https://github.com/jitsi/jiwer). The protocol draws on [blockwise ASR bootstrap analysis](https://arxiv.org/abs/1912.09508) and [multilingual CER analysis](https://arxiv.org/abs/2410.07400). See each guide for task-specific sources.

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Contributions should include the metric definition, annotation and normalization policy, a worked example, and tests for any new executable metric.

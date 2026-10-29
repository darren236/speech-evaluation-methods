# Speech evaluation methods

A guide to choosing speech metrics, plus a small ASR scorer.
It builds on the [Singapore and Southeast Asian ASR dataset survey](https://github.com/darren236/singapore-asr-datasets).

Start with what you need to judge: words, speakers, timing, translation, audio quality, or task success.
Then choose a metric and a matching test set.

## Map

The map groups metrics by use. The included scorer implements **WER and CER**.

![Mind map grouping speech evaluation into text output, speaker and timing, user outcomes, and study design](assets/evaluation-map.svg)

## Metric picks

“Standard” means a common starting point **for that task**. It is not a ranking across tasks.
Lower is better for errors and latency. Higher is better for accuracy and quality.

| Task | Starting metric | What it tells you |
| --- | --- | --- |
| English ASR | **WER** · standard | Word errors in a transcript. |
| Mandarin or mixed-script ASR | **CER** · common companion | Character errors; add switch and name checks. |
| Speaker diarization | **DER** · standard | Missed speech, false alarms, and speaker mix-ups. |
| Multi-speaker transcript | **cpWER / tcpWER** · common | Word errors with speaker assignment; tcpWER also checks timing. |
| Speech detection | Miss and false-alarm rates · common | Speech missed or silence treated as speech. |
| Live voice system | WER + latency + task success | Accuracy, speed, and whether the task worked. |
| Offline processing | **RTF** · common | Processing time per second of audio. |
| Speech translation | **BLEU / chrF / COMET** + human review | Translation agreement and adequacy. |
| Speech synthesis or enhancement | Listening test, often **MOS** | Listener-rated quality under a stated question. |

Read the [ASR metrics](docs/metrics.md), [other speech tasks](docs/other-tasks.md),
and [evaluation protocol](docs/protocol.md) for definitions, limits, and examples.

## Example

Reference: `okay lah` · prediction: `okay`.

- Count `lah`: **1 error / 2 words = 50% WER**.
- Remove `lah` during normalization: **0% WER**.

Choose one policy that matches the product. Use it for every model.

## Run the scorer

Requires Python 3.10+ and no runtime packages.

```bash
PYTHONPATH=src python3 -m speech_eval.cli examples/references.jsonl examples/hypotheses.jsonl --output report.json
```

- Reference JSONL: `id`, `reference`, and optional `group`.
- Prediction JSONL: matching `id` values and `hypothesis`.
- Missing, extra, or duplicate IDs stop scoring.

The report gives corpus WER and CER, plus scores by group.
Rates are fractions: `0.20` means 20%.

The default `basic` policy folds case and Unicode form, removes punctuation, and normalizes spaces.
Use `--normalization strict` to keep the original text. Save the policy with each score.

The scorer covers **WER and CER only**. Other metrics in this guide are explained, not computed.
If `pip` is available, `pip install -e .` also adds the `speech-eval` command.

## Checklist

1. Match the test set to the speech your product will hear.
2. Record its version, references, rights, speakers, and possible training overlap.
3. Freeze model settings, manifests, normalization, and tokenization.
4. Score every ID. Report counts and rates by dataset and condition.
5. Review local names, particles, switches, noise, and speaker turns.
6. Compare systems on paired recordings; account for shared speakers and calls.

## Sources

The scorer uses synthetic examples. It does not download or redistribute source-dataset material.
Dataset rights and reference quality are in the [survey](https://github.com/darren236/singapore-asr-datasets).

Definitions draw on [JiWER](https://github.com/jitsi/jiwer),
[MeetEval](https://github.com/fgnt/meeteval),
[SacreBLEU](https://github.com/mjpost/sacreBLEU), and
[ITU-T P.800](https://www.itu.int/rec/T-REC-P.800-199608-I/en).
The guides link to sources for specific methods.

## Contribute

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

For a new metric, include its definition, text or annotation policy, worked example, and tests.

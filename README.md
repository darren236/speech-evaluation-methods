# Speech evaluation methods

A practical guide to choosing speech metrics, with a small, auditable ASR scorer. It builds on the companion [Singapore and Southeast Asian ASR dataset survey](https://github.com/darren236/singapore-asr-datasets). Start with the **output you need to judge**: transcript text, speaker turns, timing, translation, generated speech, or the success of a voice task. Then choose a metric and a matching test set.

## Evaluation map

Use this mind map to locate a measure by the output or decision you need to evaluate. The included scorer implements **WER and CER**; the other branches are method guides.

![Mind map grouping speech evaluation into text output, speaker and timing, user outcomes, and study design](assets/evaluation-map.svg)

## Which metric should I use?

“Default” below means a familiar starting measure **within that task**, not a popularity ranking across all speech research. Lower is better for error rates and latency; higher is better for recall, quality judgments, and task success.

| What are you judging? | Start with | How established? | Add when this matters | Main blind spot |
| --- | --- | --- | --- | --- |
| English ASR transcript | **WER** (word error rate) | Default ASR baseline | CER, edit counts, names/particle accuracy | A correct meaning can still have word errors; normalization changes the score. |
| Mandarin or mixed-script ASR | **CER** (character error rate), plus a declared token rule | Common multilingual companion | WER on suitable spans; switch and entity review | Characters and English words receive different effective weight. |
| Speaker diarization | **DER** (diarization error rate) | Default diarization baseline | Miss, false alarm, confusion breakdown | It does not say whether the words are correct. |
| Multi-speaker transcript | **cpWER** or **tcpWER** | Common meeting-transcription measures | DER and ordinary WER | Scores depend on speaker and timing rules. |
| Speech detection and endpointing | Miss/false-alarm rates and end-of-turn delay | Common task measures | Boundary review and latency percentiles | Detecting speech is different from transcribing it. |
| Streaming ASR or voice assistant | Final WER **and** latency/task success | Common product bundle, not one universal metric | Time to first/stable text, interruptions | Fast output may be wrong or unstable. |
| Offline ASR processing speed | **RTF** (real-time factor) | Common throughput measure | Hardware, batch size, end-to-end latency | Fast bulk processing need not feel fast to a live user. |
| Speech translation | Human adequacy plus **BLEU/chrF** or **COMET** | Common translation measures | Names, omissions, latency | A single reference cannot list every valid translation. |
| Generated or enhanced speech | Controlled listening test, often **MOS** | Established subjective method | Intelligibility and latency | Listener setup and question wording affect results. |

See the [ASR metric guide](docs/metrics.md) for definitions and worked examples, [other speech tasks](docs/other-tasks.md) for speaker, timing, translation, and audio-quality measures, and the [evaluation protocol](docs/protocol.md) for choosing data and reporting a comparison. For a voice product, report **task success alongside the technical measure** that explains failures.

## One example: why the metric policy matters

Reference: `okay lah` · prediction: `okay`. WER is **1 deletion / 2 reference words = 50%**. A normalizer that deletes `lah` makes the same prediction score **0%**. Both numbers may be internally consistent; the right policy depends on whether the product must retain local particles. The [ASR guide](docs/metrics.md) shows the formula and other edge cases.

## Score a paired ASR manifest

Python 3.10+; the scorer has no runtime dependencies. Run it directly from the repo:

```bash
PYTHONPATH=src python3 -m speech_eval.cli examples/references.jsonl examples/hypotheses.jsonl --output report.json
```

If `pip` is available, `pip install -e .` also installs the `speech-eval` command.

Each reference line has `id`, `reference`, and optional `group`; each prediction line has the same `id` and `hypothesis`. IDs must match exactly. The scorer fails on missing, extra, or duplicate IDs. It reports corpus-level micro WER and CER as fractions (`0.20` means 20%), plus descriptive group breakdowns. `--normalization strict` scores the original text; the default `basic` policy applies Unicode NFKC, case folding, punctuation removal, and whitespace normalization. Neither policy deletes fillers or local particles such as `lah`, `ah`, or `liao`. Save the normalization policy alongside every score.

The executable scores **WER and CER only**. It does not score diarization, mixed-unit error rate, translation, human quality, or uncertainty. Those need task-specific alignment and annotation rules. See the guides before comparing model rankings.

## Evaluation checklist

1. Define the product task and the target population before selecting recordings.
2. Record dataset version, split, rights, reference provenance, speaker/recording IDs, and possible training overlap.
3. Freeze reference and prediction manifests, system version, decoding settings, normalization, and tokenization.
4. Check every prediction ID; never silently omit failed or missing outputs.
5. Report edit counts and corpus micro rates by dataset and speech condition. Keep pooled scores secondary.
6. Review errors on names, Singlish particles, switches, disfluencies, noise, and speaker turns.
7. For model comparisons, use paired recordings and resample by independent speaker or source recording where possible.

## Scope and references

The code scores reference text against ASR hypotheses; it does not download or redistribute source-dataset audio or transcripts. Dataset examples and rights are documented in the [survey](https://github.com/darren236/singapore-asr-datasets). The descriptions of [ASR metrics](https://github.com/jitsi/jiwer), [diarization and meeting metrics](https://github.com/fgnt/meeteval), [translation metrics](https://github.com/mjpost/sacreBLEU), and [subjective speech quality](https://www.itu.int/rec/T-REC-P.800-199608-I/en) are grounded in their respective source projects or standards. See each guide for specific references and scoring conditions.

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Contributions should include the metric definition, annotation and normalization policy, a worked example, and tests for any new executable metric.

# Evaluation protocol

Choose data that matches the speech your system will hear.
Use the [Singapore ASR dataset survey](https://github.com/darren236/singapore-asr-datasets) to check access, references, and source overlap.

## Pick data

| Target speech | Candidate | Key limit |
| --- | --- | --- |
| Service calls | AppTek en-SG | Manual text; ten speakers in role-played calls. |
| Spontaneous Singlish | MNSC Part 3 or SASRBench | Both come from NSC Part 3. |
| Local names and places | MNSC Part 2; SG Streets | Prompted reading differs from conversation. |
| Code switching | MNSC Part 4 | Mixed scripts need a scoring rule. |
| Accented web video | GigaSpeechBench SGP-EN | Check audio-use rights. |
| Scripted accent coverage | Common Voice Singapore accent | Check speaker balance and release counts. |

Do not count derived sets as independent evidence.
A public manifest does not settle audio rights.

Machine transcripts, including some YCSEP text, are not independent human references.
Record possible pretraining overlap; “held out from our run” does not mean “unseen by the model.”

## Metric bundles

Use several measures when one score would hide a critical failure.

| Goal | Lead measure | Add |
| --- | --- | --- |
| Singapore English ASR | WER by source and speech style | CER; name and particle accuracy. |
| Mandarin–English switching | CER or declared mixed-unit rate | English-span WER; switch-region review. |
| Meeting transcript | cpWER or tcpWER | DER; ordinary WER. |
| Live voice assistant | Task completion | Final WER; cut-offs; delay percentiles. |

See [ASR metrics](metrics.md) and [other speech tasks](other-tasks.md) for definitions.
Use the [metric examples](examples.md) to check how each score answers a different question.

## Freeze the setup

Keep two records:

- **Data manifest:** clip and source-recording IDs, speaker ID if known, dataset version and split,
  language, duration, reference source, rights note, and reference text.
- **Run record:** model version, prompt, decoding settings, endpointing, channel handling,
  sample-rate conversion, run date, and prediction text by ID.

Hash both manifests. Mark unavailable fields as `unknown`; do not infer them from an accent.
Decide the scoring unit: utterance, channel, or whole recording.

Set rules for overlap, crosstalk, disfluencies, partial words, particles, and non-speech text.
Freeze normalization and tokenization before looking at model results.

## Compare models

Score the **same recordings** against the **same references** with the **same policy**.
Record failed and missing predictions. State how they affect the score; never drop IDs silently.

Report S, D, I, N, WER, and CER by source and condition.
Also report clips, speakers, and independent source recordings.

Compare paired systems by resampling whole speakers or source recordings when possible.
Clip-level resampling can understate uncertainty when clips share a call or speaker.
State the resampling unit, draws, seed, and confidence interval method.
See [blockwise bootstrap work](https://arxiv.org/abs/1912.09508) and
[research on dependent utterances](https://arxiv.org/abs/2209.05281).

## Publish a scorecard

Include the dataset and split, reference quality, source overlap, model settings,
normalizer, token rule, counts, rates, uncertainty, failed runs, and a short error review.
Show per-condition results before a pooled number.
Do not publish restricted recordings or transcripts.

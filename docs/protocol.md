# Evaluation protocol for Singapore and regional ASR

The [dataset survey](https://github.com/darren236/singapore-asr-datasets) is the evidence inventory. Choose data for the speech the system will encounter, then document a protocol before running models.

## Select complementary tests

| Target behavior | Candidate data | Interpretation |
| --- | --- | --- |
| Service conversations | AppTek en-SG | Manual references, but ten speakers and role-played calls. |
| Spontaneous Singlish | MNSC Part 3 or SASRBench | Both derive from NSC Part 3; do not treat them as independent validations. |
| Singapore names and places | MNSC Part 2; SG Streets for street names | Prompted reading differs from spontaneous use. |
| Code-switched conversation | MNSC Part 4 | Define the scoring of mixed scripts and language switches. |
| Accented web video | GigaSpeechBench SGP-EN | Verify audio-use rights before use. |
| Scripted accent coverage | Common Voice Singapore accent | Speaker balance and release-specific test counts matter. |

The survey records access and licence caveats. The presence of a public manifest is not proof that its audio can be mirrored. Machine-generated reference text, such as some YCSEP podcast text, should not be treated as independent human ground truth. Note if a test source may have appeared in pretraining or fine-tuning; “held out from our training run” is narrower than “unseen by the model.”

## Freeze an evaluation record

Keep a manifest with utterance ID, source recording ID, speaker ID where available, dataset release and split, language/script, speech style, duration, environment, reference provenance, rights note, and reference text. Store prediction text under the same IDs. Keep model version, prompt, decoding parameters, endpointing, channel handling, sample-rate conversion, and run date in a separate run record. Hash the manifests. If metadata is unavailable, write “unknown” rather than inferring it from accents or filenames.

Decide whether scoring is utterance based, channel based, or whole recording based. Paired call channels and overlapping snippets are not independent examples. State how overlap, crosstalk, disfluencies, partial words, bracketed particles, non-speech events, and unintelligible spans are treated. Set rules before seeing system results.

## Compare systems fairly

Score the *same recordings* with the *same references and normalizer*. Include all IDs, including failed inference. Report S/D/I and denominator as well as WER and CER for each dataset and condition. Report the number of speakers and source recordings, not just clips. Avoid declaring a winner from a pooled score if it masks a serious regression on local names or code switching.

For uncertainty, resample paired systems together at the level of an independent source recording or speaker. If utterances share a call or speaker, utterance-level bootstrap samples understate dependence. State the resampling unit, number of draws, seed, and confidence interval method. [Blockwise bootstrap research](https://arxiv.org/abs/1912.09508) and [work on dependent utterances](https://arxiv.org/abs/2209.05281) explain this concern. For small strata, show raw per-recording results and avoid overstating significance.

## Release a scorecard

Publish a scorecard with dataset/release, evaluation unit, reference quality, source-family overlap, number of clips/recordings/speakers, normalization, tokenization, model settings, S/D/I/N, WER/CER, uncertainty, failure count, rights limitations, and a concise error review. Do not publish restricted source material or private recordings in the scorecard.

# ASR text metrics

## Choose a text metric

| Metric | Standing in ASR | Best question | Watch out for |
| --- | --- | --- | --- |
| **WER** — word error rate | Default baseline for word-based ASR | How many reference words changed, vanished, or appeared? | Word boundaries and normalization change the answer. |
| **CER** — character error rate | Common companion for multilingual or character-script ASR | How different are the character sequences? | A name error and a particle error of the same length count equally. |
| **Sentence/utterance error rate** | Useful diagnostic for short commands | What fraction of utterances contain any text error? | Sensitive to utterance length; does not show error size. |
| **Named-entity exact match/recall** | Task-specific diagnostic | Were names, addresses, brands, and amounts preserved? | Needs entity spans and an alias policy. |
| **Mixed-unit error rate** | Task-specific code-switching choice | How do Han characters and English words score together? | Different token rules can change rankings. |
| **MER / WIL** — match error rate / word information lost | Established alternatives, less usual as a headline than WER | Does an insertion-heavy system need another view? | Define the formula; `MER` also means *mixed* error rate in some work. |

The [JiWER implementation](https://github.com/jitsi/jiwer/blob/master/src/jiwer/process.py) provides definitions for WER, CER, match error rate, and word information measures. This repo's CLI implements **WER and CER only**; the other rows describe evaluation options.

## WER and CER

For a reference sequence with **N** units, word error rate (WER) or character error rate (CER) is **(S + D + I) / N**. S, D, and I are substitutions, deletions, and insertions under a minimum-edit-distance alignment. WER units here are whitespace-delimited words; CER units are Unicode code points after whitespace removal. The repo's CER is *not* grapheme-cluster CER. Report the counts as well as the rate. Rates can exceed 100% when insertions are numerous. A reference with zero units has an undefined rate, represented as `null`.

**Worked example:** reference `meet at Bedok`, prediction `meet Bedok now`. `at` is deleted and `now` is inserted: S = 0, D = 1, I = 1, N = 3, so WER = **2/3 = 66.7%**. This measures text agreement, not whether a listener understood the destination.

The scorer sums edit counts and reference units over utterances before dividing (corpus micro averaging). A mean of utterance WERs answers a different question and gives short utterances disproportionate weight. An empty-reference utterance can have insertions; those are retained in the corpus total. The scorer's alignment tie rule prefers substitution, then deletion, then insertion. A different tie rule can change the S/D/I breakdown while preserving total edit distance.

The scorer uses `null` when a rate has a zero denominator. [JiWER uses a different convention for an entirely empty corpus](https://github.com/jitsi/jiwer#readme). Include separate non-speech clips when hallucination or false speech is a product risk.

## Text policy changes the result

Run both strict and basic scoring when orthography matters. Strict means no text changes before tokenization. Basic applies Unicode NFKC, case folding, removes punctuation characters, and collapses whitespace. It leaves lexical items intact. For example, `[ah]` becomes `ah`, while an omitted `ah` is still a deletion. Basic removes apostrophes inside words (`don't` → `dont`). It does not equate spelling variants, transliterations, numbers, translations, or synonyms.

These rules are illustrative, not a universal benchmark standard. Publish any custom mapping table and apply the same transformation to reference and hypothesis. Preserve raw transcripts for audit. Compare models under the same frozen policy. In the [AppTek en-SG release](https://huggingface.co/datasets/apptek-com/apptek_callcenter_dialogues), the provided normalizer removes `lah` and `ah`; this repo deliberately retains them because such particles may matter to a Singapore English task.

For example, reference `okay lah` and prediction `okay` give **50% WER** here. Deleting `lah` during normalization would make the same prediction score **0%**. Decide which policy reflects the product before seeing model results.

## Code switching and mixed scripts

Whitespace WER is often misleading for Mandarin without word segmentation. CER avoids one segmentation choice but treats each character equally and can obscure English word errors. A **mixed-unit error rate** can tokenize Han text into characters and English text into words, then apply the same edit formula. That is a *protocol choice*: publish the exact script detector, treatment of numerals and borrowed words, romanization, punctuation, and boundary rules. Do not call it simply “MER” without defining it: [JiWER](https://github.com/jitsi/jiwer) uses MER for **match error rate**, a different metric.

For MNSC Part 4 and similar material, report at least script-aware strata and hand-inspected switch errors. A switch-boundary slice should define what counts as a switch and use independently annotated language spans. Aggregate WER alone can hide switch-specific failures; [switch-aware ASR work](https://arxiv.org/abs/2609.11786) shows why this matters in another language pair.

## Additional diagnostics

| Diagnostic | Use | Caveat |
| --- | --- | --- |
| Named-entity recall / exact match | Addresses, places, people, brands | Requires a separate entity annotation and alias policy. |
| Deletion rate | Missed words and particles | Use edit counts and the same reference denominator. |
| Hallucination / insertion review | Speech-free or low-quality spans | Define non-speech regions; WER alone does not identify hallucination. |
| Sentence exact match | Fully correct short commands | Very sensitive to transcription policy and length. |
| Semantic task success | Whether a voice workflow completes | Human or task-specific labels; cannot replace transcription metrics. |

**Sentence error rate** is the fraction of utterances with at least one text error under the declared normalizer. It is helpful for short exact commands, but longer utterances have more opportunities for an error. **Match error rate (MER)** uses `(S + D + I) / (H + S + D + I)`, where H is aligned correct words; **word information lost (WIL)** is another alignment-derived alternative. Both are implemented in [JiWER](https://github.com/jitsi/jiwer/blob/master/src/jiwer/process.py). Neither replaces a task-specific check of critical words.

Do not compare rates from different datasets, scripts, segmentation schemes, or normalizers as though they shared a scale. [JiWER](https://github.com/jitsi/jiwer) documents the standard edit-distance family; [multilingual ASR analysis](https://arxiv.org/abs/2410.07400) discusses WER's limits across languages.

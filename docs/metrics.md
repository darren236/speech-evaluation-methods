# ASR metrics

## At a glance

| Metric | Use | Role |
| --- | --- | --- |
| **WER** · word error rate | Word-based ASR | Standard baseline. |
| **CER** · character error rate | Character scripts and multilingual ASR | Common companion. |
| **Sentence error rate** | Short, exact commands | Diagnostic; sensitive to utterance length. |
| **Entity recall** | Names, addresses, brands, amounts | Task-specific; needs annotated entities. |
| **Mixed-unit error rate** | Code-switched text | Task-specific; publish token rules. |
| **MER / WIL** | Alternative views of word alignment | Less common headline measures. |

The CLI implements **WER and CER only**.
[JiWER](https://github.com/jitsi/jiwer/blob/master/src/jiwer/process.py) defines the related match and information measures.
See [worked examples](examples.md#transcript-text) for every metric in the table.

## Edit rates

For WER and CER, **error rate = (S + D + I) / N**.

- **S**: substitutions; **D**: deletions; **I**: insertions.
- **N**: units in the reference. WER uses words; CER uses characters.
- Lower is better. Insertions can push a rate above 100%.

This scorer splits words on whitespace.
Its CER removes whitespace and counts Unicode code points, not grapheme clusters.
Report S, D, I, and N with the rate.

**Example:** reference `meet at Bedok`; prediction `meet Bedok`.

The scorer deletes `at`.
S = 0, D = 1, I = 0, N = 3, so WER = **1/3 = 33.3%**.

The scorer adds counts across utterances, then divides. This is a corpus micro average.
A mean of utterance rates gives short clips more weight.

An empty reference can still have insertions.
If N is zero, the rate is `null`; insertions remain in the corpus total.

For equal-cost alignments, the scorer prefers substitution, then deletion, then insertion.
Another scorer may split S/D/I differently while keeping the same total.

[JiWER uses another convention for an entirely empty corpus](https://github.com/jitsi/jiwer#readme).
Include non-speech clips when false speech is a product risk.

## Normalization

The `strict` policy leaves text unchanged before tokenization.
The `basic` policy applies Unicode NFKC, case folding, punctuation removal, and space cleanup.
It keeps lexical items: `[ah]` becomes `ah`, and a missing `ah` remains an error.
It turns `don't` into `dont`.

It does not merge synonyms, spellings, numbers, translations, or romanizations.

These are repo policies, not universal benchmark rules.
Apply one frozen policy to both reference and prediction, and keep raw text for audit.
Publish any custom mapping table.

With reference `okay lah` and prediction `okay`, this repo gives **50% WER**.
Deleting `lah` in a normalizer would give **0%**.

The [AppTek en-SG normalizer](https://huggingface.co/datasets/apptek-com/apptek_callcenter_dialogues) removes `lah` and `ah`.
Decide whether those particles matter before scoring.

## Code switching

Whitespace WER treats an unsegmented Mandarin phrase as one word.
CER avoids that segmentation choice but gives English words several character units.

A **mixed-unit rate** can score Han characters and English words in one sequence.
Publish the token rule, including numbers, borrowed words, romanization, and switch boundaries.

Define the acronym: [JiWER](https://github.com/jitsi/jiwer) uses **MER** for *match error rate*.

For MNSC Part 4, report script-level results and inspect errors near switches.
Define a switch with separately annotated language spans.
An aggregate rate can hide switch errors, as [switch-aware work](https://arxiv.org/abs/2609.11786) shows.

## Diagnostics

- **Entity recall:** check names and addresses against labeled spans and alias rules.
- **Insertions/deletions:** reveal added or missed words and local particles.
- **Sentence error rate:** share of utterances with any text error after normalization.
- **Task success:** whether a voice workflow completes; needs task-specific labels.

Long utterances have more chances for a sentence error.

**Match error rate (MER)** is `(S + D + I) / (H + S + D + I)`, where H is correct words.
**Word information lost (WIL)** is another alignment measure.
[JiWER](https://github.com/jitsi/jiwer/blob/master/src/jiwer/process.py) implements both.

Compare scores only under the same data, script, tokenization, and normalizer.
[Multilingual ASR analysis](https://arxiv.org/abs/2410.07400) explains WER's limits across languages.

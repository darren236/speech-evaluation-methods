# Metric examples

These are small, invented cases for learning the metrics. They are not benchmark results.
The repo's CLI computes **WER and CER only**. Other scores need the stated labels or a specialist tool.

## Transcript text

### WER · word error rate

Reference: `meet at Bedok`; prediction: `meet Bedok`.
One deletion (`at`) over three reference words gives **1/3 = 33.3% WER**.

### CER · character error rate

Reference: `Bedok`; prediction: `Bedo`.
One deleted character over five reference characters gives **1/5 = 20% CER**.

### Sentence error rate

Suppose `open notes` is exact, while `call Mei` becomes `call Ray`.
One of two utterances has an error: **1/2 = 50%**.
This hides whether the wrong utterance had one bad word or many.

### Entity recall

The reference names `Bedok`, `Mei`, and `$20` as three required entities.
If the system gets `Bedok` and `$20` right, recall is **2/3 = 66.7%**.
The evaluator must define aliases and what counts as an exact match.

### Mixed-unit error rate

Reference: `我去 Bedok`; prediction: `我到 Bedok`.
With Han characters and English words as units, the reference is `我 | 去 | Bedok`.
One substitution gives **1/3 = 33.3%** under *this* rule.

Whitespace WER gives **1/2 = 50%**; CER gives **1/7 = 14.3%**.
These rates have different denominators. Publish the token rule before comparing systems.

### Match error rate · MER

Reference: `hello`; prediction: `hello now again`.
There is one correct word (H = 1) and two insertions (I = 2).
WER is **2/1 = 200%**. Match error rate is **2/(1 + 2) = 66.7%**.
Here MER means *match* error rate, not mixed-unit error rate.

### Word information lost · WIL

Use the same `hello` example: H = 1, reference words = 1, prediction words = 3.
WIL is **1 − (1/1 × 1/3) = 66.7%** under [JiWER's definition](https://github.com/jitsi/jiwer/blob/master/src/jiwer/process.py).

### Edit counts

Reference `okay lah` → prediction `okay`: one deletion.
Reference `okay` → prediction `okay lah`: one insertion.
Both are one error, but the error type points to different failures.

## Speakers and timing

### DER · diarization error rate

Assume 10 seconds of reference speaker time.
The system misses 1 second, adds 1 second of false speech, and assigns 1 second to the wrong speaker.
For these non-overlapping regions, **DER = (1 + 1 + 1) / 10 = 30%**.
Boundary collars and overlap rules can change the result.

### cpWER · speaker-attributed words

Reference: Alice says `turn left`; Bob says `stop`.
Prediction: speaker 1 says `turn left`; speaker 2 says `start`.
After matching the arbitrary speaker labels, one of three words is wrong: **33.3% cpWER**.

### tcpWER · words and timing

Imagine the same words and speakers are correct, but `stop` appears 20 seconds late.
cpWER can still be **0%** because it does not enforce time proximity.
tcpWER may count an error if the delay exceeds its configured time tolerance.
The exact score needs [MeetEval's timing rules](https://github.com/fgnt/meeteval/blob/main/doc/tcpwer.md).

### Speech detection

In 10 seconds of speech and 10 seconds of silence, the detector misses 2 speech seconds.
It also labels 1 silence second as speech.
With speech and silence time as separate denominators: **20% miss**, **10% false alarm**.
Always state the denominators and boundary tolerance.

### Endpoint delay

The speaker finishes at 2.0 seconds; the system finalizes at 2.6 seconds.
End-of-turn delay is **0.6 seconds**.
A decision at 1.8 seconds might cut the speaker off and needs a separate cut-off count.

### Streaming latency

Audio starts at time 0; first text appears at 0.7 seconds, stable text at 1.8,
and final text at 3.0. Report **0.7 s**, **1.8 s**, and **3.0 s** separately.
Define “stable” and the clock origin before measuring.

### RTF · real-time factor

A 10-second clip takes 2 seconds to process: **RTF = 2/10 = 0.2**.
This measures throughput under that hardware and batch setup, not live response delay.

## Translation

### BLEU

Reference: `The train is arriving soon`.
An identical output has strong token overlap; `A train is coming shortly` may keep the meaning
while sharing fewer words. BLEU depends on its tokenizer and corpus settings.
Use [SacreBLEU](https://github.com/mjpost/sacreBLEU) to report those settings.

### chrF

Reference `Bedok` and output `Bedo` share many characters despite the missing `k`.
chrF measures character n-gram overlap; its exact score needs configured n-gram settings.
It does not establish whether the place name is usable.

### COMET

Source: `左转`; reference: `Turn left`; output: `Turn right`.
Run a pinned, reference-based [COMET model](https://github.com/Unbabel/COMET) with source, reference, and output.
Do not infer a numeric score by hand; also inspect this meaning reversal directly.

### Human adequacy

For the same `左转` example, a reviewer should mark `Turn right` as incorrect.
Record the rubric and agreement between reviewers.

## Audio and outcomes

### MOS · mean opinion score

Five listeners rate naturalness **4, 4, 3, 5, 4** on a 1–5 scale.
The mean is **4.0/5** for that question and listener group.
Report the question, conditions, and uncertainty; see [ITU-T P.800](https://www.itu.int/rec/T-REC-P.800-199608-I/en).

### Intelligibility

Listeners correctly repeat 90 of 100 target words: **90% word intelligibility**
under that listening test. This is distinct from a naturalness rating.

### PESQ

Compare a clean reference recording with its narrow-band, codec-degraded version.
Run a conforming [PESQ implementation](https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=5374);
the audio is needed for a score. Do not use it as a universal TTS naturalness measure.

### Task success

An assistant completes 17 of 20 booking requests correctly and without repair.
Under that pass rule, **task success = 17/20 = 85%**.
Report failures by scenario; WER and latency can help explain them.

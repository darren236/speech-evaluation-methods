# Other speech tasks

Choose a metric for the output you need to judge.
The repo's CLI scores **WER and CER only**; the methods below need other tools or labels.
See [worked examples](examples.md#speakers-and-timing) for each measure.

## Speakers

**DER · diarization error rate** is the standard starting point for speaker diarization.
It combines missed speech, false alarms, and wrong-speaker time.
Divide by reference speaker time. Lower is better.

DER measures *time*, not word accuracy.
State the scored region, boundary collar, overlap rule, and error breakdown.
[pyannote.metrics](https://github.com/pyannote/pyannote-metrics/blob/develop/doc/source/basics.rst) documents these settings.

**cpWER** scores words *and* speaker assignment in a meeting transcript.
It matches speaker labels before scoring, but can miss implausible timing.
**tcpWER** adds a time constraint.

Use [MeetEval](https://github.com/fgnt/meeteval) for the protocol.
Its [tcpWER guide](https://github.com/fgnt/meeteval/blob/main/doc/tcpwer.md) explains the time rule.

## Detection and speed

For **voice activity detection**, report missed-speech and false-alarm rates over labeled time.
For **endpointing**, also report cut-off frequency and delay after the true end of a turn.
A late endpoint makes an accurate assistant feel slow.

See [pyannote's metric paper](https://github.com/pyannote/pyannote-metrics-paper/blob/master/paper.tex)
and [endpointing research](https://arxiv.org/abs/2505.17070).

For **streaming ASR**, pair final WER with time to first, stable, and final text.
Record the clock origin, device, network, chunk size, and revision policy.

**RTF · real-time factor** is processing time divided by audio duration.
RTF below 1 means processing is faster than playback under the tested setup.
It helps estimate offline capacity; it does not capture user-visible queue or endpoint delay.
[NVIDIA's benchmark](https://github.com/NVIDIA/DeepLearningExamples/blob/master/Kaldi/SpeechRecognition/README.md) separates throughput and latency.

## Translation

Common automatic measures are **BLEU** (token overlap), **chrF** (character overlap),
and **COMET** (a learned quality score). Higher is better under a fixed version.

[SacreBLEU](https://github.com/mjpost/sacreBLEU) records metric settings;
[COMET](https://github.com/Unbabel/COMET) documents model-specific scores.

Valid translations can use different words.
Add human adequacy review for meaning, names, negation, and numbers.
[IWSLT analysis](https://arxiv.org/abs/2406.03881) compares automatic scores with human judgments.

## Audio quality

**MOS · mean opinion score** summarizes listener ratings.
State the question: naturalness, listening quality, or another property.
Also state the listener pool, scale, playback setup, and confidence interval.

[ITU-T P.800](https://www.itu.int/rec/T-REC-P.800-199608-I/en) covers listening tests;
[P.800.1](https://www.itu.int/itu-t/recommendations/rec.aspx?lang=en&rec=12972) clarifies MOS terms.

Objective scores have narrower uses.
For example, [PESQ](https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=5374) targets narrow-band telephone and codec quality.
It is not a universal naturalness score for generated speech.

## Task success

For a voice assistant, define success as a user outcome.
Example: “book the correct appointment without repair.”
Report completion and failure by scenario, then use WER and latency to explain failures.

For any human study, blind system identity when practical and randomize sample order.
Use an annotation rubric and report disagreement between reviewers.

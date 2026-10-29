# Beyond ASR text accuracy

Speech products need measures that match their actual outputs. **Default** below means a standard starting point *for that task*. “Common” does not mean scores from different tasks can be compared. These are method notes; this repository does not implement these scorers.

| Task | Common starting point | What it answers | Specify before comparing systems |
| --- | --- | --- | --- |
| Speaker diarization | **DER** — diarization error rate | How much speaker time is missed, falsely detected, or assigned to the wrong speaker? | Scored time region, boundary collar, overlap inclusion, speaker matching. [pyannote.metrics](https://github.com/pyannote/pyannote-metrics) provides implementations. |
| Speaker-attributed ASR | **cpWER**; **tcpWER** when timing matters | Are words assigned to the right speaker as well as transcribed? | Speaker-label permutation, concatenation, overlap, and time tolerance. [MeetEval](https://github.com/fgnt/meeteval) documents these measures. |
| Speech detection / endpointing | Miss and false-alarm rates; end-of-turn delay | Does the system catch speech and stop at the right time? | Reference speech regions, boundary tolerance, silence definition, latency percentiles. |
| Streaming ASR | Final WER plus latency | Is the final text accurate and delivered promptly? | Clock origin, time to first/stable/final text, chunk size, network and device. |
| Offline ASR efficiency | **RTF** — real-time factor | How many seconds of compute are needed per second of audio? | Hardware, batching, concurrency, I/O, and whether model load is included. |
| Speech translation | Human adequacy plus **BLEU/chrF** or **COMET** | Is meaning preserved in the target language? | Reference quality, target language, names, segmentation, metric version. |
| Speech synthesis / enhancement | Controlled listening test, often reported as **MOS** | Is the speech intelligible and natural or pleasant to hear? | Listener sample, question, scale, randomization, playback, conditions. |
| Voice assistant or workflow | Task completion and failure rate | Did the user accomplish the intended action? | Task definition, acceptable outcomes, human review, operating conditions. |

## Speaker and timing metrics

**DER** adds missed speech, false alarm, and speaker confusion, then divides by reference speaker time. Lower is better. A DER of 20% does not mean 20% of words are wrong: it measures time assigned to speakers. The score depends on the evaluation region, collar around annotated boundaries, and treatment of simultaneous speech. Report those settings and the error components. [pyannote.metrics](https://github.com/pyannote/pyannote-metrics/blob/develop/doc/source/basics.rst) documents the components and evaluation map.

**cpWER** (concatenated minimum-permutation WER) evaluates speaker-attributed text while allowing arbitrary speaker labels to be matched. It can overlook implausible timing when words are right but far from their proper turns. **tcpWER** adds a time constraint. Use both text and timing evidence for meetings; [MeetEval](https://github.com/fgnt/meeteval) and its [tcpWER guide](https://github.com/fgnt/meeteval/blob/main/doc/tcpwer.md) describe the distinction. Ordinary WER ignores speaker assignment.

For voice activity detection, measure missed speech and false alarms over labeled time regions. Endpointing also needs the delay from the *true end of a turn* to the system's final decision and the rate of cutting users off. A system can have good speech detection yet feel slow because its endpoint is late. [pyannote's metric paper](https://github.com/pyannote/pyannote-metrics-paper/blob/master/paper.tex) describes detection error, precision, and recall; [endpointing research](https://arxiv.org/abs/2505.17070) discusses the interruption/latency tradeoff.

**Real-time factor (RTF)** is processing time divided by audio duration. RTF below 1 means one worker processes audio faster than its duration under the stated setup. It is useful for offline capacity planning, but live response time also includes buffering, endpointing, network, and queue delay. [NVIDIA's Kaldi benchmark](https://github.com/NVIDIA/DeepLearningExamples/blob/master/Kaldi/SpeechRecognition/README.md) distinguishes throughput from client latency. Report both when the system serves users interactively.

## Translation, generated speech, and products

For speech translation, **BLEU** measures token-sequence overlap, **chrF** uses character n-gram overlap, and **COMET** is a learned translation-quality score. Higher is better under a fixed metric and version. [SacreBLEU](https://github.com/mjpost/sacreBLEU) records tokenization and metric signatures; [COMET](https://github.com/Unbabel/COMET) documents model-specific interpretation. These are common *automatic* measures, but valid paraphrases and speech segmentation can change the score. Pair them with human adequacy review, especially for names, negation, numbers, and code switching. [IWSLT speech-translation analysis](https://arxiv.org/abs/2406.03881) compares automatic measures with human judgments.

For speech synthesis and enhancement, a **mean opinion score (MOS)** summarizes a controlled listener rating, not an intrinsic property of an audio file. State whether people rated naturalness, listening quality, intelligibility, or something else. [ITU-T P.800](https://www.itu.int/rec/T-REC-P.800-199608-I/en) covers subjective methods and [P.800.1](https://www.itu.int/itu-t/recommendations/rec.aspx?lang=en&rec=12972) distinguishes MOS terminology. Objective scores such as PESQ have application limits; the [PESQ recommendation](https://www.itu.int/ITU-T/recommendations/rec.aspx?rec=5374) concerns narrow-band telephone and codec quality, so do not treat it as a universal naturalness score for generated speech.

For a voice assistant, define a task such as “book the correct appointment without repair” and measure completion and failure by scenario. Keep WER, endpoint delay, and latency as diagnostic measures. A low WER cannot prove that a booking, search, or navigation action was correct.

For human evaluation, blind the system identity when practical, randomize sample order, define an annotation rubric, and report inter-annotator disagreement. Keep the human sample stratified by the conditions that matter to the application. A metric should answer a product question; improving a text score does not by itself establish a better voice experience.

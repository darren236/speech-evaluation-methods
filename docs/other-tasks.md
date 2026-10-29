# Beyond ASR text accuracy

Speech products need measures that match their actual outputs. These are method notes; this repository does not implement these scorers.

| Task | Starting metric | Specify before comparing systems |
| --- | --- | --- |
| Speaker diarization | Diarization error rate (DER): missed speech + false alarm + speaker confusion, divided by reference speaker time | Scored time region, boundary collar, overlap inclusion, speaker matching. [pyannote.metrics](https://github.com/pyannote/pyannote-metrics) provides reproducible implementations. |
| Speaker-attributed ASR | Speaker-attributed WER such as cpWER | How words are concatenated by speaker, speaker-label permutation, overlap handling, and whether timing matters. [MeetEval](https://github.com/fgnt/meeteval) documents meeting transcription metrics. |
| Voice activity / endpointing | Miss, false alarm, and endpoint delay | Region labels, tolerance, overlap, silence definition, latency percentiles. |
| Streaming ASR | Final WER plus time to first text, time to stable text, and finalization latency | Clock origin, audio duration, chunk size, network conditions, device, and revision policy. |
| Speech translation | Human adequacy/meaning judgments plus a declared automatic text metric | Reference quality, target language, named entities, and how multiple valid translations are handled. |
| Speech synthesis | Listening tests for intelligibility and naturalness, plus latency | Listener sample, scale wording, randomization, playback equipment, and voice consent. |

For human evaluation, blind the system identity when practical, randomize sample order, define an annotation rubric, and report inter-annotator disagreement. Keep the human sample stratified by the conditions that matter to the application. A metric should answer a product question; improving a text score is not automatically a better voice experience.

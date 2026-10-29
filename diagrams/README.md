# Diagram sources

The README uses five self-contained SVGs. They need no external fonts or image files.

```bash
python3 diagrams/render_mindmap.py
python3 diagrams/render_illustrations.py
```

Edit `GROUPS` in `render_mindmap.py` to update the six metric branches.
The second script renders the metric-lens, evaluation-flow, evidence-route, and TTS-quality illustrations.
Regenerate the SVGs after changing either source.

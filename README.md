# Homebase Studio (Streamlit)

**Drag-and-drop into your GitHub repo**, then:

```bash
pip install -r requirements.txt
streamlit run my_project/app.py
```

Highlights:
- Multipage: home + YouTube agent (`my_project/pages/01_YouTube_Agent.py`)
- Robust imports: avoids `tiktoken`, `scipy`, and `moviepy` to prevent build failures on Streamlit Cloud (uses `imageio-ffmpeg`).
- Video preview with audio (tone fallback), download buttons, script download, pre-run cost estimate & stored actual cost.
- Review flow (approve/reject) using JSON storage under `my_project/data/outputs/`.
- Quality dials with clear explanations. Script generator fills definitions, examples, counter‑examples, and action steps.

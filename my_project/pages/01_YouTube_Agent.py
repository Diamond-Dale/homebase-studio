from __future__ import annotations
import sys
from pathlib import Path
_CUR = Path(__file__).resolve()
_GRAND = _CUR.parents[2]  # repo root
if str(_GRAND) not in sys.path:
    sys.path.insert(0, str(_GRAND))

import os, time, json, pandas as pd, streamlit as st
from my_project.config import PRICING_PER_1K, FIELDS, DEFAULT_IMAGE_SIZE
from my_project.agents.youtube_agent import run_video
from my_project.utils.storage import save_run, update_status, list_runs, search_runs
from my_project.utils.tokenize import estimate_tokens_from_words
from my_project.quality.script_generator import quality_explain

st.set_page_config(page_title="YouTube Agent", page_icon="🎬", layout="wide")
st.title("🎬 YouTube Agent")

tab_create, tab_history, tab_review, tab_search = st.tabs(["Create","History","Review","Search"])

def cost_estimate(words: int, model: str):
    toks = estimate_tokens_from_words(words)
    pricing = PRICING_PER_1K.get(model, PRICING_PER_1K["fallback"])
    tin = int(toks*0.6)
    tout = toks - tin
    est = (tin/1000.0)*pricing["input"] + (tout/1000.0)*pricing["output"]
    return toks, round(est, 4)

with tab_create:
    st.subheader("Create")
    col1, col2, col3 = st.columns(3)

    with col1:
        field = st.selectbox("Field", list(FIELDS.keys()), index=0)
        niches = list(FIELDS[field]["niches"].keys())
        niche = st.selectbox("Niche", niches, index=0)

    with col2:
        quality = st.radio("Quality", ["Fast","Balanced","Deep"], index=1, horizontal=True)
        words = st.slider("Target Script Length (words)", min_value=150, max_value=2400, step=50, value=700)
        images_per_run = st.slider("Images per run", min_value=3, max_value=20, step=1, value=8)

    with col3:
        model = st.selectbox("Model", ["gpt-5","gpt-5-mini","fallback"], index=2)
        st.caption(quality_explain(quality))

        toks, est = cost_estimate(words, model)
        st.metric("Estimated tokens", toks)
        st.metric("Estimated cost ($)", est)

    if st.button("Generate video", type="primary"):
        with st.spinner("Generating script, images, audio, and video..."):
            cfg = {"field": field, "niche": niche, "quality": quality, "model": model}
            run_id = f"{int(time.time())}"
            out_root = str(Path(__file__).resolve().parents[1] / "data" / "outputs" / run_id)
            res = run_video(cfg, out_root, words, quality, images_per_run, DEFAULT_IMAGE_SIZE, model)
            meta = {
                "id": run_id,
                "field": field, "niche": niche, "quality": quality, "model": model,
                "script": res["script"],
                "video_path": res["video"],
                "audio_path": res["audio"],
                "est_cost": est,
                "actual_cost": est,
                "status": "pending",
                "created_ts": int(time.time()),
            }
            save_run(meta)
            st.success("Run completed.")
            st.video(res["video"])
            st.download_button("Download video", data=open(res["video"],"rb").read(), file_name="video.mp4")
            st.download_button("Download script (.txt)", data=res["script"], file_name="script.txt")

with tab_history:
    st.subheader("History")
    items = list_runs()
    if not items:
        st.info("No runs yet.")
    else:
        for r in items[:50]:
            with st.expander(f"{r['id']} — {r['field']} / {r['niche']} — {r.get('status','?')}"):
                st.write(f"Model: {r.get('model')} | Quality: {r.get('quality')}")
                st.write(f"Est. Cost: ${r.get('est_cost',0)} | Actual Cost: ${r.get('actual_cost',0)}")
                if os.path.exists(r.get("video_path","")):
                    st.video(r["video_path"])
                    with open(r["video_path"],"rb") as f:
                        st.download_button("Download video", data=f.read(), file_name=f"{r['id']}.mp4", key=f"dlv{r['id']}")
                st.text_area("Script", r.get("script",""), height=200)

with tab_review:
    st.subheader("Review")
    pending = [r for r in list_runs() if r.get("status")=="pending"]
    if not pending:
        st.info("No items pending review.")
    else:
        for r in pending[:50]:
            cols = st.columns([3,1,1])
            with cols[0]:
                st.write(f"**{r['field']} / {r['niche']}** — {r['id']}")
                st.caption(f"Model: {r.get('model')} | Quality: {r.get('quality')}")
            if cols[1].button("Approve", key=f"ap{r['id']}"):
                update_status(r['id'], "approved")
                st.rerun()
            if cols[2].button("Reject", key=f"rj{r['id']}"):
                update_status(r['id'], "rejected")
                st.rerun()

with tab_search:
    st.subheader("Search")
    q = st.text_input("Search text")
    if q:
        hits = search_runs(q)
        st.write(f"Found {len(hits)} result(s).")
        for r in hits[:50]:
            st.write(f"- {r['id']} — {r['field']} / {r['niche']} — {r.get('status','?')}")

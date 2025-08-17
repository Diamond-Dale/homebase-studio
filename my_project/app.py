from __future__ import annotations
import sys
from pathlib import Path
_CUR = Path(__file__).resolve()
if str(_CUR.parent.parent) not in sys.path:
    sys.path.insert(0, str(_CUR.parent.parent))

import streamlit as st
from my_project.utils.storage import aggregate

st.set_page_config(page_title="Homebase Studio", page_icon="🧭", layout="wide")
st.title("Homebase Studio")

runs, totals = aggregate()

colA, colB, colC, colD = st.columns(4)
colA.metric("Total runs", totals["count"])
colB.metric("Approved", totals["approved"])
colC.metric("Pending", totals["pending"])
colD.metric("Rejected", totals["rejected"])

col1, col2 = st.columns(2)
with col1:
    st.metric("Estimated total cost ($)", totals["est_cost"])
with col2:
    st.metric("Actual total cost ($)", totals["actual_cost"])

st.markdown("### Agents")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎬 YouTube Agent", key="nav_yt"):
        st.switch_page("pages/01_YouTube_Agent.py")
with c2:
    st.button("📰 Newsletter Agent (coming soon)", disabled=True)
with c3:
    st.button("📚 Course Agent (coming soon)", disabled=True)

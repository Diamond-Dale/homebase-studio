from __future__ import annotations
import random, re
from typing import Dict, List
from ..config import FIELDS

def _clean_repeats(lines: List[str]) -> List[str]:
    seen = set()
    out = []
    for ln in lines:
        key = re.sub(r"\W+"," ", ln.lower()).strip()
        if key and key not in seen:
            out.append(ln)
            seen.add(key)
    return out

def _expand_concept(c) -> List[str]:
    return [
        f"Core idea — {c['term']}: {c['definition']}",
        f"Concrete example: {c['example']}",
        f"Counter‑example or edge case: {c['counter']}",
        "In practice: what to do → " + {
            "Escape Velocity": "Stack thrust in stages, optimize mass ratio, and use gravity assists when feasible.",
            "Redshift": "Use spectral lines (e.g., H‑alpha) to estimate z, then convert to distance with a cosmology model.",
            "Dark Matter": "Combine rotation curves, weak lensing maps, and CMB data to constrain halo profiles.",
            "Dollar-Cost Averaging": "Automate monthly buys; keep allocation steady unless life changes require a rebalance.",
            "Emergency Fund": "Hold 3–6 months expenses in high-liquidity accounts; ladder T‑bills for surplus cash.",
            "Tax-Advantaged Accounts": "Max employer match, then Roth/Traditional based on bracket; avoid high-fee funds."
        }.get(c["term"], "Apply the principle step‑by‑step in your workflow.")
    ]

def _knowledge_pack(field: str, niche: str) -> List[Dict]:
    return FIELDS.get(field,{}).get("niches",{}).get(niche,{}).get("concepts", [])

def generate_script(field: str, niche: str, quality: str, target_words: int, seed: int=None) -> str:
    rng = random.Random(seed or random.randint(1,10_000_000))
    concepts = _knowledge_pack(field, niche) or [{"term":"Key Idea","definition":"a well‑established principle relevant to this niche.","example":"A clear, real‑world scenario that illustrates it.","counter":"Where it breaks or needs nuance."}]
    rng.shuffle(concepts)

    lines = []
    lines.append(f"Hook: Why {niche} matters for {field.lower()} and what you’ll take away.")
    for c in concepts:
        lines += _expand_concept(c)

    ql = quality.lower()
    if ql == "deep":
        lines.append("Quality emphasis: include a counter‑example for every major claim and point to a measurement or proxy.")
    elif ql == "balanced":
        lines.append("Quality emphasis: give a crisp definition and one strong example per concept.")
    else:
        lines.append("Quality emphasis: concise, high‑signal steps only.")

    lines.append("Summary in one sentence: Turn the concepts into one practical action you can take today.")

    lines = _clean_repeats([ln.strip() for ln in lines if ln.strip()])

    detail_pool = []
    for c in concepts:
        detail_pool += [
            f"Measurement: define a baseline metric to track ({c['term']} context).",
            f"Pitfall to avoid: a common misread when applying {c['term']}."
        ]
    def word_count(txt: str) -> int: return len(txt.split())
    text = "\n".join(lines)
    while word_count(text) < int(target_words*0.9) and detail_pool:
        lines.append(rng.choice(detail_pool))
        text = "\n".join(lines)
    # Cap ~110%
    words = text.split()
    cap = int(target_words*1.1)
    if len(words) > cap:
        text = " ".join(words[:cap])
    return text

def quality_explain(q: str) -> str:
    q = q.lower()
    if q == "deep":
        return "Deep adds: counter‑examples, measurement steps, and nuance checks for each section. Expect more lines and denser facts."
    if q == "balanced":
        return "Balanced adds: a clear definition + one strong example per concept, with brief caveats."
    return "Fast adds: brief, actionable bullets only — minimal storytelling, maximum throughput."

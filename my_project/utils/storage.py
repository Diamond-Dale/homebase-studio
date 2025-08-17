from __future__ import annotations
import json, uuid, time
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1] / "data" / "outputs"
ROOT.mkdir(parents=True, exist_ok=True)

def _run_path(run_id: str) -> Path:
    return ROOT / f"{run_id}.json"

def save_run(meta: Dict) -> str:
    run_id = meta.get("id") or uuid.uuid4().hex[:10]
    meta["id"] = run_id
    meta["created_ts"] = meta.get("created_ts") or int(time.time())
    meta["status"] = meta.get("status") or "pending"
    (_run_path(run_id)).write_text(json.dumps(meta, indent=2))
    return run_id

def update_status(run_id: str, status: str) -> None:
    p = _run_path(run_id)
    if not p.exists(): return
    data = json.loads(p.read_text())
    data["status"] = status
    p.write_text(json.dumps(data, indent=2))

def list_runs(status: Optional[str]=None) -> List[Dict]:
    items = []
    for p in ROOT.glob("*.json"):
        try:
            data = json.loads(p.read_text())
            if status and data.get("status") != status: 
                continue
            items.append(data)
        except Exception:
            continue
    items.sort(key=lambda d: d.get("created_ts", 0), reverse=True)
    return items

def aggregate():
    runs = list_runs()
    totals = {
        "count": len(runs),
        "approved": sum(1 for r in runs if r.get("status")=="approved"),
        "rejected": sum(1 for r in runs if r.get("status")=="rejected"),
        "pending": sum(1 for r in runs if r.get("status")=="pending"),
        "est_cost": round(sum(r.get("est_cost", 0.0) for r in runs), 4),
        "actual_cost": round(sum(r.get("actual_cost", 0.0) for r in runs), 4),
    }
    return runs, totals

def search_runs(q: str) -> List[Dict]:
    ql = q.lower().strip()
    out = []
    for r in list_runs():
        hay = " ".join([r.get("field",""), r.get("niche",""), r.get("script","")]).lower()
        if ql in hay: out.append(r)
    return out

from __future__ import annotations
from typing import Dict, Tuple
from pathlib import Path
import time

from ..quality.script_generator import generate_script
from ..utils.audio import tts_to_wav
from ..utils.video import render_frames, make_video
from ..utils.tokenize import estimate_tokens_from_text
from ..config import DEFAULT_IMAGE_SIZE

def run_video(cfg: Dict, out_root: str, length_words: int, quality: str, images_per_run: int, image_size: Tuple[int,int], model_used: str) -> Dict:
    outdir = Path(out_root)
    outdir.mkdir(parents=True, exist_ok=True)

    script = generate_script(cfg["field"], cfg["niche"], quality, length_words, seed=int(time.time())%100000)

    # Audio (always produce something)
    wav_path = str(outdir / "audio.wav")
    tts_to_wav(script, wav_path)

    # Frames
    frames_dir = outdir / "frames"
    frames = render_frames(script, image_size or DEFAULT_IMAGE_SIZE, images_per_run, frames_dir)

    # Video
    mp4_path = str(outdir / "video.mp4")
    make_video(frames, Path(wav_path), Path(mp4_path))

    # Token/cost estimate
    tokens = estimate_tokens_from_text(script)

    return {"script": script, "audio": wav_path, "video": mp4_path, "tokens": tokens}

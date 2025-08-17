from __future__ import annotations
import os, math, subprocess
from typing import List, Tuple
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FONT = None

def _load_font(size: int=40):
    global FONT
    if FONT is None:
        try:
            FONT = ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            FONT = ImageFont.load_default()
    return FONT

def wrap_text(draw, text, max_width, font):
    lines = []
    words = text.split()
    while words:
        line = words.pop(0)
        while words and draw.textlength(line + " " + words[0], font=font) <= max_width:
            line += " " + words.pop(0)
        lines.append(line)
    return lines

def render_frames(script: str, size: Tuple[int,int], images_per_run: int, out_dir: Path) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    W,H = size
    font_title = _load_font(56)
    font_body = _load_font(36)

    sentences = [s.strip() for s in script.split("\n") if s.strip()]
    chunks = max(1, images_per_run)
    per = max(1, math.ceil(len(sentences)/chunks))
    slides = [sentences[i:i+per] for i in range(0, len(sentences), per)]
    slides = slides[:chunks]

    paths = []
    for idx, lines in enumerate(slides, start=1):
        img = Image.new("RGB",(W,H),(14,16,20))
        d = ImageDraw.Draw(img)
        title = lines[0][:120]
        body = "\n".join(lines[1:])

        y = 60
        title_lines = wrap_text(d, title, W-160, font_title)
        for tl in title_lines:
            d.text((80,y), tl, font=font_title, fill=(240,240,255))
            y += 68
        y += 20

        body_lines = []
        for bl in body.split("\n"):
            body_lines.extend(wrap_text(d, bl, W-160, font_body))
        for bl in body_lines[:18]:
            d.text((80,y), bl, font=font_body, fill=(210,210,220))
            y += 48

        p = out_dir / f"frame_{idx:03d}.png"
        img.save(p)
        paths.append(p)
    return paths

def _run(cmd: list):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {p.stderr.decode('utf-8','ignore')[:4000]}")

def make_video(frames: List[Path], audio_wav: Path, out_mp4: Path, fps: int=24) -> Path:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    temp_video = out_mp4.with_name(out_mp4.stem + "_silent.mp4")

    # concat demuxer file
    concat_file = out_mp4.with_name(out_mp4.stem + "_concat.txt")
    with open(concat_file, "w") as f:
        for frame in frames:
            f.write(f"file '{frame.as_posix()}'\n")
            f.write("duration 2.5\n")
        f.write(f"file '{frames[-1].as_posix()}'\n")

    _run([ffmpeg, "-y",
          "-f","concat","-safe","0","-i", concat_file.as_posix(),
          "-vf","scale=1280:720,format=yuv420p",
          "-r", str(fps),
          temp_video.as_posix()])

    _run([ffmpeg, "-y",
          "-i", temp_video.as_posix(),
          "-i", audio_wav.as_posix(),
          "-c:v","copy","-c:a","aac","-shortest",
          out_mp4.as_posix()])
    return out_mp4

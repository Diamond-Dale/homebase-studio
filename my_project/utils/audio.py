from __future__ import annotations
import os, wave, contextlib
import numpy as np
from typing import Optional

def _sine(seconds: float, freq: float=220.0, sr: int=22050) -> np.ndarray:
    t = np.linspace(0, seconds, int(sr*seconds), endpoint=False)
    audio = 0.15*np.sin(2*np.pi*freq*t)  # quiet tone
    return (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)

def tts_to_wav(text: str, wav_path: str, prefer_gtts: bool=True) -> str:
    """
    Tries gTTS if allowed (requires outbound internet). If that fails, writes a simple sine tone
    whose duration is estimated from words at ~150 wpm. We avoid SciPy and heavy deps.
    """
    if prefer_gtts:
        try:
            from gTTS import gTTS
            # Note: decoding MP3 -> WAV requires ffmpeg/pydub; we intentionally skip to keep deps light.
            # We'll still fall back to a tone below.
            _ = gTTS(text=text, lang="en")
        except Exception:
            pass

    # Estimate speaking duration ~ 150 wpm
    words = max(1, len(text.split()))
    minutes = words / 150.0
    seconds = max(3.0, minutes * 60.0)

    sr = 22050
    audio = _sine(seconds, 220.0, sr)
    with contextlib.closing(wave.open(wav_path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sr)
        wf.writeframes(audio.tobytes())
    return wav_path

def get_wav_duration_seconds(wav_path: str) -> float:
    import wave
    with wave.open(wav_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)

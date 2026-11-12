"""Recorta los silencios largos de la voz a MAX_GAP segundos (sin acelerar la voz).
Uso: python3 scripts/tighten.py voz-raw.wav voz.wav"""
import re, subprocess, sys
import numpy as np, soundfile as sf

import os
MAX_GAP = float(os.environ.get("MAX_GAP", "0.25"))
src, dst = sys.argv[1], sys.argv[2]
log = subprocess.run(["ffmpeg", "-i", src, "-af", "silencedetect=noise=-35dB:d=0.26", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
audio, sr = sf.read(src)
keep, cur = [], 0
for s, e in zip(starts, ends):
    if s < 0.05 or e > len(audio) / sr - 0.05:
        continue  # deja intactos el principio y el final
    half = MAX_GAP / 2
    keep.append(audio[cur:int((s + half) * sr)])
    cur = int((e - half) * sr)
keep.append(audio[cur:])
out = np.concatenate(keep)
sf.write(dst, out, sr)
print(f"{len(audio)/sr:.2f}s -> {len(out)/sr:.2f}s")

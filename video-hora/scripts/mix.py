"""Mezcla voz + efectos (assets/sfx-cues.json) + música baja y normaliza a -14 LUFS.
Uso: python3 scripts/mix.py   ->  assets/mezcla.wav"""
import json, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
cues = json.load(open("assets/sfx-cues.json"))
DUR = cues["duration"]

# nombre -> (archivo, inicio, duración máx)
SFX = {
    "whoosh": ("assets/sfx/whoosh.mp3", 0.0, 1.1),
    "whoosh-corto": ("assets/sfx/whoosh-corto.mp3", 0.0, 0.8),
    "pop": ("assets/sfx/pop.mp3", 0.0, 0.42),
    "pop2": ("assets/sfx/pop2.mp3", 0.0, 0.34),
    "golpe": ("assets/sfx/golpe.mp3", 0.0, 0.9),
    "golpe-climax": ("assets/sfx/golpe-climax.mp3", 0.0, 2.6),
    "puerta": ("assets/sfx/puerta.mp3", 0.0, 1.2),
    "papel": ("assets/sfx/papel.mp3", 0.0, 1.0),
    "paginas": ("assets/sfx/paginas.mp3", 0.3, 0.9),
    "madera": ("assets/sfx/madera.mp3", 0.0, 0.44),
    "check": ("assets/sfx/check.mp3", 0.0, 0.29),
    "click": ("assets/sfx/click.mp3", 0.0, 0.35),
    "teclado-tic": ("assets/sfx/teclado.mp3", 1.02, 0.12),
    "tic-rodillo": ("assets/sfx/teclado.mp3", 3.0, 0.5),
}
MUSIC = "assets/music/m1005.mp3"
MUSIC_VOL = 0.07

inputs = ["-i", "voz.wav", "-stream_loop", "-1", "-i", MUSIC]
filters = [
    "[0:a]aresample=48000,aformat=channel_layouts=stereo,volume=1.0[v]",
    f"[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{DUR:.3f},volume={MUSIC_VOL},"
    f"afade=t=in:d=0.6,afade=t=out:st={DUR - 1.2:.3f}:d=1.2[m]",
]
labels = ["[v]", "[m]"]
for i, c in enumerate(cues["cues"]):
    f, ss, d = SFX[c["file"]]
    inputs += ["-ss", f"{ss}", "-t", f"{d}", "-i", f]
    k = i + 2
    ms = int(c["t"] * 1000)
    filters.append(f"[{k}:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st={max(0, d - 0.12):.3f}:d=0.12,"
                   f"volume={c['vol']},adelay={ms}|{ms}[s{i}]")
    labels.append(f"[s{i}]")
filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,atrim=0:{DUR:.3f}[pre]")
graph = ";".join(filters)
open("assets/.mix-graph.txt", "w").write(graph)

subprocess.run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[pre]", "-ar", "48000",
                "assets/.premix.wav"], check=True)
# loudnorm en dos pasadas
r = subprocess.run(["ffmpeg", "-i", "assets/.premix.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r, re.S).group(0))
af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", "assets/.premix.wav", "-af", af, "-ar", "48000", "assets/mezcla.wav"],
               check=True)
out = subprocess.run(["ffmpeg", "-i", "assets/mezcla.wav", "-af", "ebur128", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
I = re.findall(r"I:\s+(-?[\d.]+) LUFS", out)[-1]
print(f"mezcla.wav · {len(cues['cues'])} efectos · {I} LUFS")

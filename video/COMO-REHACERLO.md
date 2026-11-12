# Cómo rehacer el vídeo «Así nació *Aquí no hay quien viva*»

Todo se genera desde la carpeta `video/`. Lo que se ve en pantalla va enganchado a los tiempos
de cada palabra de la voz (`transcript.json`), así que si cambias una frase o la voz, basta con
repetir los pasos y la animación, los subtítulos y los efectos se recolocan solos.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (instala los iconos de Lucide).
- `pip install edge-tts` (voz de Álvaro) y `npx hyperframes skills`.
- Modelo de transcripción Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video

# 1. Voz: Álvaro (castellano de España) a partir de guion.txt
edge-tts --voice es-ES-AlvaroNeural -f guion.txt --write-media voz-alvaro.mp3
#   (en un entorno con proxy: añade  --proxy "$HTTPS_PROXY")
ffmpeg -y -i voz-alvaro.mp3 -ar 48000 -ac 1 voz-raw.wav
python3 scripts/tighten.py voz-raw.wav voz.wav        # pausas de 0,25 s como máximo, sin acelerar

# 2. Momento exacto de cada palabra y comparación con el guion
npx hyperframes transcribe voz.wav --language es --model large-v3
python3 scripts/fix_transcript.py                     # «1.» -> «Uno:», «Mer lo» -> «Merlo»...
python3 scripts/compare.py                            # debe decir IGUALES

# 3. Animación (escribe index.html y compositions/) y mezcla de sonido a -14 LUFS
python3 scripts/gen.py
python3 scripts/mix.py

# 4. Comprobaciones
npx hyperframes check
npx hyperframes snapshot --at 1,5,12,20,27,31,36,43,48,52

# 5. Render
npx hyperframes render -q delivery -o entregas/video-FINAL.mp4
python3 scripts/gen.py --sin-subtitulos
npx hyperframes render -q delivery -o entregas/video-SIN-SUBTITULOS.mp4
python3 scripts/gen.py                                # deja otra vez la versión con subtítulos

# 6. Verificación final
ffmpeg -i entregas/video-FINAL.mp4 -vf blackdetect=d=0.05 -an -f null - 2>&1 | grep black_start   # nada = OK
ffprobe -v error -show_entries format=duration -of csv=p=0 entregas/video-FINAL.mp4               # = duración de voz.wav
```

Para ver solo los primeros segundos: `npx hyperframes render --end 8 -o entregas/prueba-8s.mp4`.

## Qué hay en cada archivo

| Archivo | Para qué sirve |
| --- | --- |
| `guion.txt` | Lo que dice la voz (números escritos en letra para que se lean bien) |
| `scripts/tighten.py` | Recorta silencios largos de la voz |
| `scripts/fix_transcript.py` | Arregla cómo escribe Whisper algunas palabras (no toca los tiempos) |
| `scripts/compare.py` | Compara guion y transcripción palabra a palabra |
| `scripts/gen.py` | Generador: mundo 2D, cámara, personajes, subtítulos. `P("palabra", n)` = cuándo empieza la n-ésima vez que se dice |
| `scripts/scenes2.py` | Escenas de la segunda mitad (castings, Tejero, estreno, final) |
| `scripts/rig.py` | Personajes SVG articulados (cabeza, cuerpo, brazos, piernas, ojos) |
| `scripts/mix.py` | Mezcla voz + efectos (`assets/sfx-cues.json`) + música baja y normaliza a -14 LUFS |
| `assets/sync.json` | Informe: cada anclaje de la animación con la palabra y el segundo en que suena |
| `assets/sfx/`, `assets/music/` | Efectos y música de Mixkit (licencia gratuita de Mixkit) |

## Cambiar cosas habituales

- **Una frase:** edítala en `guion.txt` y repite desde el paso 1. Si cambias una palabra a la que
  está enganchada una animación (p. ej. «videoclub»), cambia también su `P("...")` en `gen.py`/`scenes2.py`.
- **Otra voz:** cambia `--voice` en el paso 1 (`edge-tts --list-voices | grep es-ES`).
- **Volumen de la música:** `MUSIC_VOL` en `scripts/mix.py`.
- **Colores:** `GOOD`, `BAD`, `ACC`, `INK` al principio de `scripts/gen.py`.

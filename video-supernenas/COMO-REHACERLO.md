# Cómo rehacer el vídeo «Las Supernenas de Aquí no hay quien viva»

Todo se genera desde la carpeta `video-supernenas/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-supernenas

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt: «dos mil siete» y «dos mil trece» con letras
edge-tts --voice es-ES-AlvaroNeural -f guion-voz.txt --write-media voz-alvaro.mp3   # con proxy: --proxy "$HTTPS_PROXY"
ffmpeg -y -i voz-alvaro.mp3 -ar 48000 -ac 1 voz-raw.wav
MAX_GAP=0.2 python3 scripts/tighten.py voz-raw.wav voz.wav    # pausas de 0,2 s como máximo, sin acelerar

# 2. Tiempos de cada palabra y comparación con el guion
rm -f transcript.raw.json
npx hyperframes transcribe voz.wav --language es --model large-v3
python3 scripts/fix_transcript.py     # une «en medio» en «Enmedio», parte «100000», quita el «¡Gracias!» que Whisper inventa al final, parte «38%» y, si cuadran las palabras, copia la ortografía del guion
python3 scripts/compare.py            # debe decir IGUALES

# 3. Animación y sonido (-14 LUFS)
python3 scripts/gen.py                # si una escena se engancha a una palabra fuera de su tramo, se para y avisa
python3 scripts/mix.py

# 4. Comprobaciones
npx hyperframes check
npx hyperframes snapshot --at 0,2.5,5.2,10.8,15.8,20.6,25.2,28.5,33.8,40.8,46.9,52,57.5

# 5. Render
npx hyperframes render -q delivery -o entregas/video-FINAL.mp4
python3 scripts/gen.py --sin-subtitulos
npx hyperframes render -q delivery -o entregas/video-SIN-SUBTITULOS.mp4
python3 scripts/gen.py                # vuelve a dejar la versión con subtítulos

# 6. Verificación
ffmpeg -i entregas/video-FINAL.mp4 -vf blackdetect=d=0.05 -an -f null - 2>&1 | grep black_start   # nada = OK
ffprobe -v error -show_entries format=duration -of csv=p=0 entregas/video-FINAL.mp4               # = duración de voz.wav
```

Solo los primeros segundos: `npx hyperframes render --end 8 -o entregas/prueba-8s.mp4`.

## Archivos

| Archivo | Para qué sirve |
| --- | --- |
| `guion.txt` / `guion-voz.txt` | Texto del vídeo / texto que lee la voz (pronunciación) |
| `scripts/tighten.py` | Recorta silencios (`MAX_GAP`) |
| `scripts/fix_transcript.py` | Arregla la escritura de Whisper sin tocar los tiempos |
| `scripts/compare.py` | Compara guion y voz palabra a palabra |
| `scripts/gen.py` | Motor: cámara, `P("palabra", n)`, rodillos, subtítulos, composición |
| `scripts/scenes.py` | Las escenas: homenaje (tres retratos y lazo), 1 · quiénes eran, El verdugo, el casting de Vicenta (María Asquerino), 2 · la mirilla y el portal, las frases, 3 · el impacto (tele, sofá, memes), La que se avecina, las tres estrellas y la encuesta |
| `scripts/rig.py` | Personajes SVG articulados (estilo propio, no imitan a las actrices): Marisa (`vecina1`), Concha (`vecina2`), Vicenta (`vicenta`) |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («Vicenta», «Concha», «Marisa», «tres», «Supernenas»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Audio

Tras el render se vuelve a poner `assets/mezcla.wav` (−14 LUFS) sin tocar la imagen:
`ffmpeg -i entregas/video-FINAL.mp4 -i assets/mezcla.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest entregas/tmp.mp4`

## Portada

`python3 ../portadas/hacer_portadas.py video-supernenas` -> `entregas/portada.png` (y copia en `portadas/`).

## Fuentes y datos a comprobar

- «Las Supernenas»: Marisa (Mariví Bilbao), Concha (Emma Penella) y Vicenta (Gemma Cuervo) (SensaCine).
- Vicenta iba a ser María Asquerino, que rechazó el papel tras leer el guion (SensaCine, El Debate).
- Las tres pasaron a La que se avecina como Izaskun, Charo y Mari Tere (FormulaTV).
- Emma Penella murió en agosto de 2007; Mariví Bilbao en 2013; Gemma Cuervo el 14 de marzo de 2026 (Euronews, Hola).
- [COMPROBAR] Que Emma Penella protagonizó El verdugo de Berlanga (de conocimiento propio).

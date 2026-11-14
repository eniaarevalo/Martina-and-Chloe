# Cómo rehacer el vídeo «¿Cenamos tarde por culpa de Hitler?»

Todo se genera desde la carpeta `video-hora/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-hora

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt: «mil novecientos cuarenta» y «la agencia Sinc» para que lo lea bien
edge-tts --voice es-ES-AlvaroNeural -f guion-voz.txt --write-media voz-alvaro.mp3   # con proxy: --proxy "$HTTPS_PROXY"
ffmpeg -y -i voz-alvaro.mp3 -ar 48000 -ac 1 voz-raw.wav
MAX_GAP=0.2 python3 scripts/tighten.py voz-raw.wav voz.wav    # pausas de 0,2 s como máximo, sin acelerar

# 2. Tiempos de cada palabra y comparación con el guion
rm -f transcript.raw.json
npx hyperframes transcribe voz.wav --language es --model large-v3
python3 scripts/fix_transcript.py     # quita el «¡Gracias!» que Whisper inventa al final, parte «38%» y, si cuadran las palabras, copia la ortografía del guion
python3 scripts/compare.py            # debe decir IGUALES

# 3. Animación y sonido (-14 LUFS)
python3 scripts/gen.py                # si una escena se engancha a una palabra fuera de su tramo, se para y avisa
python3 scripts/mix.py

# 4. Comprobaciones
npx hyperframes check
npx hyperframes snapshot --at 0,5.0,10.5,13.4,18.0,22.9,26.5,31.2,34.0,40.0,46.6,50.6,53.2

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
| `scripts/scenes.py` | Las escenas: el plato y el reloj de las 22:00 con «¿MITO?», 1 · el cambio de 1940, el mapa Galicia–Londres–Polonia, el sol con retraso, 2 · el mito (España y Alemania, «NO CUADRA»), 3 · la verdadera razón (posguerra, dos trabajos, estudio difundido por SINC), las cenas de hoy y el Congreso con la encuesta |
| `scripts/rig.py` | Personajes SVG articulados (estilo propio): el trabajador de la posguerra |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («Hitler», «1940», «dos», «sol», «Londres»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Audio

Tras el render se vuelve a poner `assets/mezcla.wav` (−14 LUFS) sin tocar la imagen:
`ffmpeg -i entregas/video-FINAL.mp4 -i assets/mezcla.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest entregas/tmp.mp4`

## Portada

`python3 ../portadas/hacer_portadas.py video-hora` -> `entregas/portada.png` (y copia en `portadas/`).

## Fuentes y datos a comprobar

- Cambio de hora de 1940: en 1940 Franco adelanta los relojes una hora (Euronews; Planesas).
- Lo de «para ir con la hora de Hitler» es un bulo según Euronews: en la primavera de 1940 Alemania usaba horario de verano y seguía una hora por delante.
- Posguerra y dos trabajos como motivo de los horarios tardíos [COMPROBAR] (explicación habitual; ver Planesas).
- Estudio difundido por la agencia SINC: en España vivimos más según el sol que según el reloj.
- Volver a la hora de Portugal: propuesta debatida durante años en el Congreso.
- [COMPROBAR] «Cenan a las cinco o las seis» en los países nórdicos es aproximado y cambia según el país.

# Cómo rehacer el vídeo «La niña del puerto» (historia de terror, ficción)

Todo se genera desde la carpeta `video-terror/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-terror

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt: años con letras. La voz va más lenta y grave: añade --rate=-8% --pitch=-6Hz a edge-tts
# tighten con MAX_GAP=0.45 (pausas más largas, para el suspense)
edge-tts --voice es-ES-AlvaroNeural -f guion-voz.txt --write-media voz-alvaro.mp3   # con proxy: --proxy "$HTTPS_PROXY"
ffmpeg -y -i voz-alvaro.mp3 -ar 48000 -ac 1 voz-raw.wav
MAX_GAP=0.45 python3 scripts/tighten.py voz-raw.wav voz.wav    # pausas de 0,2 s como máximo, sin acelerar

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
npx hyperframes snapshot --at 0,6.5,11.5,19.8,25.5,31.5,35.9,41.5,45,50.5,57.5,62.5,66.8,69.8

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
| `scripts/scenes.py` | Las escenas: la llegada (jueves), la niña bajo la farola, las preguntas escritas a mano, el puerto (sábado), tres días, la foto de 1986, las tres de la mañana y el lunes con la foto de 2008. Niebla, parpadeos y la niña que nunca camina ni parpadea |
| `scripts/rig.py` | Personajes SVG: la niña (`nina`), el padre (`padre`), la madre (`madre`), la hija pequeña (`hija`) y el dueño (`g1`) |
| `scripts/mix.py` | Voz + ambiente de terror (Mixkit «Horror ambience», volumen 0,10) + viento, latidos y golpes; normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («niña», «foto», «tres», «domingo», «2008»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Audio

Tras el render se vuelve a poner `assets/mezcla.wav` (−14 LUFS) sin tocar la imagen:
`ffmpeg -i entregas/video-FINAL.mp4 -i assets/mezcla.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest entregas/tmp.mp4`

## Portada

`python3 ../portadas/hacer_portadas.py video-terror` -> `entregas/portada.png` (y copia en `portadas/`).

## Nota

Es una historia de ficción. El vídeo termina con el rótulo «HISTORIA DE FICCIÓN»; conviene repetirlo en la descripción (#historiadeterror).
Sonidos de Mixkit (licencia gratuita): Horror ambience, Scary wind, Horror impact, Hard horror hit drum, Horror deep drum heartbeat, Terror transition, Horror swish.

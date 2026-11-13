# Cómo rehacer el vídeo «¿Por qué cruzamos los dedos?»

Todo se genera desde la carpeta `video-dedos/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-dedos

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt: «dos mil diez» con letras
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
npx hyperframes snapshot --at 0,0.6,8.4,12.8,16.8,22.5,29,32.7,36.6,40.6,43.6,46.8,50.6,53.4

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
| `scripts/scenes.py` | Las escenas: la mano cruzada (dibujo SVG propio, `hand_cross()`; el ángulo de los dedos está en `IDX_R` y `MID_R`), 1 · la cruz (escudo y fantasmas), la otra teoría (índices y deseo, «sin pruebas»), 2 · las mentiras (rayos X detrás de la espalda), 3 · la ciencia (golf), la réplica («no se repitió»), de viaje (Vietnam y Alemania) y comentarios |
| `scripts/rig.py` | Personaje SVG articulado: el chico que miente (`g1`) |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («dedos», «cruz», «suerte», «la», «seguridad»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Portada

`python3 ../portadas/hacer_portadas.py video-dedos` -> `entregas/portada.png` (y copia en `portadas/`).

## Fuentes y datos a comprobar

- Origen: no hay documentación histórica; la explicación más aceptada es la cruz cristiana (BBC Mundo, National Geographic). La de los índices para sellar un deseo es otra teoría popular (El Espectador).
- Cruzar los dedos a la espalda al mentir: costumbre popular (BBC Mundo).
- Damisch, Stoberock y Mussweiler (Psychological Science, 2010): la «pelota de la suerte» mejoró los putts. Calin-Jageman y Caldwell (2014) no lo replicaron.
- Vietnam (insulto) y Alemania (apretar los pulgares, «Ich drücke dir die Daumen»).
- [COMPROBAR] Lo de Vietnam viene de blogs de viaje, aunque todos coinciden.

# Cómo rehacer el vídeo «¿Y si Vicente Maroto entrenara al Atlético?»

Todo se genera desde la carpeta `video-vicente/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-vicente

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt: igual que guion.txt pero sin comillas «»
edge-tts --voice es-ES-AlvaroNeural -f guion-voz.txt --write-media voz-alvaro.mp3   # con proxy: --proxy "$HTTPS_PROXY"
ffmpeg -y -i voz-alvaro.mp3 -ar 48000 -ac 1 voz-raw.wav
MAX_GAP=0.2 python3 scripts/tighten.py voz-raw.wav voz.wav    # pausas de 0,2 s como máximo, sin acelerar

# 2. Tiempos de cada palabra y comparación con el guion
rm -f transcript.raw.json
npx hyperframes transcribe voz.wav --language es --model large-v3
python3 scripts/fix_transcript.py     # separa «tiki-taka» en dos palabras (como en el guion) y copia la ortografía del guion
python3 scripts/compare.py            # debe decir IGUALES

# 3. Animación y sonido (-14 LUFS)
python3 scripts/gen.py                # si una escena se engancha a una palabra fuera de su tramo, se para y avisa
python3 scripts/mix.py

# 4. Comprobaciones
npx hyperframes check
npx hyperframes snapshot --at 0.25,1.3,4.2,9.9,14.0,16.6,20.6,23.9,27.8,33.3,36.5,39.2,41.9

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
| `scripts/scenes.py` | Las escenas: el sofá que cae en el campo (gancho), lo que sabemos (Goya, Vicente, Javier, corona), 1 · entrenamiento, 2 · táctica (tiki taka en la pizarra), 3 · banquillo → sofá, 4 · partidos 0–0, rueda de prensa y encuesta. `sofa()` dibuja el sofá en dos piezas (respaldo detrás y asiento delante) para que el personaje parezca sentado; la clase es `sofa2` porque `.sofa` ya existe en gen.py |
| `scripts/rig.py` | Personajes SVG de estilo propio: Vicente (`vicente`, chándal rojo), Goya (`goya`), Javier (`javier`) y jugadores a rayas rojas y blancas (`atm`, `atm2`) |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («sofá», «Vicente», «tiki», «siesta»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Audio

Tras el render se vuelve a poner `assets/mezcla.wav` (−14 LUFS) sin tocar la imagen:
`ffmpeg -i entregas/video-FINAL.mp4 -i assets/mezcla.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest entregas/tmp.mp4`

## Portada

`python3 ../portadas/hacer_portadas.py video-vicente` -> `entregas/portada.png` (y copia en `portadas/`).

## Contenido

- Es un **«¿qué habría pasado si…?» imaginado**: todo lo del Atlético es inventado y lleva la etiqueta «CRUCE IMAGINADO» / sello «IMAGINADO».
- Lo real: Vicente Maroto (Ricardo Arroyo) es el padre de Javier, el marido de Goya y famoso por vago y por el sofá, «el hombre cojín» (eCartelera, eldiario.es, El Observador).
- El tiki taka: idea pedida por la autora; no se cita ninguna frase literal de la serie.
- Sin escudo oficial ni entrenadores reales: solo rayas rojas y blancas.
- Personajes dibujados en estilo propio, sin imágenes de la serie.

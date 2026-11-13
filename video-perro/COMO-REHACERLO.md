# Cómo rehacer el vídeo «Lo que un perro hace en tu cabeza»

Todo se genera desde la carpeta `video-perro/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-perro

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt: «veinticuatro por ciento» escrito con letras
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
npx hyperframes snapshot --at 0.6,4.3,14.8,18.9,26.3,28.7,31.5,40.5,46.5,51,55.6

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
| `scripts/scenes.py` | Las escenas: la mirada y el cerebro, 1 · la felicidad (oxitocina, probetas), el cortisol (10 min), 2 · la responsabilidad (agenda y lluvia), la rutina (despertador y sol), 3 · la madurez (YO → él, empatía y autoestima), la salud (3,8 M, −24 %) y «no es un capricho» con comentarios. El perro es un dibujo SVG propio (`dog()`) con cola y cabeza animadas |
| `scripts/rig.py` | Personajes SVG articulados: el dueño (`g1`) y el niño (`g3`) |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («perro», «la», «dos», «depende», «hormona», «y»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Fuentes y datos a comprobar

- Nagasawa et al. (Science, 2015): la mirada entre perro y dueño sube la oxitocina en los dos.
- Pendry y Vandagriff (AERA Open, 2019): 10 minutos acariciando perros y gatos bajan el cortisol (249 universitarios).
- Brooks et al. (BMC Psychiatry, 2018): revisión de 17 estudios; las mascotas ayudan a gestionar problemas de salud mental (resultados numéricos mixtos).
- Purewal et al. (2017): en niños, tener mascota se asocia con más autoestima y empatía.
- Kramer et al. (2019): 3,8 millones de personas; tener perro se asocia con un 24 % menos de riesgo de muerte (asociación, no causa).
- [COMPROBAR] La comparación con el vínculo madre-bebé (es cómo lo plantean los autores; otros científicos piden prudencia).

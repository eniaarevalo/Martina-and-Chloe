# Cómo rehacer el vídeo «Lo que pasaba detrás de las cámaras de La que se avecina»

Todo se genera desde la carpeta `video-rodaje/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-rodaje

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
python3 scripts/fix_transcript.py     # quita el «a» que Whisper oye en «llamó Mauri» y copia la ortografía del guion
python3 scripts/compare.py            # debe decir IGUALES

# 3. Animación y sonido (-14 LUFS)
python3 scripts/gen.py                # si una escena se engancha a una palabra fuera de su tramo, se para y avisa
python3 scripts/mix.py

# 4. Comprobaciones
npx hyperframes check
npx hyperframes snapshot --at 0.4,3.4,5.6,9.5,12.0,13.9,17.9,21.0,26.8,31.0,33.2,38.3,41.5

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
| `scripts/scenes.py` | Las escenas: «¡Mauri!» (Gil y Merlo, toma falsa), 1 · era un plató (el edificio gira y enseña los andamios), el conflicto, cerrar el círculo (Montepinar cae donde estaba el portal de Aquí no hay quien viva), 2 · risas de más, el edificio nuevo (11 pisos, 2 patios, bar) y la encuesta |
| `scripts/rig.py` | Personajes SVG de estilo propio: José Luis Gil (`pastor`), Luis Merlo (`mauri`) y dos actores genéricos (`g1`, `g2`) |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («Montepinar», «plató», «tomas», «Aquí»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Audio

Tras el render se vuelve a poner `assets/mezcla.wav` (−14 LUFS) sin tocar la imagen:
`ffmpeg -i entregas/video-FINAL.mp4 -i assets/mezcla.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest entregas/tmp.mp4`

## Portada

`python3 ../portadas/hacer_portadas.py video-rodaje` -> `entregas/portada.png` (y copia en `portadas/`).

## Fuentes

- José Luis Gil llama «Mauri» a Luis Merlo en las tomas falsas de la temporada 12 (FormulaTV).
- Montepinar era un decorado de plató; la serie lo dejó por un conflicto entre los productores y los propietarios del plató (Hola, agosto de 2019).
- Las últimas escenas de Montepinar (2020) se grabaron en el plató 2, en el mismo lugar donde estuvo el portal de Aquí no hay quien viva; Alberto Caballero: «cerrar el círculo» (FormulaTV, junio de 2020).
- Macarena Gómez: algunos compañeros exageran la risa porque saben que salen en las tomas falsas (FormulaTV).
- Contubernio 49: 11 pisos, dos patios, rellanos, portal y bar (FormulaTV).
- Descartada por no poder confirmarla: la anécdota de la ambulancia en la puerta del plató.

# Cómo rehacer el vídeo «¿Por qué las ventanas de los aviones son redondas?»

Todo se genera desde la carpeta `video-aviones/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-aviones

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt: «mil novecientos cincuenta y cuatro» y «Cómet» con tilde para que lo pronuncie bien
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
npx hyperframes snapshot --at 0,3.3,7,10.6,12.9,15.6,21.3,27,30.6,33.2,36.5,38.3,43,48.9,53,56.8

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
| `scripts/scenes.py` | Las escenas: 1954 y la esquina, el Comet (presurizada), el globo, 1 · la fatiga (clip y chapa), 2 · las esquinas (tanque de agua, grieta en la ventanita del techo, esquina contra curva), 3 · la solución (ventana redondeada, fuselaje grueso, 3 capas y agujerito), ventanilla y comentarios |
| `scripts/rig.py` | Personaje SVG articulado: la pasajera (`g2`); el avión se dibuja en `scenes.py` (`plane()`) |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («esquina», «dos», «tres», «Comet», «vuelo», «agujerito»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Fuentes y datos a comprobar

- El de Havilland Comet, primer avión comercial a reacción (en servicio desde 1952); dos accidentes en 1954 por fatiga del metal.
- Investigación de Farnborough con el fuselaje en un tanque de agua; el informe sitúa el origen de la grieta en la esquina de la ventanita de la antena del techo (no en las ventanas de pasajeros).
- Comet 4 (1958): ventanas ovaladas y fuselaje más grueso.
- Ventanillas de tres capas con agujerito en la del medio (Mental Floss, The Points Guy).
- [COMPROBAR] Fechas exactas de los accidentes (10 de enero y 8 de abril de 1954).

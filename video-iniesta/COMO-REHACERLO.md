# Cómo rehacer el vídeo «La historia detrás del gol de Iniesta»

Todo se genera desde la carpeta `video-iniesta/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-iniesta

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt escribe los números con letras («Once de julio de dos mil diez», «veintiséis», «dos mil doce»)
edge-tts --voice es-ES-AlvaroNeural -f guion-voz.txt --write-media voz-alvaro.mp3   # con proxy: --proxy "$HTTPS_PROXY"
ffmpeg -y -i voz-alvaro.mp3 -ar 48000 -ac 1 voz-raw.wav
MAX_GAP=0.2 python3 scripts/tighten.py voz-raw.wav voz.wav    # pausas de 0,2 s como máximo, sin acelerar

# 2. Tiempos de cada palabra y comparación con el guion
rm -f transcript.raw.json
npx hyperframes transcribe voz.wav --language es --model large-v3
python3 scripts/fix_transcript.py     # si hay tantas palabras como en el guion, copia su ortografía y puntuación (los tiempos no cambian)
python3 scripts/compare.py            # debe decir IGUALES

# 3. Animación y sonido (-14 LUFS)
python3 scripts/gen.py                # si una escena se engancha a una palabra fuera de su tramo, se para y avisa
python3 scripts/mix.py

# 4. Comprobaciones
npx hyperframes check
npx hyperframes snapshot --at 0,4,10,15.3,17.5,20.5,26.5,33.5,42.8,47.8,50.5,53.5

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
| `scripts/scenes.py` | Las escenas: la final (marcador, fecha, prórroga y reloj 116'), la jugada en el campo y el gol, Camacho en la tele, la camiseta, Dani, la nube que se va y sale el sol, premios, grada del Espanyol y comentarios |
| `scripts/rig.py` | Personajes SVG articulados: Iniesta (`ini`, camiseta roja con el 6) y Dani de niño (`jar`, blanquiazul) |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («Cesc», «Andrés», «gol», «Dani», «ese», «año», «Espanyol»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Fuentes y datos a comprobar

- Entrevista en The Athletic (nov. 2025), resumida en Trivela y A Bola: el gol le ayudó a salir de un lugar oscuro.
- «La jugada de mi vida» (autobiografía) y el documental «Andrés Iniesta, el héroe inesperado»: la depresión de 2009-2010.
- RFEF: «Mi gol en la final de Sudáfrica fue la apoteosis de toda una vida».
- [COMPROBAR] 2.º en el Balón de Oro 2010 y Mejor Jugador de Europa UEFA 2012 (de memoria, no salieron en la búsqueda).
- [COMPROBAR] Orden exacto de la jugada antes del pase de Cesc.

La letra manuscrita es Caveat (`assets/fonts/caveat-700.woff2`, licencia OFL), incluida en el proyecto para que el render la use.

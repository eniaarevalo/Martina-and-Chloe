# Cómo rehacer el vídeo «¿Existe Mirador de Montepinar?»

Todo se genera desde la carpeta `video-montepinar/`. La animación va enganchada a los tiempos de cada
palabra de la voz (`transcript.json`): si cambias una frase o la voz, repite los pasos y todo
(cámara, camino, personajes, subtítulos y efectos) se recoloca solo.

## Requisitos (una vez)

- Node 22 o superior, Python 3, ffmpeg.
- `npm install` (iconos de Lucide) · `pip install edge-tts` · `npx hyperframes skills`.
- Modelo Whisper `large-v3` (lo descarga HyperFrames la primera vez; ~3 GB).

## Pasos

```bash
cd video-montepinar

# 1. Voz de Álvaro (castellano de España)
#    guion.txt     = lo que se dice (sirve para comparar y para los subtítulos)
#    guion-voz.txt = el texto que lee la voz (aquí es igual; sirve para forzar pronunciaciones)
# guion-voz.txt: «dos mil veinte», «cuarenta y nueve», «mil quinientos» y «ochocientos» con letras
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
npx hyperframes snapshot --at 0,3.9,7.8,11.9,15,18.9,28,32.8,36.5,41.2,44.5,49.6,53.2

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
| `scripts/scenes.py` | Las escenas: «NO EXISTE», 1 · el decorado (Moraleja de Enmedio, Desengaño 21 y Montepinar en la nave), el truco (portal, rellano y piso separados), 2 · el adiós (tío y sobrinos, contrato roto), el derribo (2007 → 2020), 3 · la mudanza (Contubernio 49, 1.500 y 800 m²), la fachada al aire libre y el mapa «sin resultados» con comentarios |
| `scripts/rig.py` | Personaje SVG articulado: el vecino (`g1`); los edificios se dibujan en `scenes.py` (`building()`, `nave()`) |
| `scripts/mix.py` | Voz + efectos + música baja, normalizado a -14 LUFS |
| `assets/sync.json` | Cada anclaje con la palabra y el segundo en que suena |

## Ojo con `P("palabra", n)`

Si una palabra se repite («Montepinar», «plató», «decorado», «dos», «tres»…), `n` dice cuál de ellas. Si te equivocas,
`gen.py` se para con un mensaje que dice qué escena y qué palabra están fuera de su sitio.


## Fuentes y datos a comprobar

- Plató de Moraleja de Enmedio (Madrid), donde se grabaron Aquí no hay quien viva y La que se avecina (FormulaTV, Diez Minutos).
- El plató era propiedad del tío de los creadores, José Luis Moreno; sin acuerdo con el alquiler, en 2020 se dejó y el decorado se destruyó (FormulaTV, Merca2, OKDiario).
- Contubernio 49 desde la temporada 13: dos platós de 1.500 y 800 m² y un decorado exterior de calle (eCartelera, Merca2).
- [COMPROBAR] Que portal, rellanos y pisos eran decorados separados (Idealista; solo se pudo leer el resumen).
- [COMPROBAR] Si el plató era de José Luis Moreno a título personal o de una empresa de su familia.

# Evaluador de Impacto Biofisico de Mutaciones en TP53

Aplicacion educativa (Fundamentos de Biofisica) que, dada una mutacion puntual
asociada a cancer en la proteina **p53** (gen *TP53*), **explica el mecanismo
biofisico** por el que la mutacion rompe la funcion de la proteina: cambios
fisicoquimicos del aminoacido, localizacion en dominios funcionales, estabilidad
del pliegue y consecuencias estructurales.

> **Principio rector.** No competimos con predictores clinicos (SIFT, PolyPhen,
> AlphaMissense). Es una **herramienta didactica de interpretacion heuristica** que
> explica el *porque* desde principios fisicoquimicos. Todos los datos biologicos
> fueron verificados en fuentes publicas (ver pagina "Glosario y referencias").

## Estructura

```
BIOFISICA/
├── data/
│   ├── mutaciones.json   # 4 mutaciones hotspot verificadas (R175H, R248W, G245S, R282W)
│   │                     #   incluye ΔΔG, Tm, dependencia de temperatura, clase AlphaMissense
│   ├── dominios.json     # 3 dominios funcionales verificados
│   ├── gen_tp53.json     # gen/proteina: cromosoma, secuencia (UniProt), estabilidad WT
│   └── 1tup.pdb          # estructura 3D del complejo p53-ADN (RCSB, para el visor)
├── lib/
│   └── 3Dmol-min.js      # libreria del visor 3D (local, para funcionar sin internet)
├── paginas/
│   ├── introduccion.py   # 1. explorador del gen (cromosoma / dominios / secuencia)
│   ├── evaluador.py      # 2. evaluador de una mutacion (analisis completo)
│   ├── comparar.py       # 3. comparar las 4 mutaciones lado a lado
│   ├── personalizada.py  # 4. laboratorio: cualquier posicion / aminoacido
│   ├── quiz.py           # 5. quiz "¿contacto o estructural?"
│   └── referencias.py    # 6. glosario y referencias con DOIs
├── imagenes/
│   └── regulacion_transcripcional.png  # (la agregas tu) imagen de regulacion transcripcional
├── biofisica.py          # motor de calculo, interpretacion y datos
├── estructura3d.py       # genera el HTML del visor 3D (1TUP + 3Dmol.js embebidos)
├── estilos.py            # CSS compartido (estetica academica) entre paginas
├── grafo.py              # grafo interactivo mutacion <-> cancer (pyvis)
├── app.py                # punto de entrada: configuracion + navegacion entre paginas
├── pymol_render.py       # opcional: PNG estaticos de alta calidad con PyMOL (ver abajo)
└── requirements.txt
```

## Instalacion

```
pip install -r requirements.txt
```

(equivale a `pip install streamlit plotly pyvis biopython`)

El visor 3D **no** requiere paquetes adicionales ni internet: la libreria y la
estructura estan incluidas en `lib/` y `data/`.

## Ejecucion

En Windows, si `python` no esta en el PATH usa el lanzador `py`:

```
py -m streamlit run app.py
```

o bien `python -m streamlit run app.py`.

Prueba rapida del motor e integridad de los JSON:

```
py biofisica.py
py -c "import json; json.load(open('data/mutaciones.json', encoding='utf-8')); print('OK')"
```

## Las 6 paginas

1. **El gen TP53** — recorrido guiado en 4 pasos: ubicacion cromosomica (17p13.1),
   ficha del gen/proteina, mapa de dominios funcionales, y la secuencia completa
   (393 aa, UniProt P04637) con las 4 mutaciones resaltadas.
2. **Evaluador de mutaciones** — para la mutacion elegida: cambios fisicoquimicos,
   indice heuristico, mecanismo contacto/estructural, **ΔΔG de plegamiento**,
   **curva de estabilidad frente a la temperatura**, **visor 3D interactivo**,
   implicancias y el grafo mutacion-cancer.
3. **Comparar mutaciones** — las 4 lado a lado: cambios fisicoquimicos, ΔΔG,
   tabla resumen, **validacion honesta** (heuristica vs. ΔΔG medido) y mapa de
   calor de tipos de cancer.
4. **Laboratorio de mutaciones** — elige *cualquier* posicion y *cualquier*
   aminoacido; el motor calcula el impacto fisicoquimico en vivo. Detecta si
   coincide con una hotspot catalogada.
5. **Quiz** — autoevaluacion "¿contacto o estructural?" con feedback y puntaje.
6. **Glosario y referencias** — 19 terminos clave y las fuentes con DOI.

## Que hace el motor (`biofisica.py`)

- `calcular_cambios` — deltas de carga, hidrofobicidad (Kyte-Doolittle) y
  volumen (Zamyatnin), mas cambio de polaridad.
- `calcular_impacto` — indice heuristico (0-14; Bajo/Moderado/Alto), inspirado en
  la logica de SIFT/PolyPhen pero simplificado y transparente.
- `interpretar_mutacion` — integra mutacion + dominio + calculos.
- `generar_interpretacion` / `generar_implicancias` — texto explicativo e
  implicancias (clinica, terapeutica, conceptual).
- `generar_texto_estabilidad` — parrafo sobre el ΔΔG y su conexion con el mecanismo.
- `fraccion_plegada` / `generar_texto_temperatura` — curva de plegamiento (modelo
  de dos estados centrado en el Tm **medido**) y su explicacion.
- `aa_tres_en_posicion` / `dominio_en_posicion` / `mutacion_catalogada` — apoyo del
  laboratorio de mutaciones personalizadas.

## Visor 3D interactivo

La pagina del evaluador muestra la estructura del dominio de union al ADN de p53
(**PDB 1TUP**, Cho et al. 1994) con el residuo mutado resaltado, usando 3Dmol.js.
Es **rotable, con zoom, y funciona sin conexion** (la libreria y el PDB estan
embebidos). Hace visible la distincion central del proyecto: en R248W el residuo
se asoma hacia el ADN (**contacto**); en R175H queda enterrado en el nucleo de la
proteina (**estructural**).

### Agregar la imagen de regulacion transcripcional

Coloca el archivo como `imagenes/regulacion_transcripcional.png`. Mientras no
exista, el paso 2 del explorador muestra un marcador de posicion.

### Opcional: PNG estaticos con PyMOL

`pymol_render.py` genera imagenes de alta calidad del residuo sobre 1TUP si
quieres figuras estaticas de publicacion (corre `pymol -cq pymol_render.py`, o
File > Run Script dentro de PyMOL). No es necesario: el visor interactivo ya
cubre esta funcion dentro de la app.

## Nota de integridad cientifica

Los valores marcados como `por verificar` (p. ej. algunas clasificaciones ClinVar
somaticas, o el Tm exacto de las mutantes sin dato) no se rellenaron con datos
inventados. Cada dato de estabilidad lleva su campo de `precision` (medido /
aproximado / limite inferior) y su fuente.

La secuencia de aminoacidos y la ubicacion cromosomica (`data/gen_tp53.json`) se
obtuvieron directamente de UniProt (`rest.uniprot.org/uniprotkb/P04637.fasta`) y
de NCBI Gene (`eutils.ncbi.nlm.nih.gov`, Gene ID 7157), y se verifico que las
posiciones 175, 245, 248 y 282 coinciden exactamente con los aminoacidos
originales de `mutaciones.json`. Los DOIs de la pagina de referencias fueron
confirmados uno por uno.

*Fecha de la ultima actualizacion de datos: 2026-07-08.*

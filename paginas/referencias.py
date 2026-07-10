# -*- coding: utf-8 -*-
"""
Página: Glosario y referencias.

Glosario de términos clave y lista de fuentes con DOI. Todos los DOIs fueron
verificados; los que no se pudieron confirmar se marcan explícitamente.
"""

import streamlit as st

from biofisica import SCORE_MAXIMO
from estilos import seccion, hero

# ---------------------------------------------------------------------------
# Contenido (curado)
# ---------------------------------------------------------------------------
GLOSARIO = [
    ("Dominio de unión al ADN (DBD)",
     "Región central de p53 (residuos ~100–288) que reconoce y se une a secuencias "
     "específicas del ADN. Aquí cae la mayoría de las mutaciones oncogénicas."),
    ("Dominio de oligomerización",
     "Región (~319–357) que permite a p53 ensamblarse en tetrámeros, su forma funcional."),
    ("Tetrámero",
     "Complejo de cuatro subunidades de p53. p53 solo une el ADN de forma eficiente "
     "como tetrámero."),
    ("Efecto dominante negativo (DNE)",
     "Una subunidad mutante «envenena» al tetrámero al mezclarse con subunidades "
     "normales, inactivando también al alelo sano."),
    ("Mutación hotspot",
     "Posición que muta con frecuencia desproporcionada en tumores (p. ej. R175, "
     "R248, R273)."),
    ("Mecanismo de contacto",
     "La mutación elimina un residuo que toca directamente el ADN; el pliegue se "
     "conserva pero se pierde el contacto químico."),
    ("Mecanismo estructural",
     "La mutación desestabiliza el pliegue del dominio; el residuo no toca el ADN, "
     "pero sostiene la estructura sin la cual no hay unión."),
    ("Kd (constante de disociación)",
     "Concentración a la que la mitad de la proteína está unida al ADN. Menor Kd = "
     "mayor afinidad. El tipo salvaje se reporta en un rango ~5–10 nM según el "
     "elemento de respuesta de ADN usado en el ensayo (no un valor único)."),
    ("ΔΔG",
     "Cuánto desestabiliza una mutación el plegamiento, en kcal/mol, respecto al tipo "
     "salvaje. Convención: ΔΔG > 0 = mutante MENOS estable (mutante − silvestre). "
     "Mayor ΔΔG = pliegue más débil."),
    ("Tm (temperatura de fusión)",
     "Temperatura a la que la mitad de la proteína está desplegada. El DBD de p53 "
     "tiene Tm ≈ 42.9 °C (medida por fluorimetría de barrido diferencial, Life 2023, "
     "13:31), apenas por encima de los 37 °C corporales."),
    ("Hidrofobicidad (escala Kyte–Doolittle)",
     "Tendencia de un aminoácido a evitar el agua. Valores altos = más hidrofóbico."),
    ("Volumen molecular (escala Zamyatnin)",
     "Tamaño del aminoácido en Å³; cambios grandes causan choques estéricos o cavidades."),
    ("Polaridad",
     "Si la cadena lateral es polar (interactúa con agua y cargas) o no polar."),
    ("Conservación evolutiva",
     "Qué tanto se mantiene un residuo entre especies; los conservados suelen ser "
     "funcionalmente críticos."),
    ("Ganancia de función (GOF)",
     "Cuando la p53 mutante adquiere actividades oncogénicas nuevas, más allá de "
     "perder su función supresora."),
    ("Índice de impacto biofísico",
     f"Nuestro puntaje heurístico (0–{SCORE_MAXIMO}) que combina los cambios "
     "fisicoquímicos y la localización. Los pesos son un diseño pedagógico "
     "propio, no un score calibrado estadísticamente. Es didáctico, no un "
     "predictor clínico."),
    ("Síndrome de Li-Fraumeni",
     "Predisposición hereditaria a múltiples cánceres, causada por mutaciones "
     "germinales en TP53."),
    ("AlphaMissense / SIFT / PolyPhen",
     "Predictores computacionales de patogenicidad de variantes; AlphaMissense usa "
     "aprendizaje profundo."),
    ("NCI TP53 (antes IARC) / ClinVar / UniProt / Pfam",
     "Bases de datos públicas de mutaciones tumorales, variantes clínicas, "
     "secuencias/proteínas y dominios, respectivamente. La base de mutaciones "
     "tumorales de TP53 se administraba antes en el IARC y hoy la aloja el NCI."),
]

# (categoría, cita, doi_o_None, url_o_None)
REFERENCIAS = [
    ("Bases de datos y fuentes de datos",
     "NCI TP53 Database (anteriormente IARC TP53 Database), versión R21, enero 2025. "
     "Base de datos de mutaciones somáticas y germinales de TP53.", None,
     "http://tp53.cancer.gov/"),
    ("Bases de datos y fuentes de datos",
     "ClinVar (NCBI). Archivo de relaciones entre variantes y fenotipos.", None,
     "https://www.ncbi.nlm.nih.gov/clinvar/"),
    ("Bases de datos y fuentes de datos",
     "UniProt P04637 (P53_HUMAN). Secuencia canónica (393 aa, SV=4) y dominios.", None,
     "https://www.uniprot.org/uniprotkb/P04637"),
    ("Bases de datos y fuentes de datos",
     "Pfam PF00870 (dominio de unión al ADN de p53) y PF07710 (tetramerización).",
     None, "https://www.ebi.ac.uk/interpro/"),
    ("Bases de datos y fuentes de datos",
     "NCBI Gene ID 7157 (TP53); localización 17p13.1, ensamblaje GRCh38 / NC_000017.11.",
     None, "https://www.ncbi.nlm.nih.gov/gene/7157"),

    ("Estructura tridimensional",
     "Cho Y, Gorina S, Jeffrey PD, Pavletich NP (1994). Crystal structure of a p53 "
     "tumor suppressor–DNA complex: understanding tumorigenic mutations. Science "
     "265:346–355 (PDB 1TUP).", "10.1126/science.8023157", None),

    ("Estabilidad termodinámica (ΔΔG, Tm)",
     "Bullock AN, Henckel J, Fersht AR (1997). Thermodynamic stability of wild-type "
     "and mutant p53 core domain. PNAS 94:14338–14342.", "10.1073/pnas.94.26.14338",
     None),
    ("Estabilidad termodinámica (ΔΔG, Tm)",
     "Joerger AC, Ang HC, Fersht AR (2006). Structural basis for understanding "
     "oncogenic p53 mutations and designing rescue drugs. PNAS 103:15056–15061.",
     "10.1073/pnas.0607286103", None),
    ("Estabilidad termodinámica (ΔΔG, Tm)",
     "Estabilidad térmica de mutantes de p53 por fluorimetría de barrido diferencial "
     "(DSF). Life 2023, 13:31 (WT Tm 42.9 °C; R248W 39.3 °C).",
     "10.3390/life13010031", None),
    ("Estabilidad termodinámica (ΔΔG, Tm)",
     "Joerger AC, Fersht AR (2008). Structural biology of the tumor suppressor p53. "
     "Annu Rev Biochem 77:557–582 (revisión).",
     "10.1146/annurev.biochem.77.060806.091238", None),
    ("Estabilidad termodinámica (ΔΔG, Tm)",
     "Boeckler FM, Joerger AC, Jaggi G, Rutherford TJ, Veprintsev DB, Fersht AR (2008). "
     "Targeted rescue of a destabilized mutant of p53 by an in silico screened drug "
     "(Y220C; cavidad y ΔΔG). PNAS 105:10360–10365.", "10.1073/pnas.0805326105", None),
    ("Estabilidad termodinámica (ΔΔG, Tm)",
     "Mavridi D, Funk JS, Balourdas D-I, Krämer A, Khan Tareque R, Timofeev O, et al. "
     "(2026). Targeting the p53 cancer mutants Y220C, Y220N, and Y220S with the "
     "small-molecule stabilizer rezatapopt (ΔTm de Y220C). Cell Death Dis 17:268.",
     "10.1038/s41419-026-08492-9", None),

    ("Escalas fisicoquímicas de aminoácidos",
     "Kyte J, Doolittle RF (1982). A simple method for displaying the hydropathic "
     "character of a protein. J Mol Biol 157:105–132 (hidrofobicidad).",
     "10.1016/0022-2836(82)90515-0", None),
    ("Escalas fisicoquímicas de aminoácidos",
     "Zamyatnin AA (1972). Protein volume in solution. Prog Biophys Mol Biol "
     "24:107–123 (volúmenes molares).", "10.1016/0079-6107(72)90005-3", None),

    ("Predictores de patogenicidad",
     "Cheng J et al. (2023). Accurate proteome-wide missense variant effect "
     "prediction with AlphaMissense. Science 381:eadg7492.", "10.1126/science.adg7492",
     None),
    ("Predictores de patogenicidad",
     "Ng PC, Henikoff S (2003). SIFT: predicting amino acid changes that affect "
     "protein function. Nucleic Acids Res 31:3812–3814.", "10.1093/nar/gkg509", None),
    ("Predictores de patogenicidad",
     "Adzhubei IA et al. (2010). A method and server for predicting damaging "
     "missense mutations (PolyPhen-2). Nature Methods 7:248–249.",
     "10.1038/nmeth0410-248", None),

    ("Unión al ADN y dependencia de temperatura",
     "Friedlander P, Legros Y, Soussi T, Prives C (1996). Regulation of mutant p53 "
     "temperature-sensitive DNA binding. J Biol Chem 271:25468–25478.",
     "10.1074/jbc.271.41.25468", None),

    ("Síndromes hereditarios y ganancia/pérdida de función",
     "Li FP, Fraumeni JF Jr (1969). Soft-tissue sarcomas, breast cancer, and other "
     "neoplasms: a familial syndrome? Ann Intern Med 71:747–752.",
     "10.7326/0003-4819-71-4-747", None),
    ("Síndromes hereditarios y ganancia/pérdida de función",
     "Muller PAJ, Vousden KH (2014). Mutant p53 in cancer: new functions and "
     "therapeutic opportunities. Cancer Cell 25:304–317 (efecto dominante negativo "
     "y ganancia de función).", "10.1016/j.ccr.2014.01.021", None),
]

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
hero(
    "Glosario y referencias",
    "Los términos clave y las fuentes que sostienen cada dato de la aplicación",
    "Todos los datos biológicos provienen de fuentes públicas verificadas. Todos los "
    "DOIs de esta página fueron confirmados directamente en CrossRef.",
)

# ---------------------------------------------------------------------------
# Glosario
# ---------------------------------------------------------------------------
seccion("Glosario")
# El HTML debe ir SIN saltos de línea ni indentación: Streamlit-markdown
# interpretaría las líneas indentadas como bloque de código y mostraría el
# HTML crudo en pantalla.
_items = "".join(
    f'<div style="padding:0.5rem 0;border-bottom:1px solid #eef1f4;">'
    f'<div style="font-family:Georgia,serif;font-weight:600;color:#1f3a5f;'
    f'font-size:1rem;">{termino}</div>'
    f'<div style="font-size:0.92rem;color:#33465c;margin-top:0.15rem;">{definicion}</div>'
    f'</div>'
    for termino, definicion in GLOSARIO
)
st.markdown(f'<div>{_items}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Referencias
# ---------------------------------------------------------------------------
seccion("Referencias")
st.caption("Agrupadas por tipo de dato. Haz clic en el DOI o el enlace para ir a la fuente.")

_categoria_actual = None
for categoria, cita, doi, url in REFERENCIAS:
    if categoria != _categoria_actual:
        st.markdown(
            f'<div style="font-family:Georgia,serif; font-weight:600; color:#1f3a5f; '
            f'margin:0.9rem 0 0.3rem; font-size:1.02rem;">{categoria}</div>',
            unsafe_allow_html=True,
        )
        _categoria_actual = categoria
    enlace = ""
    if doi:
        enlace = f" · [doi:{doi}](https://doi.org/{doi})"
    elif url:
        enlace = f" · [enlace]({url})"
    st.markdown(f"- {cita}{enlace}")

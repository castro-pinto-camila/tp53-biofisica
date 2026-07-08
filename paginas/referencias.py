# -*- coding: utf-8 -*-
"""
Página: Glosario y referencias.

Glosario de términos clave y lista de fuentes con DOI. Todos los DOIs fueron
verificados; los que no se pudieron confirmar se marcan explícitamente.
"""

import streamlit as st

from estilos import seccion

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
     "mayor afinidad. El tipo salvaje ≈ 7 nM."),
    ("ΔΔG",
     "Cuánto desestabiliza una mutación el plegamiento, en kcal/mol, respecto al tipo "
     "salvaje. Mayor ΔΔG = pliegue más débil."),
    ("Tm (temperatura de fusión)",
     "Temperatura a la que la mitad de la proteína está desplegada. El DBD de p53 "
     "tiene Tm ≈ 43 °C, apenas por encima de los 37 °C corporales."),
    ("Hidrofobicidad (escala Kyte–Doolittle)",
     "Tendencia de un aminoácido a evitar el agua. Valores altos = más hidrofóbico."),
    ("Volumen molecular (escala Zamyatnin)",
     "Tamaño del aminoácido en ų; cambios grandes causan choques estéricos o cavidades."),
    ("Polaridad",
     "Si la cadena lateral es polar (interactúa con agua y cargas) o no polar."),
    ("Conservación evolutiva",
     "Qué tanto se mantiene un residuo entre especies; los conservados suelen ser "
     "funcionalmente críticos."),
    ("Ganancia de función (GOF)",
     "Cuando la p53 mutante adquiere actividades oncogénicas nuevas, más allá de "
     "perder su función supresora."),
    ("Índice de impacto biofísico",
     "Nuestro puntaje heurístico (0–14) que combina los cambios fisicoquímicos y la "
     "localización. Es didáctico, no un predictor clínico."),
    ("Síndrome de Li-Fraumeni",
     "Predisposición hereditaria a múltiples cánceres, causada por mutaciones "
     "germinales en TP53."),
    ("AlphaMissense / SIFT / PolyPhen",
     "Predictores computacionales de patogenicidad de variantes; AlphaMissense usa "
     "aprendizaje profundo."),
    ("IARC / ClinVar / UniProt / Pfam",
     "Bases de datos públicas de mutaciones tumorales, variantes clínicas, "
     "secuencias/proteínas y dominios, respectivamente."),
]

# (categoría, cita, doi_o_None, url_o_None)
REFERENCIAS = [
    ("Bases de datos y fuentes de datos",
     "IARC TP53 Database (versión R21, enero 2025). Base de datos de mutaciones "
     "somáticas y germinales de TP53.", None, "https://tp53.isb-cgc.org/"),
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
     "Annu Rev Biochem 77:557–582 (revisión).", None, None),

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

    ("Unión al ADN y dependencia de temperatura",
     "Barakat K et al. (2011); datos de microarray de unión al ADN de p53 y "
     "comportamiento dependiente de temperatura de R248W. (DOI por verificar.)",
     None, None),
]

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-title">Glosario y referencias</div>
    <div class="hero-sub">Los términos clave y las fuentes que sostienen cada dato
    de la aplicación</div>
    <div class="hero-note">
      Todos los datos biológicos provienen de fuentes públicas verificadas. Los DOIs
      de esta página fueron confirmados; el único sin confirmar está marcado
      explícitamente como «DOI por verificar».
    </div>
    """,
    unsafe_allow_html=True,
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

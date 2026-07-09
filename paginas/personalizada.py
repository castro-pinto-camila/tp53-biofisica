# -*- coding: utf-8 -*-
"""
Página: Laboratorio de mutaciones (mutación personalizada).

Permite elegir CUALQUIER posición de p53 y CUALQUIER aminoácido de sustitución;
el motor calcula en vivo los cambios fisicoquímicos y el índice heurístico. Para
posiciones fuera de las 4 hotspot catalogadas NO hay datos clínicos ni ΔΔG medido:
se muestra únicamente el análisis fisicoquímico, claramente rotulado.
"""

import plotly.graph_objects as go
import streamlit as st

from biofisica import (
    AMINOACIDOS,
    TRES_A_UNA,
    cargar_gen,
    cargar_dominios,
    cargar_mutaciones,
    aa_tres_en_posicion,
    dominio_en_posicion,
    mutacion_catalogada,
    calcular_cambios,
    calcular_impacto,
    generar_interpretacion,
    SCORE_MAXIMO,
)
from estilos import seccion

gen = cargar_gen()
LARGO = gen["longitud_aa"]

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-title">Laboratorio de mutaciones</div>
    <div class="hero-sub">Elige cualquier posición y cualquier sustitución: el motor
    calcula el impacto fisicoquímico en vivo</div>
    <div class="hero-note">
      Esto es la parte <b>biofísica</b> del análisis, calculada para cualquier mutación.
      Para posiciones fuera de las 4 hotspot catalogadas <b>no hay datos clínicos ni ΔΔG
      medido</b>: solo el cambio fisicoquímico y el índice heurístico, que es orientativo
      y no un predictor.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Nota didáctica: tipos de mutación (por qué el lab hace solo "missense")
# ---------------------------------------------------------------------------
with st.expander("¿Qué tipos de mutación existen? (y por qué este lab hace solo «missense»)"):
    st.markdown(
        "Las mutaciones puntuales se clasifican por **qué le hacen a la proteína**. "
        "Tomando el codón de la **Arginina (CGG)** como ejemplo:"
    )
    st.markdown(
        "| Tipo | Qué pasa | Ejemplo |\n"
        "|---|---|---|\n"
        "| **Sinónima** (silenciosa) | Cambia el ADN pero sigue codificando el **mismo** "
        "aminoácido | CGG → CG**A** = sigue siendo Arg |\n"
        "| **Missense** (no sinónima) | Cambia a un **aminoácido distinto** | CGG → **T**GG "
        "= ahora Trp (¡esto es R248W!) |\n"
        "| **Nonsense** (sin sentido) | Aparece un codón **STOP** y la proteína se **corta** "
        "| CGA → **T**GA = STOP |"
    )
    st.markdown(
        "Este laboratorio trabaja con **aminoácidos, no con codones**, así que solo "
        "representa mutaciones **missense** (cambiar un aminoácido por otro) — que es "
        "justo lo que importa para el impacto **biofísico**. Una mutación *sinónima* no "
        "cambia el aminoácido (aquí se vería como «sin cambio»), y una *nonsense* corta "
        "la proteína en vez de alterar una propiedad fisicoquímica; por eso ambas quedan "
        "fuera del alcance de esta herramienta."
    )
    st.caption(
        "«Sinónima» y «silenciosa» son el mismo tipo. Nota: incluso una mutación "
        "sinónima puede, en casos puntuales, afectar el corte del ARN o la velocidad de "
        "traducción — pero como regla general no cambia la proteína."
    )

# ---------------------------------------------------------------------------
# Controles
# ---------------------------------------------------------------------------
seccion("Diseña tu mutación")

col_pos, col_aa = st.columns([2, 1])
with col_pos:
    posicion = st.slider("Posición en la proteína (1-393)", 1, LARGO, 175)
with col_aa:
    aa_orig = aa_tres_en_posicion(posicion)
    codigos = sorted(AMINOACIDOS.keys())
    idx_def = codigos.index("His") if aa_orig != "His" else codigos.index("Ala")
    aa_mut = st.selectbox(
        "Sustituir por",
        codigos,
        index=idx_def,
        format_func=lambda c: f"{c} ({TRES_A_UNA[c]})",
    )

dom_clave, dom_info = dominio_en_posicion(posicion)
dom_txt = dom_info.get("nombre", "fuera de dominios anotados")

st.markdown(
    f"""
    <div style="font-size:0.95rem;color:#33465c;margin:0.3rem 0 0.2rem;">
      Residuo original en la posición {posicion}: <b>{aa_orig} ({TRES_A_UNA.get(aa_orig,'?')})</b>
      &nbsp;·&nbsp; localización: <b>{dom_txt}</b>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Mapa lineal con el marcador de posición ---
colores_dominio = {"union_ADN": "#a23b3b", "oligomerizacion": "#2c6b8f", "regulador": "#8a6a12"}
fig_map = go.Figure()
fig_map.add_shape(type="rect", x0=1, x1=LARGO, y0=0, y1=1,
                  fillcolor="#eef0f3", line=dict(width=0), layer="below")
for clave, d in cargar_dominios().items():
    fig_map.add_shape(type="rect", x0=d["inicio"], x1=d["fin"], y0=0, y1=1,
                      fillcolor=colores_dominio.get(clave, "#9aa0a6"),
                      opacity=0.85, line=dict(width=0))
fig_map.add_shape(type="line", x0=posicion, x1=posicion, y0=-0.35, y1=1.35,
                  line=dict(color="#1a1a1a", width=2))
fig_map.add_annotation(x=posicion, y=1.7, text=f"{aa_orig}{posicion}{aa_mut}",
                       showarrow=False,
                       font=dict(size=12, family="Georgia, serif", color="#1a1a1a"))
fig_map.update_xaxes(range=[1, LARGO], title="Posición (aminoácido)", showgrid=False)
fig_map.update_yaxes(visible=False, range=[-0.6, 2.0])
fig_map.update_layout(height=160, template="simple_white",
                      margin=dict(t=20, b=30, l=20, r=20),
                      font=dict(family="Georgia, serif", color="#33465c"))
st.plotly_chart(fig_map, width="stretch")

# ---------------------------------------------------------------------------
# Resultado
# ---------------------------------------------------------------------------
if aa_mut == aa_orig:
    st.info("El aminoácido elegido es el mismo que el original: no hay mutación. "
            "Elige un aminoácido distinto para ver el análisis.")
    st.stop()

# Aviso si coincide con una mutación catalogada
catalogada = mutacion_catalogada(posicion, aa_mut)

# El flag `conservado` es una propiedad de la POSICIÓN, no de la sustitución.
# Solo lo tenemos curado para las 4 hotspot: si la mutación elegida coincide con
# una de ellas, usamos su valor real para que el score sea IDÉNTICO al del
# Evaluador (antes el Laboratorio fijaba conservado=False y daba un score
# distinto para la misma mutación). Para posiciones sin dato, queda False y se
# advierte abajo en el pie.
if catalogada:
    conservado = cargar_mutaciones()[catalogada]["conservado"]
else:
    conservado = False

cambios = calcular_cambios(aa_orig, aa_mut)
nivel, score = calcular_impacto(cambios, dom_clave, conservado=conservado)
if catalogada:
    st.success(
        f"Esta mutación coincide con **{catalogada}**, una de las 4 hotspot catalogadas. "
        f"En la página «Evaluador de mutaciones» encontrarás su evidencia clínica, ΔΔG "
        f"medido y mecanismo verificados."
    )

seccion("Impacto fisicoquímico calculado")

_COLORES_NIVEL = {
    "Bajo": ("#e8f0ea", "#2f6a44", "#cfe0d4"),
    "Moderado": ("#f6efdd", "#8a6a12", "#e6d7ad"),
    "Alto": ("#f4e6e6", "#8f2f2f", "#e3c9c9"),
}
_bg, _fg, _br = _COLORES_NIVEL.get(nivel, ("#eef0f3", "#333", "#ddd"))
st.markdown(
    f"""
    <div class="impact-badge" style="background:{_bg};color:{_fg};border:1px solid {_br};">
      {aa_orig}{posicion}{aa_mut} &nbsp;·&nbsp; Índice heurístico: <b>{nivel}</b>
      &nbsp;·&nbsp; {score} / {SCORE_MAXIMO}
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Gráfica de deltas ---
etiquetas = ["Δ Carga", "Δ Hidrofobicidad (K–D)", "Δ Volumen (Å³)"]
valores = [cambios["delta_carga"], cambios["delta_hidrofobicidad"], cambios["delta_volumen"]]


def _color(v):
    if v > 0:
        return "#a23b3b"
    if v < 0:
        return "#2a6f7f"
    return "#9aa0a6"


fig = go.Figure(go.Bar(
    x=etiquetas, y=valores, marker_color=[_color(v) for v in valores],
    marker_line_color="#33465c", marker_line_width=1,
    text=[f"{v:+.2f}" for v in valores], textposition="outside",
))
fig.update_layout(
    template="simple_white", height=360, margin=dict(t=30, b=20, l=20, r=20),
    yaxis_title="Δ (mutado − original)",
    font=dict(family="Georgia, serif", color="#33465c"), showlegend=False,
)
fig.add_hline(y=0, line_color="#c3ccd6", line_width=1)
st.plotly_chart(fig, width="stretch")

# --- Polaridad ---
if cambios["cambia_polaridad"]:
    st.markdown(
        f"""
        <div class="callout" style="background:#f6efdd;border-left:4px solid #b07d1a;">
          <div class="callout-t" style="color:#8a6a12;">Cambio de polaridad</div>
          El residuo pasa de <b>{cambios['polaridad_original']}</b> a
          <b>{cambios['polaridad_mutada']}</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"""
        <div class="callout" style="background:#f2f5f8;border-left:4px solid #9aa7b4;">
          <div class="callout-t" style="color:#4a5560;">Polaridad conservada</div>
          El residuo mantiene su carácter <b>{cambios['polaridad_original']}</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

# --- Interpretación automática ---
seccion("Interpretación biofísica")
resultado = {
    "cambios": cambios,
    "dominio_clave": dom_clave,
    "dominio_info": dom_info,
    "dne": "",
}
st.write(generar_interpretacion(resultado))
if dom_info.get("relevancia"):
    st.caption(f"Relevancia del dominio ({dom_txt}): {dom_info['relevancia']}")
st.caption(
    "Análisis fisicoquímico automático (herramienta didáctica). El índice heurístico "
    "no incluye conservación evolutiva ni estabilidad del pliegue, así que subestima o "
    "sobreestima según el caso — como se ve en la página de comparación."
)

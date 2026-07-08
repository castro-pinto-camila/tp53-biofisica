# -*- coding: utf-8 -*-
"""
Página: Evaluador de Impacto Biofísico de Mutaciones en TP53 (p53).

Herramienta DIDÁCTICA de interpretación heurística: explica el mecanismo biofísico
por el que una mutación altera la función de p53. No es un predictor clínico
(SIFT / PolyPhen / AlphaMissense).
"""

import os

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from biofisica import (
    cargar_mutaciones,
    cargar_gen,
    interpretar_mutacion,
    generar_interpretacion,
    generar_implicancias,
    generar_texto_estabilidad,
    generar_texto_temperatura,
    fraccion_plegada,
)
from grafo import construir_grafo
from estilos import seccion

# ---------------------------------------------------------------------------
# 1. Encabezado
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-title">Evaluador de Impacto Biofísico de Mutaciones en TP53</div>
    <div class="hero-sub">Del genotipo al mecanismo: por qué una mutación puntual
    altera a la proteína supresora tumoral p53</div>
    <div class="hero-note">
      Herramienta <b>didáctica</b> de interpretación heurística basada en principios
      fisicoquímicos. No es un predictor clínico (SIFT / PolyPhen / AlphaMissense).
      Datos verificados en IARC (R21, ene. 2025), ClinVar y UniProt / Pfam.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 2. Selección de mutación mediante botones con diseño
# ---------------------------------------------------------------------------
mutaciones = cargar_mutaciones()
opciones = list(mutaciones.keys())

if "mutacion_sel" not in st.session_state:
    st.session_state.mutacion_sel = opciones[0]

seccion("Selección de mutación")
st.caption("Elige una mutación hotspot de TP53 para analizar su mecanismo biofísico.")

cols_btn = st.columns(len(opciones))
for col, nombre in zip(cols_btn, opciones):
    m = mutaciones[nombre]
    etiqueta = f"{nombre}\n{m['aa_original']}{m['posicion']}{m['aa_mutado']}"
    activo = st.session_state.mutacion_sel == nombre
    with col:
        if st.button(
            etiqueta,
            key=f"btn_{nombre}",
            type="primary" if activo else "secondary",
            use_container_width=True,
        ):
            st.session_state.mutacion_sel = nombre
            # Sin este rerun explicito, el color del boton (calculado arriba
            # con el estado ANTERIOR al clic) queda "un clic atrasado"
            # respecto al contenido, que si usa el estado ya actualizado.
            st.rerun()

seleccion = st.session_state.mutacion_sel
r = interpretar_mutacion(seleccion)

# --- Etiqueta de impacto ---
_COLORES_NIVEL = {
    "Bajo":     ("#e8f0ea", "#2f6a44", "#cfe0d4"),
    "Moderado": ("#f6efdd", "#8a6a12", "#e6d7ad"),
    "Alto":     ("#f4e6e6", "#8f2f2f", "#e3c9c9"),
}
_bg, _fg, _br = _COLORES_NIVEL.get(r["nivel_impacto"], ("#eef0f3", "#333", "#ddd"))
st.markdown(
    f"""
    <div style="margin-top:0.6rem;">
      <div class="impact-badge" style="background:{_bg};color:{_fg};border:1px solid {_br};">
        Índice de impacto biofísico: <b>{r['nivel_impacto']}</b>
        &nbsp;·&nbsp; {r['score_impacto']} / 14
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 3. Tres tarjetas: cambio de aminoácido / localización / evidencia clínica
# ---------------------------------------------------------------------------
seccion("Panorama de la mutación")

info = r.get("dominio_info", {})
cambios = r["cambios"]

# Etiqueta DNE para la primera tarjeta
dne = str(r.get("dne", "")).lower()
if dne == "yes":
    dne_tag = '<div class="tag" style="background:#f4e6e6;color:#8f2f2f;">Efecto dominante negativo: Sí</div>'
elif dne == "moderate":
    dne_tag = '<div class="tag" style="background:#f6efdd;color:#8a6a12;">Efecto dominante negativo: Moderado</div>'
else:
    dne_tag = '<div class="tag" style="background:#eef0f3;color:#5a6570;">Efecto dominante negativo: No</div>'

gof_row = ""
if r.get("gof") and r["gof"] != "No reportado":
    gof_row = f'<div class="kv"><span>Ganancia de función</span><b>{r["gof"]}</b></div>'

card_aa = f"""
<div class="acard">
  <div class="acard-h">Cambio de aminoácido</div>
  <div class="kv"><span>Original</span><b>{r['aa_original']}</b></div>
  <div class="kv"><span>Mutado</span><b>{r['aa_mutado']}</b></div>
  <div class="kv"><span>Posición</span><b>{r['posicion']}</b></div>
  <div class="kv"><span>Tipo de efecto</span><b>{r['tipo_efecto']}</b></div>
  {gof_row}
  {dne_tag}
</div>
"""

rango = ""
if info.get("inicio") and info.get("fin"):
    rango = f'<div class="kv"><span>Rango</span><b>residuos {info["inicio"]}–{info["fin"]}</b></div>'

card_loc = f"""
<div class="acard">
  <div class="acard-h">Localización funcional</div>
  <div class="kv"><span>Dominio</span><b>{info.get('nombre', r['dominio_clave'])}</b></div>
  {rango}
  <div class="kv"><span>Fuente</span><b>{info.get('fuente', '—')}</b></div>
  <div class="acard-note"><b>Relevancia biofísica.</b> {info.get('relevancia', '—')}</div>
</div>
"""

card_clin = f"""
<div class="acard">
  <div class="acard-h">Evidencia clínica</div>
  <div class="kv"><span>Enfermedad</span><b>{r['enfermedad']}</b></div>
  <div class="kv"><span>Casos en IARC</span><b>{r['casos_iarc']}</b></div>
  <div class="kv"><span>ClinVar germinal</span><b>{r['clinvar_germinal']}</b></div>
  <div class="kv"><span>ClinVar somático</span><b>{r.get('clinvar_somatico', 'por verificar')}</b></div>
</div>
"""

c1, c2, c3 = st.columns(3)
c1.markdown(card_aa, unsafe_allow_html=True)
c2.markdown(card_loc, unsafe_allow_html=True)
c3.markdown(card_clin, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 4. Gráfica de barras con los 3 deltas
# ---------------------------------------------------------------------------
seccion("Cambios fisicoquímicos (mutado − original)")

etiquetas = ["Δ Carga", "Δ Hidrofobicidad (K–D)", "Δ Volumen (Å³)"]
valores = [
    cambios["delta_carga"],
    cambios["delta_hidrofobicidad"],
    cambios["delta_volumen"],
]


def _color(v):
    if v > 0:
        return "#a23b3b"   # brick (aumento)
    if v < 0:
        return "#2a6f7f"   # teal (disminución)
    return "#9aa0a6"       # gris (sin cambio)


fig = go.Figure(
    go.Bar(
        x=etiquetas,
        y=valores,
        marker_color=[_color(v) for v in valores],
        marker_line_color="#33465c",
        marker_line_width=1,
        text=[f"{v:+.2f}" for v in valores],
        textposition="outside",
    )
)
fig.update_layout(
    template="simple_white",
    height=380,
    margin=dict(t=30, b=20, l=20, r=20),
    yaxis_title="Δ (mutado − original)",
    font=dict(family="Georgia, serif", color="#33465c"),
    showlegend=False,
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
          <b>{cambios['polaridad_mutada']}</b>, lo que altera el tipo de interacciones
          que puede establecer en su entorno.
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

# ---------------------------------------------------------------------------
# 5. Interpretación biofísica
# ---------------------------------------------------------------------------
seccion("Interpretación biofísica")
st.write(generar_interpretacion(r))
st.caption(
    "Texto generado automáticamente a partir de los cambios fisicoquímicos. "
    "Herramienta didáctica de interpretación heurística; no reemplaza un análisis "
    "clínico ni un predictor validado."
)

# ---------------------------------------------------------------------------
# 6. Mecanismo de pérdida de afinidad al ADN (sección distintiva)
# ---------------------------------------------------------------------------
seccion("Mecanismo de pérdida de afinidad al ADN")

afinidad = r.get("afinidad_ADN", {})
clasif = afinidad.get("clasificacion", "")

if clasif == "contact":
    st.markdown(
        """
        <div class="callout" style="background:#f4e6e6;border-left:4px solid #a23b3b;">
          <div class="callout-t" style="color:#8f2f2f;">Mecanismo de CONTACTO</div>
          El residuo tocaba directamente el ADN. El pliegue se conserva, pero se pierde
          el contacto químico específico que sostiene la unión.
        </div>
        """,
        unsafe_allow_html=True,
    )
elif clasif == "structural":
    st.markdown(
        """
        <div class="callout" style="background:#f6efdd;border-left:4px solid #b07d1a;">
          <div class="callout-t" style="color:#8a6a12;">Mecanismo ESTRUCTURAL</div>
          El residuo no contacta el ADN, pero sostiene el pliegue del dominio. Su
          mutación desestabiliza la estructura y, con ella, la capacidad de unir ADN.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.info("Mecanismo: por verificar.")

ca, cb = st.columns(2)
ca.markdown(f"**Afinidad de referencia (Kd):** {afinidad.get('kd_wt', '—')}")
cb.markdown(f"**Clasificación:** {clasif.upper() if clasif else 'por verificar'}")
st.markdown(f"**Efecto del mutante.** {afinidad.get('efecto_mutante', '—')}")
st.caption(f"Referencia: {afinidad.get('referencia', '—')}")

# ---------------------------------------------------------------------------
# 6-bis. Estabilidad termodinámica del pliegue (ΔΔG) — dato medido
# ---------------------------------------------------------------------------
est = r.get("estabilidad", {})
ddg = est.get("ddG_kcal_mol")
if ddg is not None:
    seccion("Estabilidad termodinámica del pliegue (ΔΔG)")

    prec = est.get("ddG_precision", "")
    signo = "&gt;" if prec == "límite inferior" else "≈"
    if ddg >= 3:
        _b, _f, _r = "#f4e6e6", "#8f2f2f", "#e3c9c9"
    elif ddg >= 2:
        _b, _f, _r = "#f6efdd", "#8a6a12", "#e6d7ad"
    else:
        _b, _f, _r = "#eaf0f5", "#33597a", "#cbdae6"

    tm_mut = est.get("tm_celsius")
    tm_html = (
        f'<div style="font-size:0.82rem;margin-top:0.45rem;">Tm mutante: <b>{tm_mut} °C</b></div>'
        if tm_mut else ""
    )

    col_ddg, col_txt = st.columns([1, 2.3])
    with col_ddg:
        st.markdown(
            f"""
            <div style="background:{_b};border:1px solid {_r};border-radius:8px;
                 padding:1rem 0.8rem;text-align:center;color:{_f};">
              <div style="font-family:Georgia,serif;font-size:0.88rem;">Desestabilización del pliegue</div>
              <div style="font-family:Georgia,serif;font-size:1.9rem;font-weight:700;margin:0.15rem 0;">
                {signo} {ddg:.0f}<span style="font-size:0.95rem;"> kcal/mol</span></div>
              <div style="font-size:0.78rem;">({prec})</div>
              {tm_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_txt:
        st.write(generar_texto_estabilidad(r))

    _fuente_ddg = est.get("ddG_fuente", "—")
    _cap = f"Fuente ΔΔG: {_fuente_ddg}"
    if tm_mut:
        _cap += f" · Fuente Tm: {est.get('tm_fuente', '—')}"
    st.caption(_cap)

# ---------------------------------------------------------------------------
# 6-ter. Estabilidad frente a la temperatura (curva de plegamiento)
# ---------------------------------------------------------------------------
_wt_est = cargar_gen().get("estabilidad_wt", {})
tm_wt = _wt_est.get("tm_celsius")
if tm_wt is not None and ddg is not None:
    seccion("Estabilidad frente a la temperatura")

    # Callout: rojo si es la historia estrella (dependencia de temperatura de
    # contacto, R248W); gris neutro para el resto.
    if r.get("dependencia_temperatura"):
        _bt, _ft = "#f4e6e6", "#8f2f2f"
    else:
        _bt, _ft = "#f2f5f8", "#4a5560"
    st.markdown(
        f"""
        <div class="callout" style="background:{_bt};border-left:4px solid {_ft};">
          <div class="callout-t" style="color:{_ft};">¿Por qué importa la temperatura?</div>
          {generar_texto_temperatura(r)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    _temps = [20 + 0.25 * i for i in range(0, 121)]  # 20 → 50 °C
    fig_temp = go.Figure()
    fig_temp.add_trace(go.Scatter(
        x=_temps, y=[fraccion_plegada(t, tm_wt) for t in _temps],
        mode="lines", name=f"Tipo salvaje (Tm {tm_wt} °C)",
        line=dict(color="#2c6b8f", width=3),
    ))
    tm_mut_curva = est.get("tm_celsius")
    if tm_mut_curva is not None:
        fig_temp.add_trace(go.Scatter(
            x=_temps, y=[fraccion_plegada(t, tm_mut_curva) for t in _temps],
            mode="lines", name=f"{r['nombre']} (Tm {tm_mut_curva} °C)",
            line=dict(color="#a23b3b", width=3),
        ))
    fig_temp.add_vline(
        x=37, line_color="#33465c", line_dash="dot", line_width=2,
        annotation_text="37 °C (cuerpo)", annotation_position="top",
    )
    fig_temp.add_annotation(x=22.5, y=0.5, text="plegado<br>une ADN", showarrow=False,
                            font=dict(size=11, color="#2f6a44"), align="center")
    fig_temp.add_annotation(x=48.5, y=0.5, text="desplegado<br>no une", showarrow=False,
                            font=dict(size=11, color="#8f2f2f"), align="center")
    fig_temp.update_layout(
        template="simple_white", height=380,
        font=dict(family="Georgia, serif", color="#33465c"),
        margin=dict(t=30, b=20, l=20, r=20),
        xaxis_title="Temperatura (°C)", yaxis_title="Fracción plegada (modelo)",
        yaxis=dict(range=[-0.05, 1.12]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig_temp, width="stretch")
    st.caption(
        "Curvas de plegamiento modeladas (transición de dos estados) centradas en el "
        "Tm MEDIDO de cada proteína. Ilustran el margen de estabilidad frente a la "
        "temperatura corporal, no la fracción exacta unida al ADN. Tm por DSF (Life 2023)."
    )

# ---------------------------------------------------------------------------
# 7. ¿Por qué importa esto? — implicancias
# ---------------------------------------------------------------------------
seccion("¿Por qué importa esto?")
for titulo, texto in generar_implicancias(r):
    with st.expander(titulo):
        st.write(texto)

# ---------------------------------------------------------------------------
# 8. Red de mutaciones y tipos de cáncer
# ---------------------------------------------------------------------------
seccion("Red de mutaciones y tipos de cáncer")
st.caption(
    "Nodos rojos: mutaciones. Nodos azules: tipos de cáncer (columna Topography de "
    "IARC). Arrastra los nodos para reorganizar la red. Usa los botones de la "
    "esquina inferior izquierda del grafo para acercar, alejar o volver a la "
    "vista original."
)
try:
    ruta_grafo = construir_grafo()
    with open(ruta_grafo, "r", encoding="utf-8") as f:
        html_grafo = f.read()
    components.html(html_grafo, height=670, scrolling=True)
    try:
        os.remove(ruta_grafo)
    except OSError:
        pass
except Exception as exc:  # noqa: BLE001
    st.info("No se pudo renderizar el grafo (¿está instalado pyvis?). Detalle: %s" % exc)

# ---------------------------------------------------------------------------
# 9. Visualización 3D interactiva (3Dmol.js sobre la estructura 1TUP)
# ---------------------------------------------------------------------------
seccion("Estructura tridimensional (interactiva)")
_es_contacto = afinidad.get("clasificacion") == "contact"
st.caption(
    ("Arrastra para rotar y usa la rueda para acercar. Proteína en gris, ADN en "
     "naranja, zinc estructural en gris oscuro, y el residuo %s%d resaltado en rojo. "
     % (r["aa_original"], r["posicion"]))
    + ("Fíjate cómo el residuo se asoma hacia el ADN: es un defecto de CONTACTO."
       if _es_contacto else
       "Fíjate cómo el residuo queda dentro del cuerpo de la proteína, lejos del ADN: "
       "su papel es ESTRUCTURAL (sostiene el pliegue).")
)
try:
    from estructura3d import generar_html_3d
    components.html(generar_html_3d(r["posicion"], r["nombre"],
                                    afinidad.get("clasificacion", "")),
                    height=520, scrolling=False)
    st.caption(
        "Estructura: PDB 1TUP (Cho et al. 1994, Science 265:346). Visor 3Dmol.js "
        "embebido; funciona sin conexión."
    )
except Exception as exc:  # noqa: BLE001
    st.info("No se pudo cargar el visor 3D. Detalle: %s" % exc)

# -*- coding: utf-8 -*-
"""
Página: Comparar mutaciones.

Pone lado a lado las 4 mutaciones ya analizadas individualmente en el evaluador:
cambios fisicoquímicos, índice de impacto y tipos de cáncer asociados. La
comparación de cáncer es descriptiva (co-ocurrencia registrada en IARC) — no se
afirma una relación causal entre el cambio fisicoquímico y el tipo de cáncer.
"""

import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from biofisica import cargar_mutaciones, interpretar_mutacion, SCORE_MAXIMO
from estilos import seccion

mutaciones = cargar_mutaciones()
opciones = list(mutaciones.keys())
resultados = {nombre: interpretar_mutacion(nombre) for nombre in opciones}

# Un color fijo por mutación, reutilizado en TODAS las secciones de esta
# página (gráfico, tabla y mapa de calor) para poder seguir cada mutación de
# un vistazo.
COLORES_MUT = {
    "R175H": "#1f3a5f",
    "R248W": "#a23b3b",
    "G245S": "#2c6b8f",
    "R282W": "#8a6a12",
}

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-title">Comparación de mutaciones</div>
    <div class="hero-sub">Las 4 mutaciones lado a lado: cambios fisicoquímicos,
    índice de impacto y tipos de cáncer asociados</div>
    <div class="hero-note">
      Esta página junta lo que ya viste mutación por mutación en el evaluador.
      La comparación de tipos de cáncer es <b>descriptiva</b> (co-ocurrencia
      registrada en IARC): no implica que el cambio fisicoquímico
      <i>cause</i> un tipo de cáncer en particular.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 1. Cambios fisicoquímicos — un panel por métrica (las 3 tienen escalas muy
#    distintas: la carga se mueve entre -1 y +1, el volumen entre decenas de
#    Å³; en un solo eje compartido el volumen taparía a los otros dos).
# ---------------------------------------------------------------------------
seccion("Cambios fisicoquímicos, lado a lado")
st.caption(
    "Cada panel usa su propia escala porque las unidades no son comparables entre sí."
)

METRICAS = [
    ("delta_carga", "Δ Carga"),
    ("delta_hidrofobicidad", "Δ Hidrofobicidad (K–D)"),
    ("delta_volumen", "Δ Volumen (Å³)"),
]

fig = make_subplots(rows=1, cols=3, subplot_titles=[m[1] for m in METRICAS], horizontal_spacing=0.08)
for col_idx, (clave, _) in enumerate(METRICAS, start=1):
    valores = [resultados[n]["cambios"][clave] for n in opciones]
    colores = [COLORES_MUT[n] for n in opciones]
    fig.add_trace(
        go.Bar(
            x=opciones, y=valores, marker_color=colores,
            marker_line_color="#33465c", marker_line_width=1,
            text=[f"{v:+.2f}" for v in valores], textposition="outside",
            showlegend=False,
        ),
        row=1, col=col_idx,
    )
    fig.add_hline(y=0, line_color="#c3ccd6", line_width=1, row=1, col=col_idx)

fig.update_layout(
    height=380,
    template="simple_white",
    font=dict(family="Georgia, serif", color="#33465c"),
    margin=dict(t=50, b=20, l=20, r=20),
)
fig.update_annotations(font=dict(family="Georgia, serif", size=13, color="#1f3a5f"))
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------------------------
# 2. Tabla resumen — índice de impacto y mecanismo, en una sola vista
# ---------------------------------------------------------------------------
seccion("Índice de impacto y mecanismo")

filas = ""
for nombre in opciones:
    r = resultados[nombre]
    color = COLORES_MUT[nombre]
    dominio_nombre = r["dominio_info"].get("nombre", r["dominio_clave"])
    clasif = r["afinidad_ADN"].get("clasificacion", "")
    clasif_txt = clasif.upper() if clasif else "por verificar"
    dne = str(r.get("dne", "")).lower()
    dne_txt = {"yes": "Sí", "moderate": "Moderado"}.get(dne, "No")
    est = r.get("estabilidad", {})
    ddg = est.get("ddG_kcal_mol")
    if ddg is None:
        ddg_txt = "por verificar"
    else:
        _s = "&gt;" if est.get("ddG_precision") == "límite inferior" else "≈"
        ddg_txt = f"{_s} {ddg:.0f} kcal/mol"
    filas += f"""
    <tr>
      <td><span style="display:inline-block;width:10px;height:10px;border-radius:50%;
          background:{color};margin-right:7px;"></span><b>{nombre}</b></td>
      <td>{dominio_nombre}</td>
      <td>{clasif_txt}</td>
      <td>{ddg_txt}</td>
      <td>{r['nivel_impacto']} ({r['score_impacto']} / {SCORE_MAXIMO})</td>
      <td>{dne_txt}</td>
    </tr>
    """

st.markdown(
    f"""
    <table class="tabla-comp">
      <thead>
        <tr><th>Mutación</th><th>Dominio</th><th>Mecanismo</th>
            <th>ΔΔG (pliegue)</th><th>Índice de impacto</th>
            <th>Efecto dominante negativo</th></tr>
      </thead>
      <tbody>{filas}</tbody>
    </table>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 2-bis. Estabilidad del pliegue (ΔΔG) — barras comparativas
# ---------------------------------------------------------------------------
seccion("Desestabilización del pliegue (ΔΔG), lado a lado")
st.caption(
    "Cuánto desestabiliza cada mutación el plegamiento del dominio (0 = tipo salvaje). "
    "Valores medidos/estimados de la literatura (Bullock & Fersht 1997; Joerger et al. "
    "2006); R282W es un límite inferior (> 3). Contraste clave: R175H y R282W son las "
    "más desestabilizadas pese a que su cambio químico local es leve."
)

ddg_vals, ddg_txt_bar, ddg_colores = [], [], []
for nombre in opciones:
    est = resultados[nombre].get("estabilidad", {})
    v = est.get("ddG_kcal_mol")
    ddg_vals.append(v if v is not None else 0)
    if v is None:
        ddg_txt_bar.append("s/d")
    else:
        _s = ">" if est.get("ddG_precision") == "límite inferior" else "≈"
        ddg_txt_bar.append(f"{_s}{v:.0f}")
    ddg_colores.append(COLORES_MUT[nombre])

fig_ddg = go.Figure(
    go.Bar(
        x=opciones, y=ddg_vals, marker_color=ddg_colores,
        marker_line_color="#33465c", marker_line_width=1,
        text=ddg_txt_bar, textposition="outside",
        showlegend=False,
    )
)
fig_ddg.update_layout(
    height=340, template="simple_white",
    font=dict(family="Georgia, serif", color="#33465c"),
    margin=dict(t=30, b=20, l=20, r=20),
    yaxis_title="ΔΔG desestabilización (kcal/mol)",
)
st.plotly_chart(fig_ddg, width="stretch")

# ---------------------------------------------------------------------------
# 2-ter. ¿Qué tan bien predice la heurística? — validación honesta
# ---------------------------------------------------------------------------
seccion("¿Qué tan bien predice la heurística? — validación honesta")
st.caption(
    "Nuestro índice heurístico mira solo el cambio fisicoquímico LOCAL del aminoácido. "
    "Aquí lo contrastamos contra el ΔΔG MEDIDO (la desestabilización real del pliegue). "
    "Si la heurística fuera un buen predictor de la estabilidad, los puntos caerían sobre "
    "la diagonal. Ambos ejes están normalizados 0-1 solo para poder compararlos."
)

_DDG_REF = 3.0  # kcal/mol, referencia de normalización
val_x, val_y, val_lbl, val_col = [], [], [], []
for nombre in opciones:
    r = resultados[nombre]
    ddg = r.get("estabilidad", {}).get("ddG_kcal_mol")
    if ddg is None:
        continue
    val_x.append(r["score_impacto"] / SCORE_MAXIMO)
    val_y.append(min(ddg / _DDG_REF, 1.0))
    val_lbl.append(nombre)
    val_col.append(COLORES_MUT[nombre])

fig_val = go.Figure()
fig_val.add_trace(go.Scatter(
    x=[0, 1], y=[0, 1], mode="lines",
    line=dict(color="#c3ccd6", dash="dash", width=1.5),
    name="acuerdo perfecto", hoverinfo="skip",
))
fig_val.add_trace(go.Scatter(
    x=val_x, y=val_y, mode="markers+text", text=val_lbl, textposition="top center",
    textfont=dict(family="Georgia, serif", size=12, color="#33465c"),
    marker=dict(size=18, color=val_col, line=dict(color="#33465c", width=1.5)),
    showlegend=False, hovertemplate="%{text}<extra></extra>",
))
fig_val.add_annotation(x=0.16, y=0.92, text="la heurística<br>SUBESTIMA", showarrow=False,
                       font=dict(size=11, color="#8f2f2f"), align="center")
fig_val.add_annotation(x=0.86, y=0.14, text="la heurística<br>SOBREESTIMA", showarrow=False,
                       font=dict(size=11, color="#33597a"), align="center")
fig_val.update_layout(
    template="simple_white", height=460,
    font=dict(family="Georgia, serif", color="#33465c"),
    margin=dict(t=40, b=20, l=20, r=20),
    xaxis=dict(title="Índice heurístico (normalizado)", range=[-0.05, 1.12]),
    yaxis=dict(title="ΔΔG medido (normalizado)", range=[-0.05, 1.18]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_val, width="stretch")

st.markdown(
    """
    <div class="callout" style="background:#f7f9fb;border-left:4px solid #1f3a5f;">
      <div class="callout-t" style="color:#1f3a5f;">Lo que esto revela</div>
      <b>R175H</b> queda muy por encima de la diagonal: la heurística le da un índice
      moderado porque el cambio químico local (Arg→His) es leve, pero el ΔΔG muestra que
      es de las <b>más</b> desestabilizadas — la física local no «ve» el colapso del
      pliegue. <b>R248W</b>, al contrario, queda por debajo: la heurística la puntúa muy
      alto por el gran cambio fisicoquímico, pero su ΔΔG es solo moderado porque su
      defecto real es de <b>contacto</b> con el ADN, no de plegamiento.
      <br><br>
      Por eso nos presentamos como herramienta <b>didáctica</b>, no como predictor: la
      física local simple capta los cambios químicos grandes pero se pierde la estabilidad
      del pliegue. Un predictor entrenado como <b>AlphaMissense</b> clasifica las 4 como
      <i>likely pathogenic</i> — ha aprendido el contexto estructural que a nuestra
      heurística le falta.
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(
    "ΔΔG: Bullock & Fersht 1997; Joerger et al. 2006. Clase AlphaMissense: "
    "Cheng et al. 2023, Science 381:eadg7492."
)

# ---------------------------------------------------------------------------
# 3. Tipos de cáncer asociados — mapa de calor de co-ocurrencia
# ---------------------------------------------------------------------------
seccion("Tipos de cáncer asociados")
st.caption(
    "Qué tipos de cáncer aparecen junto a cada mutación (columna Topography, IARC). "
    "Ordenado de más a menos compartido entre las 4 mutaciones. Es una comparación "
    "descriptiva de co-ocurrencia, no una relación causal."
)

cancer_todos = sorted(
    {c for m in mutaciones.values() for c in m["canceres"]},
    key=lambda c: -sum(1 for m in mutaciones.values() if c in m["canceres"]),
)
matriz = [[1 if cancer in mutaciones[n]["canceres"] else 0 for n in opciones] for cancer in cancer_todos]

fig2 = go.Figure(
    go.Heatmap(
        z=matriz, x=opciones, y=cancer_todos,
        colorscale=[[0, "#f7f9fb"], [1, "#a23b3b"]],
        showscale=False, xgap=4, ygap=4,
        hovertemplate="%{y} · %{x}<extra></extra>",
    )
)
fig2.update_layout(
    height=max(280, 34 * len(cancer_todos)),
    template="simple_white",
    font=dict(family="Georgia, serif", color="#33465c"),
    margin=dict(t=20, b=20, l=20, r=20),
    yaxis=dict(autorange="reversed"),
)
st.plotly_chart(fig2, width="stretch")

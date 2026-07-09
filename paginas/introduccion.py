# -*- coding: utf-8 -*-
"""
Página: El gen TP53 — introducción explorable antes del evaluador de mutaciones.

Recorrido guiado en 4 pasos (ubicación cromosómica -> gen y proteína -> dominios
funcionales -> secuencia y mutaciones) usando datos ya verificados del proyecto
(data/gen_tp53.json, data/dominios.json, data/mutaciones.json). No se inventa
ningún valor nuevo: la secuencia proviene de UniProt P04637 y la localización
cromosómica de NCBI Gene ID 7157 (ver "fuente_secuencia" / "fuente_localizacion"
en data/gen_tp53.json).
"""

import os

import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from biofisica import cargar_gen, cargar_dominios, cargar_mutaciones
from estilos import seccion
from diagrama import SVG_DOGMA_CENTRAL
from grafo import construir_grafo

gen = cargar_gen()
dominios = cargar_dominios()
mutaciones = cargar_mutaciones()

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-title">TP53: el gen guardián del genoma</div>
    <div class="hero-sub">De un cambio de una sola letra en el ADN al mecanismo
    biofísico por el que una célula pierde su freno contra el cáncer</div>

    <div class="stat-hero">
      <span class="stat-num">~50%</span>
      <span class="stat-txt">de todos los cánceres humanos llevan una mutación en
      TP53 — es el gen más frecuentemente mutado en tumores. Esta app abre una de
      esas mutaciones y muestra <b>por qué</b> rompe la proteína.</span>
    </div>

    <div class="learn-box">
      <div class="learn-h">Qué vas a aprender</div>
      <ul>
        <li>Distinguir los dos mecanismos por los que una mutación abole la unión al
            ADN: <b>defecto de contacto</b> vs. <b>defecto estructural</b>.</li>
        <li>Leer un <b>ΔΔG</b> y entender por qué el dominio de p53 es
            «marginalmente estable»: basta perder 1–3 kcal/mol para desplegarlo a
            37 °C.</li>
        <li>Comparar una heurística fisicoquímica simple contra datos <b>medidos</b>
            y ver dónde acierta y dónde falla (rigor honesto, no caja negra).</li>
      </ul>
    </div>

    <div class="hero-note">
      <b>Empieza aquí:</b> recorre los 4 pasos de abajo (genoma → proteína →
      dominios → secuencia y mutaciones) y termina en el evaluador. Datos
      verificados en UniProt, NCBI Gene e IARC (fuentes al pie de cada sección).
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(
    "Prevalencia de TP53 en tumores: Olivier, Hollstein & Hainaut 2010, Cold Spring "
    "Harb Perspect Biol (doi:10.1101/cshperspect.a001008)."
)

# ---------------------------------------------------------------------------
# Selector de paso (recorrido guiado, mismo patrón de botones que el evaluador)
# ---------------------------------------------------------------------------
PASOS = [
    "1 · Ubicación cromosómica",
    "2 · El gen y la proteína",
    "3 · Dominios funcionales",
    "4 · Secuencia y mutaciones",
]

if "paso_intro" not in st.session_state:
    st.session_state.paso_intro = 0

seccion("Explorador del gen TP53")
cols_paso = st.columns(len(PASOS))
for i, (col, etiqueta) in enumerate(zip(cols_paso, PASOS)):
    activo = st.session_state.paso_intro == i
    with col:
        if st.button(
            etiqueta,
            key=f"paso_{i}",
            type="primary" if activo else "secondary",
            use_container_width=True,
        ):
            st.session_state.paso_intro = i
            # Sin este rerun explicito, el color del boton (calculado arriba
            # con el estado ANTERIOR al clic) queda "un clic atrasado"
            # respecto al contenido, que si usa el estado ya actualizado.
            st.rerun()

paso = st.session_state.paso_intro

# ---------------------------------------------------------------------------
# Paso 1 — Ubicación cromosómica
# ---------------------------------------------------------------------------
if paso == 0:
    col_img, col_txt = st.columns([1, 1.4])

    with col_img:
        st.markdown(
            """
            <svg viewBox="0 0 320 400" xmlns="http://www.w3.org/2000/svg"
                 style="max-width:230px; display:block; margin:0.5rem auto;">
              <rect x="110" y="20" width="46" height="110" rx="23"
                    fill="#e4e8ec" stroke="#8a97a6" stroke-width="1.5"/>
              <rect x="110" y="52" width="46" height="24" fill="#a23b3b"/>
              <path d="M110,130 Q133,150 156,130 L156,150 Q133,168 110,150 Z"
                    fill="#c7ccd2" stroke="#8a97a6" stroke-width="1.5"/>
              <rect x="110" y="150" width="46" height="210" rx="23"
                    fill="#e4e8ec" stroke="#8a97a6" stroke-width="1.5"/>
              <text x="133" y="400" text-anchor="middle" font-family="Georgia, serif"
                    font-size="15" fill="#1f3a5f" font-weight="700">Cromosoma 17</text>
              <text x="98" y="35" text-anchor="end" font-family="Georgia, serif"
                    font-size="12" fill="#4a5560">brazo p</text>
              <text x="98" y="345" text-anchor="end" font-family="Georgia, serif"
                    font-size="12" fill="#4a5560">brazo q</text>
              <line x1="156" y1="64" x2="205" y2="64" stroke="#a23b3b"
                    stroke-width="1.5" stroke-dasharray="3,3"/>
              <text x="210" y="60" font-family="Georgia, serif" font-size="13.5"
                    fill="#a23b3b" font-weight="700">17p13.1</text>
              <text x="210" y="78" font-family="Georgia, serif" font-size="12"
                    fill="#33465c">gen TP53</text>
            </svg>
            <p style="text-align:center; font-size:0.8rem; color:#6a7480;">
              Esquema ilustrativo, no a escala.
            </p>
            """,
            unsafe_allow_html=True,
        )

    with col_txt:
        st.markdown("#### ¿Dónde está el gen TP53?")
        st.markdown(
            f"""
            El gen **{gen['gen']}** se encuentra en el **cromosoma {gen['cromosoma']}**,
            en la banda citogenética **{gen['banda_citogenetica']}** — cerca del extremo
            del brazo corto (p).

            En coordenadas del ensamblaje **{gen['ensamblaje']}** ocupa la región
            **{gen['coordenadas']['inicio']:,}–{gen['coordenadas']['fin']:,}**
            (cadena {gen['coordenadas']['cadena']}) y está compuesto por
            **{gen['num_exones']} exones**.
            """
        )
        st.caption(f"Fuente: {gen['fuente_localizacion']}")

# ---------------------------------------------------------------------------
# Paso 2 — El gen y la proteína
# ---------------------------------------------------------------------------
elif paso == 1:
    col1, col2 = st.columns([1, 1.4])

    with col1:
        st.markdown(
            f"""
            <div class="acard">
              <div class="acard-h">Ficha del gen y la proteína</div>
              <div class="kv"><span>Gen</span><b>{gen['gen']}</b></div>
              <div class="kv"><span>Proteína</span><b>{gen['proteina']}</b></div>
              <div class="kv"><span>UniProt</span><b>{gen['uniprot_id']}</b></div>
              <div class="kv"><span>NCBI Gene ID</span><b>{gen['ncbi_gene_id']}</b></div>
              <div class="kv"><span>Organismo</span><b>{gen['organismo']}</b></div>
              <div class="kv"><span>Cromosoma</span><b>{gen['cromosoma']} ({gen['banda_citogenetica']})</b></div>
              <div class="kv"><span>Longitud</span><b>{gen['longitud_aa']} aminoácidos</b></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("#### ¿Qué hace la proteína p53?")
        st.markdown(gen["funcion_general"])
        st.caption(f"Fuentes: {gen['fuente_secuencia']} · {gen['fuente_localizacion']}")

    st.markdown("---")
    st.markdown("#### Cómo se produce la proteína p53")
    st.caption(
        "Igual que cualquier gen, TP53 se expresa siguiendo el dogma central: el "
        "ADN se copia a ARN y el ARN se traduce en la proteína."
    )
    # Si algún día colocas tu propia imagen en imagenes/regulacion_transcripcional.png,
    # se usa esa; si no, se muestra el diagrama SVG incorporado.
    _ruta_regulacion = os.path.join("imagenes", "regulacion_transcripcional.png")
    if os.path.exists(_ruta_regulacion):
        st.image(_ruta_regulacion, caption="Producción de la proteína p53.",
                 width="stretch")
    else:
        # st.markdown sanitiza el SVG; components.html lo dibuja de forma fiable.
        components.html(SVG_DOGMA_CENTRAL, height=470, scrolling=False)

# ---------------------------------------------------------------------------
# Paso 3 — Dominios funcionales
# ---------------------------------------------------------------------------
elif paso == 2:
    st.markdown("#### Organización en dominios funcionales")
    st.caption(
        "Mapa lineal de la proteína (393 aminoácidos). Las líneas punteadas marcan "
        "la posición de las 4 mutaciones que se analizan en el evaluador."
    )

    largo = gen["longitud_aa"]
    colores_dominio = {
        "union_ADN": "#a23b3b",
        "oligomerizacion": "#2c6b8f",
        "regulador": "#8a6a12",
    }

    fig = go.Figure()
    fig.add_shape(
        type="rect", x0=1, x1=largo, y0=0, y1=1,
        fillcolor="#eef0f3", line=dict(width=0), layer="below",
    )
    # Los dominios "oligomerizacion" (319-357) y "regulador" (364-393) quedan
    # muy juntos en la escala 1-393; se alterna la altura de cada etiqueta
    # para que no se superpongan.
    for i, (clave, d) in enumerate(dominios.items()):
        color = colores_dominio.get(clave, "#9aa0a6")
        fig.add_shape(
            type="rect", x0=d["inicio"], x1=d["fin"], y0=0, y1=1,
            fillcolor=color, opacity=0.88, line=dict(width=0),
        )
        y_etiqueta = 1.28 if i % 2 == 0 else 1.55
        centro = (d["inicio"] + d["fin"]) / 2
        fig.add_annotation(
            x=centro, y=y_etiqueta, text=d["nombre"], showarrow=False,
            font=dict(size=11, family="Georgia, serif", color="#33465c"),
        )

    # Las mutaciones G245S (245) y R248W (248) quedan a solo 3 posiciones de
    # distancia; se alterna la profundidad de cada etiqueta (orden por
    # posición) para que las líneas y el texto no se crucen.
    mutaciones_ordenadas = sorted(mutaciones.items(), key=lambda kv: kv[1]["posicion"])
    for i, (nombre, m) in enumerate(mutaciones_ordenadas):
        y_fondo = -0.4 if i % 2 == 0 else -0.65
        fig.add_shape(
            type="line", x0=m["posicion"], x1=m["posicion"], y0=y_fondo + 0.15, y1=1.15,
            line=dict(color="#1a1a1a", width=1.5, dash="dot"),
        )
        fig.add_annotation(
            x=m["posicion"], y=y_fondo, text=f"{nombre} ({m['posicion']})",
            showarrow=False, textangle=-40,
            font=dict(size=10, family="Georgia, serif", color="#33465c"),
        )

    fig.update_xaxes(range=[1, largo + 12], title="Posición (aminoácido)", showgrid=False)
    fig.update_yaxes(visible=False, range=[-0.95, 1.85])
    fig.update_layout(
        height=340,
        margin=dict(t=50, b=90, l=20, r=70),
        template="simple_white",
        font=dict(family="Georgia, serif", color="#33465c"),
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("##### Detalle de cada dominio")
    for clave, d in dominios.items():
        color = colores_dominio.get(clave, "#9aa0a6")
        st.markdown(
            f"""
            <div class="acard" style="margin-bottom:0.6rem;">
              <div class="acard-h" style="border-color:{color};">
                <span style="display:inline-block;width:10px;height:10px;
                border-radius:50%;background:{color};margin-right:6px;"></span>
                {d['nombre']} (residuos {d['inicio']}–{d['fin']})
              </div>
              <div class="acard-note">{d['relevancia']}</div>
              <div class="acard-note"><i>Fuente: {d['fuente']}</i></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------------------------
# Paso 4 — Secuencia y mutaciones
# ---------------------------------------------------------------------------
elif paso == 3:
    st.markdown("#### Secuencia completa y posiciones que pueden mutar")
    st.caption(
        "Secuencia canónica de p53 (393 aminoácidos, código de una letra). Los "
        "residuos resaltados son las 4 mutaciones hotspot que analiza el evaluador."
    )

    secuencia = gen["secuencia_aa"]
    posiciones_mut = {m["posicion"]: nombre for nombre, m in mutaciones.items()}

    partes = []
    for i, aa in enumerate(secuencia, start=1):
        if i in posiciones_mut:
            partes.append(f'<mark title="{posiciones_mut[i]} (posición {i})">{aa}</mark>')
        else:
            partes.append(aa)
        if i % 60 == 0:
            partes.append("<br>")
    secuencia_html = "".join(partes)

    st.markdown(f'<div class="secuencia-aa">{secuencia_html}</div>', unsafe_allow_html=True)
    st.caption(f"Fuente: {gen['fuente_secuencia']}")

    st.markdown("##### Mutaciones resaltadas")
    cols_leyenda = st.columns(len(mutaciones))
    for col, (nombre, m) in zip(cols_leyenda, mutaciones.items()):
        with col:
            st.markdown(
                f"""
                <div class="acard" style="min-height:auto; text-align:center; padding:0.7rem;">
                  <b style="color:#a23b3b;">{nombre}</b><br>
                  <span style="font-size:0.85rem; color:#5a6570;">
                    {m['aa_original']}{m['posicion']}{m['aa_mutado']}
                  </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --- ¿De dónde vienen estas mutaciones? ---
    st.markdown("##### ¿De dónde vienen estas mutaciones?")
    st.markdown(
        "La **mayoría** de las mutaciones en TP53 son **somáticas**: surgen durante la "
        "vida en una célula concreta y **no se heredan**. Una **minoría** son "
        "**germinales** (heredadas) y causan el **síndrome de Li-Fraumeni** — las 4 "
        "mutaciones de esta app aparecen en ambos casos. Muchos de los puntos calientes "
        "más frecuentes (R175, R248, R282) mutan tanto por un proceso **interno**: la "
        "citosina metilada de los sitios «CpG» se transforma sola, sin necesidad de un "
        "agente externo. En cambio, otras mutaciones de TP53 llevan la **firma de "
        "agentes ambientales**: la luz **UV** en cáncer de piel, el **tabaco** en "
        "pulmón, o la **aflatoxina** (un hongo de alimentos mal conservados) en cáncer "
        "de hígado."
    )
    st.caption(
        "Fuentes: Olivier, Hollstein & Hainaut 2010, Cold Spring Harb Perspect Biol "
        "(doi:10.1101/cshperspect.a001008); Baugh et al. 2018, Cell Death Differ "
        "(doi:10.1038/cdd.2017.180)."
    )

    # --- Red de mutaciones y tipos de cáncer (vista general de las 4) ---
    st.markdown("##### Red de mutaciones y tipos de cáncer")
    st.caption(
        "Nodos rojos: mutaciones. Nodos azules: tipos de cáncer (columna Topography de "
        "IARC). **Haz clic en un tipo de cáncer** para abrir su página explicativa en "
        "cancer.gov (Instituto Nacional del Cáncer, en español). Arrastra los nodos para "
        "reorganizar la red; usa los botones de la esquina inferior izquierda para "
        "acercar, alejar o volver a la vista original."
    )
    try:
        _ruta_grafo = construir_grafo()
        with open(_ruta_grafo, "r", encoding="utf-8") as _f:
            _html_grafo = _f.read()
        components.html(_html_grafo, height=670, scrolling=True)
        try:
            os.remove(_ruta_grafo)
        except OSError:
            pass
    except Exception as _exc:  # noqa: BLE001
        st.info("No se pudo renderizar el grafo. Detalle: %s" % _exc)

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_boton, _ = st.columns([1, 1.4, 1])
    with col_boton:
        if st.button("Ir al evaluador de mutaciones →", type="primary", use_container_width=True):
            st.switch_page("paginas/evaluador.py")

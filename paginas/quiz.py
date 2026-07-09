# -*- coding: utf-8 -*-
"""
Página: Quiz — «¿Contacto o estructural?».

Pequeño juego de autoevaluación que refuerza la distinción central del proyecto
(mecanismo de contacto vs. estructural) y otros conceptos biofísicos. Las
preguntas de mecanismo se generan a partir de los datos verificados de las
mutaciones; el resto son conceptuales.
"""

import random

import streamlit as st

from biofisica import cargar_mutaciones
from estilos import seccion

mutaciones = cargar_mutaciones()

# ---------------------------------------------------------------------------
# Banco de preguntas
# ---------------------------------------------------------------------------
PREGUNTAS = []
for nombre, m in mutaciones.items():
    clasif = m["afinidad_ADN"]["clasificacion"]
    correcta = "Contacto" if clasif == "contact" else "Estructural"
    PREGUNTAS.append({
        "pregunta": f"La mutación **{nombre}** ({m['aa_original']}{m['posicion']}"
                    f"{m['aa_mutado']}): ¿su defecto principal es de contacto directo "
                    f"con el ADN o estructural (desestabiliza el pliegue)?",
        "opciones": ["Contacto", "Estructural"],
        "correcta": correcta,
        "explicacion": m["afinidad_ADN"]["efecto_mutante"],
    })

PREGUNTAS.append({
    "pregunta": "¿Cuál de estas mutaciones pierde la unión al ADN por **dependencia "
                "de temperatura** (une a temperaturas bajas, pero no a 37 °C)?",
    "opciones": ["R175H", "R248W", "G245S", "R282W"],
    "correcta": "R248W",
    "explicacion": "R248W tiene un Tm de 39.3 °C, apenas por encima de los 37 °C "
                   "corporales: a temperatura fisiológica entra en su transición de "
                   "desplegamiento y pierde la unión, aunque a temperaturas más bajas sí une.",
})
PREGUNTAS.append({
    "pregunta": "El dominio de unión al ADN de p53 es «marginalmente estable»: su Tm "
                "(~43 °C) está apenas por encima de la temperatura corporal. "
                "¿Verdadero o falso?",
    "opciones": ["Verdadero", "Falso"],
    "correcta": "Verdadero",
    "explicacion": "Por eso desestabilizaciones de solo 1-3 kcal/mol bastan para "
                   "desplegar el dominio a 37 °C y abolir su función.",
})
PREGUNTAS.append({
    "pregunta": "Nuestro índice heurístico le da un impacto «Moderado» a R175H, pero el "
                "ΔΔG medido muestra que es de las más desestabilizadas. ¿Qué ilustra esto?",
    "opciones": [
        "Que la física local simple no capta el colapso del pliegue",
        "Que R175H en realidad es benigna",
        "Que el ΔΔG está mal medido",
    ],
    "correcta": "Que la física local simple no capta el colapso del pliegue",
    "explicacion": "El cambio químico local (Arg→His) es leve, pero desestabiliza mucho "
                   "el pliegue. Por eso somos una herramienta didáctica, no un predictor.",
})
PREGUNTAS.append({
    "pregunta": "El dominio de unión al ADN de p53 necesita **carga positiva** para "
                "funcionar. ¿Por qué?",
    "opciones": [
        "Atrae al esqueleto fosfato del ADN, que está cargado negativamente",
        "Repele al ADN para no unirse demasiado fuerte",
        "La carga no influye en la unión al ADN",
    ],
    "correcta": "Atrae al esqueleto fosfato del ADN, que está cargado negativamente",
    "explicacion": "Por eso perder una arginina (+1) en el dominio de unión, como en "
                   "R175H, R248W o R282W, debilita directamente el contacto proteína-ADN.",
})
PREGUNTAS.append({
    "pregunta": "¿Qué significa el **efecto dominante negativo (DNE)** de una mutación "
                "de p53?",
    "opciones": [
        "La subunidad mutante inactiva también al alelo sano dentro del tetrámero",
        "La mutación solo afecta si están mutadas las dos copias del gen",
        "La proteína mutante gana una función oncogénica nueva",
    ],
    "correcta": "La subunidad mutante inactiva también al alelo sano dentro del tetrámero",
    "explicacion": "p53 funciona como tetrámero; una subunidad mutante «envenena» el "
                   "complejo mezclándose con las normales. La última opción describe la "
                   "ganancia de función (GOF), que es un fenómeno distinto.",
})
PREGUNTAS.append({
    "pregunta": "La **mayoría** de las mutaciones de TP53 en tumores son… ",
    "opciones": ["Somáticas (no se heredan)", "Germinales (heredadas)", "Sinónimas"],
    "correcta": "Somáticas (no se heredan)",
    "explicacion": "Surgen durante la vida en una célula concreta. Una minoría son "
                   "germinales y causan el síndrome de Li-Fraumeni.",
})
PREGUNTAS.append({
    "pregunta": "El **índice de impacto biofísico** de esta app es…",
    "opciones": [
        "Una heurística didáctica no calibrada clínicamente",
        "Un predictor clínico validado equivalente a AlphaMissense",
        "Una medida experimental de laboratorio",
    ],
    "correcta": "Una heurística didáctica no calibrada clínicamente",
    "explicacion": "Combina cambios fisicoquímicos y localización con pesos de diseño "
                   "pedagógico. La página «Comparar» muestra dónde acierta y dónde falla "
                   "frente al ΔΔG medido.",
})


# ---------------------------------------------------------------------------
# Estado del quiz
# ---------------------------------------------------------------------------
def reiniciar_quiz():
    orden = list(range(len(PREGUNTAS)))
    random.shuffle(orden)
    st.session_state.quiz_orden = orden
    st.session_state.quiz_idx = 0
    st.session_state.quiz_score = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_selected = None


if "quiz_orden" not in st.session_state:
    reiniciar_quiz()

# ---------------------------------------------------------------------------
# Encabezado
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-title">Quiz: ¿contacto o estructural?</div>
    <div class="hero-sub">Pon a prueba lo que entendiste sobre el mecanismo biofísico
    de las mutaciones</div>
    """,
    unsafe_allow_html=True,
)

orden = st.session_state.quiz_orden
N = len(orden)
idx = st.session_state.quiz_idx
score = st.session_state.quiz_score

# ---------------------------------------------------------------------------
# Pantalla final
# ---------------------------------------------------------------------------
if idx >= N:
    seccion("Resultado")
    pct = round(100 * score / N)
    if pct >= 80:
        st.success(f"¡Excelente! Puntaje: **{score} / {N}** ({pct}%). Dominas la "
                   f"distinción contacto vs. estructural.")
    elif pct >= 50:
        st.warning(f"Bien: **{score} / {N}** ({pct}%). Repasa la página del evaluador "
                   f"para afinar el mecanismo de cada mutación.")
    else:
        st.error(f"Puntaje: **{score} / {N}** ({pct}%). Te recomiendo revisar las "
                 f"secciones de mecanismo y estabilidad antes de reintentar.")
    if st.button("Reiniciar quiz", type="primary", key="reiniciar_final"):
        reiniciar_quiz()
        st.rerun()
    st.stop()

# ---------------------------------------------------------------------------
# Pregunta actual
# ---------------------------------------------------------------------------
q = PREGUNTAS[orden[idx]]

st.progress(idx / N)
st.caption(f"Pregunta {idx + 1} de {N}  ·  Aciertos: {score}")
st.markdown(f"### {q['pregunta']}")

if not st.session_state.quiz_answered:
    cols = st.columns(len(q["opciones"]))
    for col, opcion in zip(cols, q["opciones"]):
        if col.button(opcion, key=f"opt_{idx}_{opcion}", use_container_width=True):
            st.session_state.quiz_selected = opcion
            st.session_state.quiz_answered = True
            if opcion == q["correcta"]:
                st.session_state.quiz_score += 1
            st.rerun()
else:
    sel = st.session_state.quiz_selected
    if sel == q["correcta"]:
        st.success(f"¡Correcto! La respuesta es **{q['correcta']}**.")
    else:
        st.error(f"Elegiste «{sel}». La respuesta correcta es **{q['correcta']}**.")
    st.info(q["explicacion"])
    etiqueta = "Siguiente pregunta →" if idx + 1 < N else "Ver resultado →"
    if st.button(etiqueta, type="primary", key=f"next_{idx}"):
        st.session_state.quiz_idx += 1
        st.session_state.quiz_answered = False
        st.session_state.quiz_selected = None
        st.rerun()

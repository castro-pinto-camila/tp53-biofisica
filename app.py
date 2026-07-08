# -*- coding: utf-8 -*-
"""
Evaluador de Impacto Biofísico de Mutaciones en TP53 (p53) — punto de entrada.

Este archivo solo define la configuración de página y la navegación entre las
3 páginas de la app. El contenido vive en paginas/introduccion.py,
paginas/evaluador.py y paginas/comparar.py.

Ejecutar en Windows:
    py -m streamlit run app.py
"""

import streamlit as st

from estilos import aplicar_estilo

st.set_page_config(
    page_title="Evaluador de Impacto Biofísico · TP53",
    layout="wide",
)
aplicar_estilo()

pagina_intro = st.Page(
    "paginas/introduccion.py",
    title="El gen TP53",
    icon=":material/home:",
    default=True,
)
pagina_evaluador = st.Page(
    "paginas/evaluador.py",
    title="Evaluador de mutaciones",
    icon=":material/science:",
)
pagina_comparar = st.Page(
    "paginas/comparar.py",
    title="Comparar mutaciones",
    icon=":material/bar_chart:",
)
pagina_personalizada = st.Page(
    "paginas/personalizada.py",
    title="Laboratorio de mutaciones",
    icon=":material/biotech:",
)
pagina_quiz = st.Page(
    "paginas/quiz.py",
    title="Quiz",
    icon=":material/quiz:",
)
pagina_referencias = st.Page(
    "paginas/referencias.py",
    title="Glosario y referencias",
    icon=":material/menu_book:",
)

# La clave del dict aparece como titulo de seccion sobre los enlaces, en vez
# de mostrar solo la flecha ">>" de expandir/colapsar el panel lateral.
pg = st.navigation({
    "TP53 · Menú": [
        pagina_intro,
        pagina_evaluador,
        pagina_comparar,
        pagina_personalizada,
        pagina_quiz,
        pagina_referencias,
    ]
})
pg.run()

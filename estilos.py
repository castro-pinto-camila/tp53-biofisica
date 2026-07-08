# -*- coding: utf-8 -*-
"""
Estilos compartidos (estética académica) entre todas las páginas de la app.
"""

import streamlit as st

_CSS = """
<style>
  /* Contenedor principal un poco más angosto, tipo documento */
  .block-container { max-width: 1150px; padding-top: 2rem; }

  /* Encabezado */
  .hero-title {
      font-family: Georgia, 'Times New Roman', serif;
      font-size: 2.05rem; font-weight: 700; color: #1f3a5f;
      line-height: 1.2; margin-bottom: 0.25rem;
  }
  .hero-sub {
      font-family: Georgia, serif; font-size: 1.08rem; font-style: italic;
      color: #4a5560; margin-bottom: 0.6rem;
  }
  .hero-note {
      font-size: 0.86rem; color: #6a7480; border-left: 3px solid #cfd6dd;
      padding: 0.4rem 0.8rem; background: #f7f9fb; border-radius: 0 4px 4px 0;
  }

  /* Encabezados de sección */
  .section-h {
      font-family: Georgia, serif; font-size: 1.28rem; font-weight: 600;
      color: #1f3a5f; border-bottom: 1px solid #d6dbe0;
      padding-bottom: 0.3rem; margin: 1.6rem 0 0.9rem;
  }

  /* Tarjetas */
  .acard {
      border: 1px solid #dfe3e8; border-radius: 6px; padding: 1rem 1.15rem;
      background: #ffffff; min-height: 210px;
  }
  .acard-h {
      font-family: Georgia, serif; font-size: 1.02rem; font-weight: 600;
      color: #1f3a5f; border-bottom: 2px solid #eef0f3;
      padding-bottom: 0.4rem; margin-bottom: 0.6rem;
  }
  .kv { display: flex; justify-content: space-between; gap: 0.5rem;
        padding: 0.22rem 0; font-size: 0.92rem; border-bottom: 1px dotted #eef1f4; }
  .kv span { color: #5a6570; }
  .kv b { color: #1a1a1a; font-weight: 600; text-align: right; }
  .acard-note { font-size: 0.82rem; color: #6a7480; margin-top: 0.6rem;
                line-height: 1.35; }
  .tag { display: inline-block; padding: 0.12rem 0.55rem; border-radius: 12px;
         font-size: 0.78rem; font-weight: 600; margin-top: 0.6rem; }

  /* Etiqueta de impacto */
  .impact-badge {
      display: inline-block; padding: 0.5rem 1.1rem; border-radius: 24px;
      font-family: Georgia, serif; font-size: 1.02rem;
  }

  /* Callouts (mecanismo / polaridad) */
  .callout { padding: 0.8rem 1.1rem; border-radius: 0 5px 5px 0;
             margin: 0.4rem 0; font-size: 0.95rem; }
  .callout-t { font-family: Georgia, serif; font-weight: 700;
               margin-bottom: 0.25rem; }

  /* Botones (selección de mutación, pasos del explorador, etc.) */
  div.stButton > button {
      font-family: Georgia, serif; font-weight: 600; border-radius: 5px;
      letter-spacing: 0.01em; padding: 0.55rem 0.5rem; border-width: 1px;
  }
  div.stButton > button[kind="secondary"] {
      background: #ffffff; color: #33465c; border-color: #c3ccd6;
  }
  div.stButton > button[kind="secondary"]:hover {
      border-color: #1f3a5f; color: #1f3a5f;
  }

  /* Expanders más sobrios */
  .streamlit-expanderHeader { font-family: Georgia, serif; }

  /* Secuencia de aminoácidos (monoespaciada, con saltos por bloques) */
  .secuencia-aa {
      font-family: 'Courier New', monospace; font-size: 0.92rem;
      line-height: 1.9; letter-spacing: 0.03em; word-break: break-all;
      background: #f7f9fb; border: 1px solid #dfe3e8; border-radius: 6px;
      padding: 1rem 1.1rem; color: #33465c;
  }
  .secuencia-aa mark {
      background: #a23b3b; color: #ffffff; border-radius: 3px;
      padding: 0 2px; font-weight: 700;
  }

  /* Marcador de posición para imagenes pendientes */
  .placeholder-img {
      border: 2px dashed #c3ccd6; border-radius: 6px; padding: 1.4rem;
      text-align: center; color: #6a7480; font-size: 0.9rem; background: #f7f9fb;
  }

  /* Tabla comparativa (página "Comparar mutaciones") */
  .tabla-comp { width: 100%; border-collapse: collapse; font-size: 0.92rem;
                margin: 0.5rem 0 1.2rem; }
  .tabla-comp th {
      background: #1f3a5f; color: #ffffff; font-family: Georgia, serif;
      font-weight: 600; text-align: left; padding: 0.55rem 0.75rem;
  }
  .tabla-comp td { padding: 0.5rem 0.75rem; border-bottom: 1px solid #eef0f3; }
  .tabla-comp tr:nth-child(even) td { background: #f7f9fb; }
</style>
"""


def aplicar_estilo():
    st.markdown(_CSS, unsafe_allow_html=True)


def seccion(titulo):
    st.markdown(f'<div class="section-h">{titulo}</div>', unsafe_allow_html=True)

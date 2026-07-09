# -*- coding: utf-8 -*-
"""
Estilos compartidos entre todas las páginas de la app.

Sistema de diseño basado en *tokens* (variables CSS en :root): color, tipografía
y espaciado se definen una sola vez y todo lo demás los referencia con var(...).
Esto permite:
  - Cambiar la identidad visual desde un único lugar.
  - Soportar modo oscuro (prefers-color-scheme) redefiniendo los tokens.
Tipografía: serif (títulos, para gravedad académica) + sans (cuerpo, para lectura
en pantalla) — en vez de serif en absolutamente todo, que leía como paper impreso.
"""

import streamlit as st

_CSS = """
<style>
  :root {
    /* --- Paleta (modo claro) --- */
    --navy:        #1f3a5f;   /* primario: títulos, encabezados            */
    --navy-2:      #33465c;   /* texto secundario fuerte                    */
    --brick:       #a23b3b;   /* acento cálido: aumento / contacto / alerta */
    --teal:        #2c6b8f;   /* acento frío: disminución / estructura      */
    --gold:        #8a6a12;   /* acento ámbar: moderado / advertencia       */
    --green:       #2f6a44;   /* acento verde: bajo / plegado               */

    --ink:         #1a1a1a;   /* texto principal        */
    --ink-soft:    #5a6570;   /* texto atenuado         */
    --ink-faint:   #6a7480;   /* pies de figura, notas  */

    --surface:     #ffffff;   /* fondo de tarjetas            */
    --bg-soft:     #f7f9fb;   /* fondos suaves (hero-note, etc) */
    --bg-inset:    #eef0f3;   /* rieles, fondos hundidos       */
    --border:      #dfe3e8;   /* bordes de tarjeta             */
    --border-soft: #eef1f4;   /* separadores tenues            */

    /* --- Tipografía --- */
    --serif: Georgia, 'Iowan Old Style', 'Times New Roman', serif;
    --sans:  -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    --mono:  'SFMono-Regular', 'Cascadia Code', 'Courier New', monospace;

    /* --- Espaciado y forma --- */
    --radius:   8px;
    --radius-sm: 5px;
    --shadow:  0 1px 2px rgba(31,58,95,0.04), 0 2px 8px rgba(31,58,95,0.05);
  }

  /* --- Modo oscuro: se redefinen SOLO los tokens; el resto hereda --- */
  @media (prefers-color-scheme: dark) {
    :root {
      --navy:        #9dc0e6;
      --navy-2:      #b9c7d6;
      --brick:       #e08a8a;
      --teal:        #7fb8d4;
      --gold:        #d8b45a;
      --green:       #7cc79a;

      --ink:         #e8ecf1;
      --ink-soft:    #aeb8c4;
      --ink-faint:   #8a94a0;

      --surface:     #1a2230;
      --bg-soft:     #161c27;
      --bg-inset:    #222c3a;
      --border:      #33404f;
      --border-soft: #2a3542;
      --shadow:      0 1px 2px rgba(0,0,0,0.25), 0 2px 10px rgba(0,0,0,0.30);
    }
  }

  /* Cuerpo en sans (lectura en pantalla) */
  .block-container { max-width: 1150px; padding-top: 2rem; }
  .block-container p, .block-container li, .kv, .acard-note,
  .callout, .tabla-comp, .tag { font-family: var(--sans); }

  /* Encabezado */
  .hero-title {
      font-family: var(--serif);
      font-size: 2.15rem; font-weight: 700; color: var(--navy);
      line-height: 1.18; margin-bottom: 0.25rem; letter-spacing: -0.01em;
  }
  .hero-sub {
      font-family: var(--serif); font-size: 1.1rem; font-style: italic;
      color: var(--ink-soft); margin-bottom: 0.7rem;
  }
  .hero-note {
      font-family: var(--sans); font-size: 0.88rem; color: var(--ink-faint);
      border-left: 3px solid var(--teal);
      padding: 0.5rem 0.9rem; background: var(--bg-soft);
      border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  }

  /* Encabezados de sección */
  .section-h {
      font-family: var(--serif); font-size: 1.3rem; font-weight: 600;
      color: var(--navy); border-bottom: 1px solid var(--border);
      padding-bottom: 0.3rem; margin: 1.7rem 0 0.9rem;
  }

  /* --- Recuadro "qué vas a aprender" (objetivos de aprendizaje) --- */
  .learn-box {
      border: 1px solid var(--border); border-left: 4px solid var(--gold);
      border-radius: var(--radius); background: var(--surface);
      padding: 1rem 1.2rem; margin: 0.6rem 0 0.4rem; box-shadow: var(--shadow);
  }
  .learn-box .learn-h {
      font-family: var(--serif); font-weight: 700; color: var(--navy);
      font-size: 1.02rem; margin-bottom: 0.5rem;
  }
  .learn-box ul { margin: 0; padding-left: 1.1rem; }
  .learn-box li { font-family: var(--sans); font-size: 0.92rem;
                  color: var(--ink); margin: 0.28rem 0; }

  /* --- Cifra de impacto (hero stat) --- */
  .stat-hero {
      display: flex; align-items: baseline; gap: 0.6rem; flex-wrap: wrap;
      background: var(--bg-soft); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 0.8rem 1.1rem; margin: 0.5rem 0 0.3rem;
  }
  .stat-hero .stat-num {
      font-family: var(--serif); font-weight: 700; color: var(--brick);
      font-size: 2rem; line-height: 1;
  }
  .stat-hero .stat-txt { font-family: var(--sans); color: var(--ink-soft);
                         font-size: 0.95rem; }

  /* Tarjetas */
  .acard {
      border: 1px solid var(--border); border-radius: var(--radius);
      padding: 1rem 1.15rem; background: var(--surface); min-height: 210px;
      box-shadow: var(--shadow);
  }
  .acard-h {
      font-family: var(--serif); font-size: 1.02rem; font-weight: 600;
      color: var(--navy); border-bottom: 2px solid var(--border-soft);
      padding-bottom: 0.4rem; margin-bottom: 0.6rem;
  }
  .kv { display: flex; justify-content: space-between; gap: 0.5rem;
        padding: 0.22rem 0; font-size: 0.92rem; border-bottom: 1px dotted var(--border-soft); }
  .kv span { color: var(--ink-soft); }
  .kv b { color: var(--ink); font-weight: 600; text-align: right; }
  .acard-note { font-size: 0.82rem; color: var(--ink-faint); margin-top: 0.6rem;
                line-height: 1.4; }
  .tag { display: inline-block; padding: 0.12rem 0.55rem; border-radius: 12px;
         font-size: 0.78rem; font-weight: 600; margin-top: 0.6rem; }

  /* Etiqueta de impacto */
  .impact-badge {
      display: inline-block; padding: 0.5rem 1.1rem; border-radius: 24px;
      font-family: var(--serif); font-size: 1.02rem; font-weight: 600;
  }

  /* Callouts (mecanismo / polaridad) */
  .callout { padding: 0.8rem 1.1rem; border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
             margin: 0.4rem 0; font-size: 0.95rem; }
  .callout-t { font-family: var(--serif); font-weight: 700;
               margin-bottom: 0.25rem; }

  /* Botones (selección de mutación, pasos del explorador, etc.) */
  div.stButton > button {
      font-family: var(--sans); font-weight: 600; border-radius: var(--radius-sm);
      letter-spacing: 0.01em; padding: 0.55rem 0.5rem; border-width: 1px;
      transition: border-color 0.12s ease, color 0.12s ease;
  }
  div.stButton > button[kind="secondary"] {
      background: var(--surface); color: var(--navy-2); border-color: var(--border);
  }
  div.stButton > button[kind="secondary"]:hover {
      border-color: var(--navy); color: var(--navy);
  }

  /* Expanders más sobrios */
  .streamlit-expanderHeader { font-family: var(--serif); }

  /* Secuencia de aminoácidos (monoespaciada, con saltos por bloques) */
  .secuencia-aa {
      font-family: var(--mono); font-size: 0.92rem;
      line-height: 1.9; letter-spacing: 0.03em; word-break: break-all;
      background: var(--bg-soft); border: 1px solid var(--border);
      border-radius: var(--radius); padding: 1rem 1.1rem; color: var(--navy-2);
  }
  .secuencia-aa mark {
      background: var(--brick); color: #ffffff; border-radius: 3px;
      padding: 0 2px; font-weight: 700;
  }

  /* Marcador de posición para imagenes pendientes */
  .placeholder-img {
      border: 2px dashed var(--border); border-radius: var(--radius); padding: 1.4rem;
      text-align: center; color: var(--ink-faint); font-size: 0.9rem; background: var(--bg-soft);
  }

  /* Tabla comparativa (página "Comparar mutaciones") */
  .tabla-comp { width: 100%; border-collapse: collapse; font-size: 0.92rem;
                margin: 0.5rem 0 1.2rem; }
  .tabla-comp th {
      background: var(--navy); color: #ffffff; font-family: var(--serif);
      font-weight: 600; text-align: left; padding: 0.55rem 0.75rem;
  }
  .tabla-comp td { padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--border-soft);
                   color: var(--ink); }
  .tabla-comp tr:nth-child(even) td { background: var(--bg-soft); }

  /* --- Responsive: en pantallas angostas, las tarjetas no fuerzan altura --- */
  @media (max-width: 640px) {
      .acard { min-height: auto; }
      .hero-title { font-size: 1.7rem; }
      .stat-hero .stat-num { font-size: 1.6rem; }
      .block-container { padding-top: 1.2rem; }
  }
</style>
"""


def aplicar_estilo():
    st.markdown(_CSS, unsafe_allow_html=True)


def seccion(titulo):
    st.markdown(f'<div class="section-h">{titulo}</div>', unsafe_allow_html=True)

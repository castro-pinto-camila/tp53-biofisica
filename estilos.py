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
    --heading:     #1f3a5f;   /* títulos grandes (hero) — muy contrastado   */
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

    /* --- Gradiente de cabecera (banner hero) --- */
    --hero-a: #1f3a5f;   /* navy profundo */
    --hero-b: #2c6b8f;   /* teal          */
    --hero-c: #7a2f3a;   /* acento vino para el borde inferior del hero */

    /* --- Subtítulos de sección: SIEMPRE oscuros, fijos --- */
    /* A diferencia de --navy (que se aclara en modo oscuro), estos dos NO se
       redefinen dentro del @media prefers-color-scheme: dark de abajo, así que
       el subtítulo y su barra de acento se mantienen oscuros en ambos modos. */
    --section-heading: #16283f;  /* navy muy oscuro, fijo               */
    --wine-accent:     #7a2f3a;  /* mismo vino del borde de la tarjeta título */

    /* --- Espaciado y forma --- */
    --radius:   8px;
    --radius-sm: 5px;
    --radius-lg: 16px;
    --shadow:  0 1px 2px rgba(31,58,95,0.05), 0 4px 14px rgba(31,58,95,0.07);
    --shadow-lg: 0 6px 24px rgba(31,58,95,0.12);
  }

  /* --- Modo oscuro: se redefinen SOLO los tokens; el resto hereda --- */
  @media (prefers-color-scheme: dark) {
    :root {
      --navy:        #a9caee;
      --heading:     #e7f0fb;
      --navy-2:      #c4d2e0;
      --brick:       #e79a9a;
      --teal:        #86bcd8;
      --gold:        #ddba64;
      --green:       #85cfa2;

      --ink:         #e8ecf1;
      --ink-soft:    #aeb8c4;
      --ink-faint:   #8a94a0;

      --surface:     #232e40;
      --bg-soft:     #1c2534;
      --bg-inset:    #2a3648;
      --border:      #3a4759;
      --border-soft: #303c4c;
      --shadow:      0 1px 2px rgba(0,0,0,0.20), 0 4px 16px rgba(0,0,0,0.30);
      --shadow-lg:   0 8px 30px rgba(0,0,0,0.42);

      --hero-a: #16283f;
      --hero-b: #1b4a5f;
      --hero-c: #6a2b34;
    }
  }

  /* Cuerpo en sans (lectura en pantalla) */
  .block-container { max-width: 1150px; padding-top: 2rem; }
  .block-container p, .block-container li, .kv, .acard-note,
  .callout, .tabla-comp, .tag { font-family: var(--sans); }

  /* --- Cabecera con gradiente (banner hero) --- */
  .hero-banner {
      position: relative; overflow: hidden;
      background: linear-gradient(135deg, var(--hero-a) 0%, var(--hero-b) 100%);
      border-radius: var(--radius-lg);
      border-bottom: 3px solid var(--hero-c);
      padding: 1.7rem 1.9rem; margin: 0.2rem 0 1.1rem;
      box-shadow: var(--shadow-lg);
  }
  /* Hélice de ADN decorativa (SVG data-uri en una sola línea), tenue, a la derecha */
  .hero-banner::after {
      content: ""; position: absolute; top: -28px; right: 6px;
      width: 150px; height: 300px; opacity: 0.22; pointer-events: none;
      background-repeat: no-repeat; background-position: center;
      background-size: contain;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='240' viewBox='0 0 120 240'%3E%3Cg fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M26.0 0.0 L27.7 5.0 L32.5 10.0 L40.0 15.0 L49.5 20.0 L60.0 25.0 L70.5 30.0 L80.0 35.0 L87.5 40.0 L92.3 45.0 L94.0 50.0 L92.3 55.0 L87.5 60.0 L80.0 65.0 L70.5 70.0 L60.0 75.0 L49.5 80.0 L40.0 85.0 L32.5 90.0 L27.7 95.0 L26.0 100.0 L27.7 105.0 L32.5 110.0 L40.0 115.0 L49.5 120.0 L60.0 125.0 L70.5 130.0 L80.0 135.0 L87.5 140.0 L92.3 145.0 L94.0 150.0 L92.3 155.0 L87.5 160.0 L80.0 165.0 L70.5 170.0 L60.0 175.0 L49.5 180.0 L40.0 185.0 L32.5 190.0 L27.7 195.0 L26.0 200.0 L27.7 205.0 L32.5 210.0 L40.0 215.0 L49.5 220.0 L60.0 225.0 L70.5 230.0 L80.0 235.0 L87.5 240.0'/%3E%3Cpath d='M94.0 0.0 L92.3 5.0 L87.5 10.0 L80.0 15.0 L70.5 20.0 L60.0 25.0 L49.5 30.0 L40.0 35.0 L32.5 40.0 L27.7 45.0 L26.0 50.0 L27.7 55.0 L32.5 60.0 L40.0 65.0 L49.5 70.0 L60.0 75.0 L70.5 80.0 L80.0 85.0 L87.5 90.0 L92.3 95.0 L94.0 100.0 L92.3 105.0 L87.5 110.0 L80.0 115.0 L70.5 120.0 L60.0 125.0 L49.5 130.0 L40.0 135.0 L32.5 140.0 L27.7 145.0 L26.0 150.0 L27.7 155.0 L32.5 160.0 L40.0 165.0 L49.5 170.0 L60.0 175.0 L70.5 180.0 L80.0 185.0 L87.5 190.0 L92.3 195.0 L94.0 200.0 L92.3 205.0 L87.5 210.0 L80.0 215.0 L70.5 220.0 L60.0 225.0 L49.5 230.0 L40.0 235.0 L32.5 240.0'/%3E%3Cline x1='32.5' y1='10.0' x2='87.5' y2='10.0' stroke-width='2'/%3E%3Cline x1='49.5' y1='20.0' x2='70.5' y2='20.0' stroke-width='2'/%3E%3Cline x1='70.5' y1='30.0' x2='49.5' y2='30.0' stroke-width='2'/%3E%3Cline x1='87.5' y1='40.0' x2='32.5' y2='40.0' stroke-width='2'/%3E%3Cline x1='94.0' y1='50.0' x2='26.0' y2='50.0' stroke-width='2'/%3E%3Cline x1='87.5' y1='60.0' x2='32.5' y2='60.0' stroke-width='2'/%3E%3Cline x1='70.5' y1='70.0' x2='49.5' y2='70.0' stroke-width='2'/%3E%3Cline x1='49.5' y1='80.0' x2='70.5' y2='80.0' stroke-width='2'/%3E%3Cline x1='32.5' y1='90.0' x2='87.5' y2='90.0' stroke-width='2'/%3E%3Cline x1='26.0' y1='100.0' x2='94.0' y2='100.0' stroke-width='2'/%3E%3Cline x1='32.5' y1='110.0' x2='87.5' y2='110.0' stroke-width='2'/%3E%3Cline x1='49.5' y1='120.0' x2='70.5' y2='120.0' stroke-width='2'/%3E%3Cline x1='70.5' y1='130.0' x2='49.5' y2='130.0' stroke-width='2'/%3E%3Cline x1='87.5' y1='140.0' x2='32.5' y2='140.0' stroke-width='2'/%3E%3Cline x1='94.0' y1='150.0' x2='26.0' y2='150.0' stroke-width='2'/%3E%3Cline x1='87.5' y1='160.0' x2='32.5' y2='160.0' stroke-width='2'/%3E%3Cline x1='70.5' y1='170.0' x2='49.5' y2='170.0' stroke-width='2'/%3E%3Cline x1='49.5' y1='180.0' x2='70.5' y2='180.0' stroke-width='2'/%3E%3Cline x1='32.5' y1='190.0' x2='87.5' y2='190.0' stroke-width='2'/%3E%3Cline x1='26.0' y1='200.0' x2='94.0' y2='200.0' stroke-width='2'/%3E%3Cline x1='32.5' y1='210.0' x2='87.5' y2='210.0' stroke-width='2'/%3E%3Cline x1='49.5' y1='220.0' x2='70.5' y2='220.0' stroke-width='2'/%3E%3Cline x1='70.5' y1='230.0' x2='49.5' y2='230.0' stroke-width='2'/%3E%3C/g%3E%3C/svg%3E");
  }
  .hero-banner > * { position: relative; z-index: 1; }

  .hero-title {
      font-family: var(--serif);
      font-size: 2.2rem; font-weight: 700; color: var(--heading);
      line-height: 1.2; margin-bottom: 0.3rem;
  }
  .hero-banner .hero-title { color: #ffffff; }
  .hero-sub {
      font-family: var(--serif); font-size: 1.1rem; font-style: italic;
      color: var(--ink-soft); margin-bottom: 0.6rem; max-width: 64ch;
  }
  .hero-banner .hero-sub { color: rgba(255,255,255,0.86); }
  .hero-note {
      font-family: var(--sans); font-size: 0.88rem; color: var(--ink-soft);
      border-left: 3px solid var(--teal);
      padding: 0.15rem 0 0.15rem 0.9rem; background: transparent;
      margin: 0.5rem 0 0;
  }
  .hero-note b { color: var(--navy); }
  .hero-banner .hero-note {
      color: rgba(255,255,255,0.82); border-left-color: rgba(255,255,255,0.45);
  }
  .hero-banner .hero-note b { color: #ffffff; }

  /* Encabezados de sección (con acento lateral en gradiente) */
  /* color y barra usan tokens FIJOS (--section-heading / --wine-accent), no
     los adaptativos --navy/--teal/--brick, para que nunca se aclaren en modo
     oscuro: siempre navy oscuro con un toque de vino. */
  .section-h {
      font-family: var(--serif); font-size: 1.3rem; font-weight: 600;
      color: var(--section-heading); border-bottom: 1px solid var(--border);
      padding-bottom: 0.35rem; margin: 1.8rem 0 0.9rem;
      display: flex; align-items: center; gap: 0.55rem;
  }
  .section-h::before {
      content: ""; display: inline-block; width: 6px; height: 1.05em;
      border-radius: 3px; flex: none;
      background: linear-gradient(180deg, var(--section-heading), var(--wine-accent));
  }

  /* --- Recuadro "qué vas a aprender" (objetivos de aprendizaje) --- */
  /* Fondo teñido con el acento ámbar (color-mix) en vez de una losa opaca: se
     lee como panel, no como bloque negro en modo oscuro. */
  .learn-box {
      border: 1px solid var(--border); border-left: 4px solid var(--gold);
      border-radius: var(--radius);
      background: color-mix(in srgb, var(--gold) 8%, var(--surface));
      padding: 0.9rem 1.2rem; margin: 1rem 0 0.6rem;
  }
  .learn-box .learn-h {
      font-family: var(--serif); font-weight: 700; color: var(--heading);
      font-size: 1.05rem; margin-bottom: 0.5rem;
  }
  .learn-box ul { margin: 0; padding-left: 1.1rem; }
  .learn-box li { font-family: var(--sans); font-size: 0.92rem;
                  color: var(--ink); margin: 0.34rem 0; line-height: 1.45; }

  /* --- Cifra de impacto (dentro del banner): número grande + texto --- */
  .stat-hero {
      display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;
      margin: 0.9rem 0 0.1rem; padding-top: 0.9rem;
      border-top: 1px solid rgba(255,255,255,0.18);
  }
  .stat-hero .stat-num {
      font-family: var(--serif); font-weight: 700;
      color: #ffd9a8; font-size: 2.9rem; line-height: 1;
      text-shadow: 0 1px 8px rgba(0,0,0,0.25);
  }
  .stat-hero .stat-txt { font-family: var(--sans); color: rgba(255,255,255,0.9);
                         font-size: 0.96rem; line-height: 1.5; flex: 1 1 300px; }
  .stat-hero .stat-txt b { color: #ffffff; }

  /* Tarjetas (con acento superior y elevación al pasar el cursor) */
  .acard {
      position: relative; border: 1px solid var(--border);
      border-radius: var(--radius); border-top: 3px solid var(--teal);
      padding: 1rem 1.15rem; background: var(--surface); min-height: 210px;
      box-shadow: var(--shadow); transition: transform 0.14s ease, box-shadow 0.14s ease;
  }
  .acard:hover { transform: translateY(-3px); box-shadow: var(--shadow-lg); }
  .acard-h {
      font-family: var(--serif); font-size: 1.05rem; font-weight: 600;
      color: var(--navy); padding-bottom: 0.45rem; margin-bottom: 0.6rem;
      border-bottom: 2px solid transparent;
      border-image: linear-gradient(90deg, var(--teal), transparent) 1;
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
  /* Cabecera con el mismo navy oscuro fijo que los subtítulos de sección (no
     el --navy adaptativo, que en modo oscuro se aclaraba y dejaba el
     encabezado en azul pálido con texto blanco casi ilegible). Cada <td>
     ahora lleva SIEMPRE un fondo explícito emparejado con su color de texto
     (antes solo las filas pares lo tenían; las impares heredaban un fondo que
     no correspondía al texto claro, dejándolo casi invisible). */
  .tabla-comp { width: 100%; border-collapse: collapse; font-size: 0.92rem;
                margin: 0.5rem 0 1.2rem; }
  .tabla-comp th {
      background: var(--section-heading); color: #ffffff; font-family: var(--serif);
      font-weight: 600; text-align: left; padding: 0.55rem 0.75rem;
  }
  .tabla-comp td { padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--border-soft);
                   background: var(--surface); color: var(--ink); }
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


def hero(titulo, subtitulo, nota=None):
    """Cabecera con gradiente (banner hero) reutilizable en todas las páginas.

    Se emite en una sola línea de HTML: st.markdown interpreta el HTML indentado
    como bloque de código, así que evitamos saltos de línea con sangría.
    """
    nota_html = f'<div class="hero-note">{nota}</div>' if nota else ""
    st.markdown(
        f'<div class="hero-banner">'
        f'<div class="hero-title">{titulo}</div>'
        f'<div class="hero-sub">{subtitulo}</div>'
        f'{nota_html}</div>',
        unsafe_allow_html=True,
    )

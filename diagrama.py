# -*- coding: utf-8 -*-
"""
Diagrama didactico (SVG) del dogma central aplicado a TP53:
como se produce la proteina p53 a partir del gen (ADN -> ARN -> proteina).

Hecho a mano, con la paleta academica de la app y etiquetas correctas (sin
depender de generadores de imagenes). Se incrusta como SVG responsivo.
"""

SVG_DOGMA_CENTRAL = """
<svg viewBox="0 0 980 430" xmlns="http://www.w3.org/2000/svg" role="img"
     width="100%" height="100%" preserveAspectRatio="xMidYMid meet"
     font-family="Georgia, 'Times New Roman', serif">
  <title>Del gen TP53 a la proteina p53</title>
  <desc>El ADN del gen TP53 se transcribe a ARN mensajero por la ARN polimerasa;
  el ribosoma lo traduce en una cadena de 393 aminoacidos que se pliega en la
  proteina p53.</desc>

  <rect x="6" y="6" width="968" height="418" rx="12" fill="#ffffff" stroke="#dfe3e8" stroke-width="1.5"/>

  <text x="490" y="46" text-anchor="middle" font-size="23" font-weight="700" fill="#1f3a5f">Del gen TP53 a la proteina p53</text>
  <text x="490" y="70" text-anchor="middle" font-size="13.5" font-style="italic" fill="#5a6570">El mismo camino que cualquier gen: ADN &#8594; ARN &#8594; proteina</text>

  <!-- ETAPA 1: GEN (ADN) -->
  <g stroke-linecap="round">
    <polyline points="60,205 72,220 84,214 96,196 108,190 120,205 132,220 144,214 156,196 168,190 180,205" fill="none" stroke="#1f3a5f" stroke-width="3.2"/>
    <polyline points="60,205 72,190 84,196 96,214 108,220 120,205 132,190 144,196 156,214 168,220 180,205" fill="none" stroke="#2c6b8f" stroke-width="3.2"/>
    <line x1="72" y1="190" x2="72" y2="220" stroke="#9db2c6" stroke-width="1.8"/>
    <line x1="96" y1="196" x2="96" y2="214" stroke="#9db2c6" stroke-width="1.8"/>
    <line x1="144" y1="196" x2="144" y2="214" stroke="#9db2c6" stroke-width="1.8"/>
    <line x1="168" y1="190" x2="168" y2="220" stroke="#9db2c6" stroke-width="1.8"/>
  </g>
  <text x="120" y="300" text-anchor="middle" font-size="15" font-weight="700" fill="#1f3a5f">Gen TP53</text>
  <text x="120" y="320" text-anchor="middle" font-size="12" fill="#5a6570">ADN &#183; cromosoma 17</text>

  <!-- flecha 1 -->
  <text x="243" y="150" text-anchor="middle" font-size="13" font-weight="700" fill="#33465c">Transcripcion</text>
  <text x="243" y="167" text-anchor="middle" font-size="10.5" fill="#5a6570">la ARN polimerasa copia el ADN</text>
  <line x1="200" y1="205" x2="285" y2="205" stroke="#9aa7b4" stroke-width="3"/>
  <polygon points="285,198 298,205 285,212" fill="#9aa7b4"/>

  <!-- ETAPA 2: ARNm -->
  <polyline points="322,205 334,220 346,214 358,196 370,190 382,205 394,220 406,214 418,196 430,190 442,205" fill="none" stroke="#b07d1a" stroke-width="4" stroke-linecap="round"/>
  <circle cx="346" cy="214" r="3.2" fill="#b07d1a"/>
  <circle cx="382" cy="205" r="3.2" fill="#b07d1a"/>
  <circle cx="418" cy="196" r="3.2" fill="#b07d1a"/>
  <text x="382" y="300" text-anchor="middle" font-size="15" font-weight="700" fill="#1f3a5f">ARN mensajero</text>
  <text x="382" y="320" text-anchor="middle" font-size="12" fill="#5a6570">copia movil del gen (ARNm)</text>

  <!-- flecha 2 -->
  <text x="500" y="150" text-anchor="middle" font-size="13" font-weight="700" fill="#33465c">Traduccion</text>
  <text x="500" y="167" text-anchor="middle" font-size="10.5" fill="#5a6570">el ribosoma lee los codones</text>
  <line x1="458" y1="205" x2="543" y2="205" stroke="#9aa7b4" stroke-width="3"/>
  <polygon points="543,198 556,205 543,212" fill="#9aa7b4"/>

  <!-- ETAPA 3: CADENA DE AMINOACIDOS -->
  <g>
    <polyline points="582,198 600,190 618,198 636,190 654,198 672,190" fill="none" stroke="#a23b3b" stroke-width="2.4"/>
    <circle cx="582" cy="198" r="8.5" fill="#a23b3b"/>
    <circle cx="600" cy="190" r="8.5" fill="#c15a5a"/>
    <circle cx="618" cy="198" r="8.5" fill="#a23b3b"/>
    <circle cx="636" cy="190" r="8.5" fill="#c15a5a"/>
    <circle cx="654" cy="198" r="8.5" fill="#a23b3b"/>
    <circle cx="672" cy="190" r="8.5" fill="#c15a5a"/>
  </g>
  <text x="628" y="300" text-anchor="middle" font-size="15" font-weight="700" fill="#1f3a5f">Cadena de aminoacidos</text>
  <text x="628" y="320" text-anchor="middle" font-size="12" fill="#5a6570">393 en total</text>

  <!-- flecha 3 -->
  <text x="748" y="150" text-anchor="middle" font-size="13" font-weight="700" fill="#33465c">Plegamiento</text>
  <text x="748" y="167" text-anchor="middle" font-size="10.5" fill="#5a6570">toma su forma 3D</text>
  <line x1="708" y1="205" x2="790" y2="205" stroke="#9aa7b4" stroke-width="3"/>
  <polygon points="790,198 803,205 790,212" fill="#9aa7b4"/>

  <!-- ETAPA 4: PROTEINA p53 -->
  <g>
    <ellipse cx="862" cy="200" rx="36" ry="31" fill="#a23b3b"/>
    <path d="M842 200 q10 -16 22 -4 q10 12 20 -2" fill="none" stroke="#ffffff" stroke-width="3" stroke-linecap="round" opacity="0.85"/>
    <circle cx="862" cy="200" r="4.5" fill="#ffffff" opacity="0.85"/>
  </g>
  <text x="862" y="300" text-anchor="middle" font-size="15" font-weight="700" fill="#1f3a5f">Proteina p53</text>
  <text x="862" y="320" text-anchor="middle" font-size="12" fill="#5a6570">plegada y funcional</text>

  <!-- LEYENDA -->
  <g font-size="12.5" fill="#33465c">
    <circle cx="360" cy="382" r="6" fill="#1f3a5f"/><text x="372" y="386">ADN</text>
    <circle cx="452" cy="382" r="6" fill="#b07d1a"/><text x="464" y="386">ARN</text>
    <circle cx="548" cy="382" r="6" fill="#a23b3b"/><text x="560" y="386">Proteina</text>
  </g>
  <text x="490" y="410" text-anchor="middle" font-size="11" fill="#8a94a0">Cada color es un tipo de molecula. Esquema didactico, no a escala.</text>
</svg>
"""

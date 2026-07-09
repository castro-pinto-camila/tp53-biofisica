# -*- coding: utf-8 -*-
"""
Visor 3D interactivo de la estructura del dominio de unión al ADN de p53
(PDB 1TUP) con el residuo mutado resaltado.

Es autocontenido y funciona SIN internet: la librería 3Dmol.js y el archivo PDB
se leen del proyecto (lib/3Dmol-min.js, data/1tup.pdb) y se incrustan en el HTML
que la app embebe con streamlit.components.v1.

Referencia estructura: Cho, Gorina, Jeffrey & Pavletich 1994, Science 265:346
(PDB 1TUP). Cadenas A/B/C = monómeros de p53; E/F = ADN; ZN = zinc estructural.
"""

import os

_BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(_BASE, "lib", "3Dmol-min.js"), encoding="utf-8") as _f:
    # Evita que un eventual "</script>" dentro de la librería rompa el HTML.
    _JS = _f.read().replace("</script>", "<\\/script>")

with open(os.path.join(_BASE, "data", "1tup.pdb"), encoding="utf-8") as _f:
    _PDB = _f.read()

# Cadena del monómero que hace los contactos específicos con el ADN en 1TUP;
# se usa para centrar la cámara en la relación residuo–ADN.
_CADENA_FOCO = "B"

_PLANTILLA = """
<style>
  .v3d-wrap { position: relative; }
  .v3d-controls {
      position: absolute; left: 10px; bottom: 10px; z-index: 5;
      display: flex; gap: 6px;
  }
  .v3d-btn {
      width: 34px; height: 34px; border-radius: 50%;
      background: #ffffff; border: 1px solid #c3ccd6;
      display: flex; align-items: center; justify-content: center;
      cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.08);
  }
  .v3d-btn:hover { border-color: #1f3a5f; background: #f2f5f8; }
  .v3d-btn svg { width: 16px; height: 16px; }
</style>
<div class="v3d-wrap">
  <div id="viewer3d" style="width:100%; height:480px; position:relative;
       border:1px solid #dfe3e8; border-radius:6px;"></div>
  <div class="v3d-controls">
    <div class="v3d-btn" id="v3d-zoom-out" title="Alejar">
      <svg viewBox="0 0 24 24" fill="none" stroke="#33465c" stroke-width="2.4" stroke-linecap="round">
        <line x1="5" y1="12" x2="19" y2="12"/>
      </svg>
    </div>
    <div class="v3d-btn" id="v3d-zoom-in" title="Acercar">
      <svg viewBox="0 0 24 24" fill="none" stroke="#33465c" stroke-width="2.4" stroke-linecap="round">
        <line x1="12" y1="5" x2="12" y2="19"/>
        <line x1="5" y1="12" x2="19" y2="12"/>
      </svg>
    </div>
    <div class="v3d-btn" id="v3d-home" title="Vista original">
      <svg viewBox="0 0 24 24" fill="none" stroke="#33465c" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M4 11.5 L12 4 L20 11.5"/>
        <path d="M6.5 9.8 V20 H17.5 V9.8"/>
      </svg>
    </div>
  </div>
</div>
<script>__JS__</script>
<script type="text/plain" id="pdbdata">__PDB__</script>
<script>
(function () {
  function go() {
    if (typeof $3Dmol === "undefined") { setTimeout(go, 50); return; }
    var viewer = $3Dmol.createViewer(document.getElementById("viewer3d"),
                                     {backgroundColor: "white"});
    var pdb = document.getElementById("pdbdata").textContent;
    viewer.addModel(pdb, "pdb");

    // Proteína: cartoon gris.
    viewer.setStyle({}, {cartoon: {color: 0xc9ced6}});
    // ADN: cartoon + varillas naranjas.
    viewer.setStyle({resn: ["DA", "DT", "DG", "DC"]},
                    {cartoon: {color: 0xe0a458},
                     stick: {colorscheme: "orangeCarbon", radius: 0.16}});
    // Zinc estructural.
    viewer.setStyle({resn: "ZN"}, {sphere: {color: 0x8a97a6, scale: 0.4}});

    // Residuo mutado: varillas rojas + esferas, en las tres cadenas.
    var sel = {resi: __POS__};
    viewer.setStyle(sel, {stick: {colorscheme: "redCarbon", radius: 0.35},
                          cartoon: {color: 0xa23b3b}});
    viewer.addStyle(sel, {sphere: {color: 0xa23b3b, scale: 0.28}});
    // Etiqueta solo en la cadena de foco para no repetirla en las 3 copias.
    viewer.addResLabels({resi: __POS__, chain: "__FOCO__"},
                        {fontSize: 12, fontColor: "white",
                         backgroundColor: 0xa23b3b, showBackground: true});

    // Centrar en la copia que contacta el ADN, con algo de contexto.
    viewer.zoomTo({resi: __POS__, chain: "__FOCO__"});
    viewer.zoom(0.62);
    viewer.render();

    // Vista de referencia para el boton "casita" (volver al encuadre inicial).
    var vistaInicial = viewer.getView();

    document.getElementById("v3d-home").addEventListener("click", function () {
      viewer.setView(vistaInicial);
    });
    document.getElementById("v3d-zoom-in").addEventListener("click", function () {
      viewer.zoom(1.3, 200);
    });
    document.getElementById("v3d-zoom-out").addEventListener("click", function () {
      viewer.zoom(1 / 1.3, 200);
    });
  }
  go();
})();
</script>
"""


def generar_html_3d(posicion, nombre="", clasificacion=""):
    """Devuelve el HTML autocontenido del visor 3D con el residuo `posicion`
    resaltado sobre la estructura 1TUP.
    """
    html = _PLANTILLA
    html = html.replace("__JS__", _JS)
    html = html.replace("__PDB__", _PDB)
    html = html.replace("__POS__", str(int(posicion)))
    html = html.replace("__FOCO__", _CADENA_FOCO)
    return html

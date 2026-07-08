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
<div id="viewer3d" style="width:100%; height:480px; position:relative;
     border:1px solid #dfe3e8; border-radius:6px;"></div>
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

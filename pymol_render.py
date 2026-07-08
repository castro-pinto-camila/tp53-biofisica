# -*- coding: utf-8 -*-
"""
FASE FINAL (opcional) — Visualizacion 3D con PyMOL en modo headless.

Genera un PNG por mutacion resaltando el residuo mutado sobre la estructura del
dominio de union al ADN de p53. Las imagenes se guardan en imagenes/estructuras/
y la app (app.py) las muestra automaticamente si existen.

NO se integra PyMOL dentro de la app en tiempo real: este script se ejecuta por
separado y solo produce imagenes estaticas.

Requisitos:
    - PyMOL instalado (open-source o incentive). Ejemplos de instalacion:
        conda install -c conda-forge pymol-open-source
    - Conexion a internet la primera vez (PyMOL descarga el PDB con 'fetch').

Uso (headless, sin ventana):
    pymol -cq pymol_render.py

Estructura de referencia: 1TUP (dominio central de p53 unido a ADN).
"""

import os

# 'cmd' solo existe cuando el script corre dentro de PyMOL.
try:
    from pymol import cmd
except ImportError:  # permite importar el modulo fuera de PyMOL sin romper
    cmd = None

# Codigo PDB del dominio de union al ADN de p53 unido a ADN.
PDB_CODE = "1TUP"

# Cadena de la proteina p53 en 1TUP (A/B/C son proteina; E/F son ADN).
CADENA_PROTEINA = "A"

# Mutaciones a renderizar: nombre -> posicion (numeracion de p53).
MUTACIONES = {
    "R175H": 175,
    "R248W": 248,
    "G245S": 245,
    "R282W": 282,
}

_BASE = os.path.dirname(os.path.abspath(__file__))
_SALIDA = os.path.join(_BASE, "imagenes", "estructuras")


def render_residuo(nombre, posicion):
    """Genera un PNG con el residuo `posicion` resaltado."""
    cmd.reinitialize()
    cmd.fetch(PDB_CODE, async_=0)

    cmd.hide("everything")
    cmd.bg_color("white")
    cmd.show("cartoon", "polymer.protein")
    cmd.color("grey80", "polymer.protein")

    # ADN, si esta presente en la estructura
    cmd.show("cartoon", "polymer.nucleic")
    cmd.color("wheat", "polymer.nucleic")

    sel = "chain %s and resi %d" % (CADENA_PROTEINA, posicion)
    cmd.show("sticks", sel)
    cmd.color("red", sel)
    cmd.set("cartoon_transparency", 0.3)

    cmd.orient(sel)
    cmd.zoom(sel, 8)
    cmd.set("ray_opaque_background", 0)

    destino = os.path.join(_SALIDA, "%s.png" % nombre)
    cmd.png(destino, width=1000, height=800, dpi=150, ray=1)
    print("Guardado:", destino)


def main():
    if cmd is None:
        raise SystemExit(
            "Este script debe ejecutarse dentro de PyMOL:\n"
            "    pymol -cq pymol_render.py"
        )
    os.makedirs(_SALIDA, exist_ok=True)
    for nombre, posicion in MUTACIONES.items():
        try:
            render_residuo(nombre, posicion)
        except Exception as exc:  # noqa: BLE001
            print("Error renderizando %s: %s" % (nombre, exc))


if __name__ == "__main__" or cmd is not None:
    main()

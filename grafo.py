# -*- coding: utf-8 -*-
"""
Grafo interactivo mutacion <-> tipo de cancer, estilo Obsidian (pyvis).

Nodos de mutacion en rojo (grandes), nodos de tipo de cancer en azul (pequenos),
aristas grises. Fisica barnes_hut, fondo oscuro. Devuelve la ruta a un HTML
temporal que la app embebe con streamlit.components.v1.
"""

import os
import tempfile

from pyvis.network import Network

from biofisica import cargar_mutaciones

COLOR_MUTACION = "#a23b3b"   # rojo ladrillo (académico)
COLOR_CANCER = "#2c6b8f"     # azul apagado
COLOR_ARISTA = "#c3ccd6"     # gris claro
FONDO = "#ffffff"

# Enlaces al Instituto Nacional del Cáncer (NCI, en español). Cada uno fue
# VERIFICADO (HTTP 200 + título correcto) el 2026-07-08; no son enlaces
# inventados. Colon y Recto comparten la página de cáncer colorrectal.
URLS_CANCER = {
    "Pulmón":   "https://www.cancer.gov/espanol/tipos/pulmon",
    "Mama":     "https://www.cancer.gov/espanol/tipos/seno",
    "Colon":    "https://www.cancer.gov/espanol/tipos/colorrectal",
    "Recto":    "https://www.cancer.gov/espanol/tipos/colorrectal",
    "Ovario":   "https://www.cancer.gov/espanol/tipos/ovario",
    "Esófago":  "https://www.cancer.gov/espanol/tipos/esofago",
    "Cerebro":  "https://www.cancer.gov/espanol/tipos/cerebro",
    "Estómago": "https://www.cancer.gov/espanol/tipos/estomago",
    "Hígado":   "https://www.cancer.gov/espanol/tipos/higado",
    "Páncreas": "https://www.cancer.gov/espanol/tipos/pancreas",
    "Piel":     "https://www.cancer.gov/espanol/tipos/piel",
}


def construir_grafo():
    """Construye el grafo y devuelve la ruta al HTML generado."""
    mutaciones = cargar_mutaciones()

    net = Network(
        height="650px",
        width="100%",
        bgcolor=FONDO,
        directed=False,
        notebook=False,
        cdn_resources="in_line",  # HTML autocontenido (mejor para embeber)
    )
    # Nota: NO se pasa font_color aqui. pyvis, si recibe font_color en el
    # constructor de Network, lo reenvia a CADA nodo y SOBREESCRIBE por
    # completo el dict "font" indicado en add_node (incluido el tamano),
    # dejando solo el color. Por eso el tamano de fuente se define abajo,
    # nodo por nodo, en el propio add_node.
    # net.barnes_hut() configuraría solo la física; como set_options() más
    # abajo REEMPLAZA toda la configuración (no la combina), replicamos aquí
    # una version mas COMPACTA que los valores por defecto (menor repulsion y
    # longitud de resorte) para que la vista inicial ya muestre los nodos
    # bastante grandes sin necesidad de hacer zoom manual, junto con los
    # controles de navegación (botones +/-/casa) y un zoom por rueda menos
    # agresivo.
    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -30000,
          "centralGravity": 0.35,
          "springLength": 160,
          "springConstant": 0.02,
          "damping": 0.15,
          "avoidOverlap": 0.2
        },
        "stabilization": {"iterations": 150}
      },
      "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": {"enabled": true, "bindToWindow": false},
        "zoomSpeed": 0.35
      }
    }
    """)

    canceres_agregados = set()

    for nombre, mut in mutaciones.items():
        # Nodo de mutacion
        tooltip_mut = ("%s | %s%d%s | dominio: %s | casos IARC: %s"
                       % (nombre, mut["aa_original"], mut["posicion"],
                          mut["aa_mutado"], mut["dominio"], mut["casos_iarc"]))
        net.add_node(
            nombre,
            label=nombre,
            title=tooltip_mut,
            color=COLOR_MUTACION,
            size=46,
            shape="dot",
            font={"size": 26, "color": "#33465c", "strokeWidth": 3, "strokeColor": "#ffffff"},
        )

        # Nodos de cancer + aristas
        for cancer in mut.get("canceres", []):
            if cancer not in canceres_agregados:
                url = URLS_CANCER.get(cancer)
                titulo = "Tipo de cáncer: %s" % cancer
                if url:
                    titulo += " — clic para leer en cancer.gov (NCI)"
                net.add_node(
                    cancer,
                    label=cancer,
                    title=titulo,
                    color=COLOR_CANCER,
                    size=24,
                    shape="dot",
                    url=url,  # atributo propio, leído por el manejador de clic (JS)
                    font={"size": 18, "color": "#33465c", "strokeWidth": 3, "strokeColor": "#ffffff"},
                )
                canceres_agregados.add(cancer)
            net.add_edge(nombre, cancer, color=COLOR_ARISTA)

    # Guardar en un HTML temporal.
    # Nota: net.save_graph() escribe con la codificacion por defecto de Windows
    # (cp1252) y falla con caracteres Unicode del template de pyvis. Por eso
    # generamos el HTML como string y lo escribimos nosotros en UTF-8.
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", delete=False, encoding="utf-8"
    )
    ruta = tmp.name
    try:
        html = net.generate_html(notebook=False)
    except TypeError:
        html = net.generate_html()

    # Estilo de los botones de navegacion (+/-/casa) para que combinen con la
    # estetica academica de la app. Los iconos de vis.js son PNG verdes
    # incrustados (no se puede cambiar su color con background-color), asi que
    # se usa un filtro CSS para llevarlos a la paleta azul/gris del resto de
    # la interfaz. Los selectores igualan la especificidad de vis-network.css
    # (que antepone "div.vis-network div.vis-navigation div.vis-button") para
    # poder sobreescribirlo.
    estilo_botones = """
    <style>
      div.vis-network div.vis-navigation div.vis-button {
          background-color: #ffffff !important;
          border: 1px solid #c3ccd6 !important;
          border-radius: 50% !important;
          box-shadow: none !important;
          filter: hue-rotate(95deg) saturate(0.45) brightness(0.72);
      }
      div.vis-network div.vis-navigation div.vis-button:hover {
          border-color: #1f3a5f !important;
          background-color: #f2f5f8 !important;
          box-shadow: none !important;
      }
      div.vis-network div.vis-navigation div.vis-button:active {
          box-shadow: none !important;
      }
    </style>
    """
    if "</head>" in html:
        html = html.replace("</head>", estilo_botones + "</head>", 1)
    else:
        html = estilo_botones + html

    # Zoom inicial. Por defecto vis.js ajusta la vista para que "quepan" TODOS
    # los nodos, lo que deja el grafo diminuto y las etiquetas ilegibles hasta
    # que el usuario hace zoom manualmente. Este script espera a que la
    # variable global "network" (creada por el template de pyvis) exista,
    # deja que la física se estabilice y luego acerca la camara un poco mas
    # (manteniendo el mismo centro) para que los nombres se lean sin esfuerzo.
    script_zoom_inicial = """
    <script>
      (function ajustarZoomInicial() {
        if (typeof network === "undefined" || !network) {
          setTimeout(ajustarZoomInicial, 60);
          return;
        }
        var yaAplicado = false;
        function acercar() {
          if (yaAplicado) { return; }
          yaAplicado = true;
          var centro = network.getViewPosition();
          var escala = network.getScale();
          network.moveTo({position: centro, scale: escala * 1.8, animation: false});
        }
        network.once("stabilizationIterationsDone", function () {
          network.fit({animation: false});
          acercar();
        });
        // Respaldo por si el evento ya ocurrio antes de registrar el listener.
        setTimeout(acercar, 1000);

        // Clic en un nodo de cancer -> abre su pagina en cancer.gov (NCI).
        network.on("click", function (params) {
          if (params.nodes && params.nodes.length > 0) {
            var nodo = network.body.data.nodes.get(params.nodes[0]);
            if (nodo && nodo.url) {
              window.open(nodo.url, "_blank", "noopener");
            }
          }
        });
        // Cursor de mano al pasar sobre un nodo con enlace.
        network.on("hoverNode", function (params) {
          var nodo = network.body.data.nodes.get(params.node);
          var cont = network.canvas && network.canvas.frame ? network.canvas.frame : null;
          if (cont) { cont.style.cursor = (nodo && nodo.url) ? "pointer" : "default"; }
        });
        network.on("blurNode", function () {
          var cont = network.canvas && network.canvas.frame ? network.canvas.frame : null;
          if (cont) { cont.style.cursor = "default"; }
        });
      })();
    </script>
    """
    if "</body>" in html:
        html = html.replace("</body>", script_zoom_inicial + "</body>", 1)
    else:
        html = html + script_zoom_inicial

    tmp.write(html)
    tmp.close()
    return ruta


if __name__ == "__main__":
    ruta = construir_grafo()
    print("Grafo generado en:", ruta)
    print("Tamano:", os.path.getsize(ruta), "bytes")

# -*- coding: utf-8 -*-
"""
Motor de calculo e interpretacion biofisica de mutaciones en TP53 (p53).

Herramienta DIDACTICA de interpretacion heuristica. No es un predictor clinico.
Los datos biologicos provienen de archivos JSON curados manualmente y verificados
en IARC, ClinVar y UniProt/Pfam.
"""

import json
import math
import os

# ---------------------------------------------------------------------------
# Rutas de datos (relativas a este archivo, robustas ante el cwd)
# ---------------------------------------------------------------------------
_BASE = os.path.dirname(os.path.abspath(__file__))
_RUTA_MUTACIONES = os.path.join(_BASE, "data", "mutaciones.json")
_RUTA_DOMINIOS = os.path.join(_BASE, "data", "dominios.json")
_RUTA_GEN = os.path.join(_BASE, "data", "gen_tp53.json")

# ---------------------------------------------------------------------------
# Tabla de propiedades fisicoquimicas de los 20 aminoacidos estandar.
#   carga:          -1, 0, +1 (His se toma como 0)
#   hidrofobicidad: escala Kyte-Doolittle
#   volumen:        volumen molecular (angstrom^3), escala de Zamyatnin
#   polaridad:      "polar" / "no_polar"
# Codigos de 3 letras.
# ---------------------------------------------------------------------------
AMINOACIDOS = {
    "Ala": {"carga": 0,  "hidrofobicidad": 1.8,  "volumen": 89,  "polaridad": "no_polar"},
    "Arg": {"carga": 1,  "hidrofobicidad": -4.5, "volumen": 173, "polaridad": "polar"},
    "Asn": {"carga": 0,  "hidrofobicidad": -3.5, "volumen": 114, "polaridad": "polar"},
    "Asp": {"carga": -1, "hidrofobicidad": -3.5, "volumen": 111, "polaridad": "polar"},
    "Cys": {"carga": 0,  "hidrofobicidad": 2.5,  "volumen": 109, "polaridad": "polar"},
    "Gln": {"carga": 0,  "hidrofobicidad": -3.5, "volumen": 144, "polaridad": "polar"},
    "Glu": {"carga": -1, "hidrofobicidad": -3.5, "volumen": 138, "polaridad": "polar"},
    "Gly": {"carga": 0,  "hidrofobicidad": -0.4, "volumen": 60,  "polaridad": "no_polar"},
    "His": {"carga": 0,  "hidrofobicidad": -3.2, "volumen": 153, "polaridad": "polar"},
    "Ile": {"carga": 0,  "hidrofobicidad": 4.5,  "volumen": 167, "polaridad": "no_polar"},
    "Leu": {"carga": 0,  "hidrofobicidad": 3.8,  "volumen": 167, "polaridad": "no_polar"},
    "Lys": {"carga": 1,  "hidrofobicidad": -3.9, "volumen": 169, "polaridad": "polar"},
    "Met": {"carga": 0,  "hidrofobicidad": 1.9,  "volumen": 163, "polaridad": "no_polar"},
    "Phe": {"carga": 0,  "hidrofobicidad": 2.8,  "volumen": 190, "polaridad": "no_polar"},
    "Pro": {"carga": 0,  "hidrofobicidad": -1.6, "volumen": 113, "polaridad": "no_polar"},
    "Ser": {"carga": 0,  "hidrofobicidad": -0.8, "volumen": 89,  "polaridad": "polar"},
    "Thr": {"carga": 0,  "hidrofobicidad": -0.7, "volumen": 116, "polaridad": "polar"},
    "Trp": {"carga": 0,  "hidrofobicidad": -0.9, "volumen": 227, "polaridad": "no_polar"},
    "Tyr": {"carga": 0,  "hidrofobicidad": -1.3, "volumen": 194, "polaridad": "polar"},
    "Val": {"carga": 0,  "hidrofobicidad": 4.2,  "volumen": 140, "polaridad": "no_polar"},
}

# Códigos de 1 letra <-> 3 letras (para leer la secuencia canónica).
UNA_A_TRES = {
    "A": "Ala", "R": "Arg", "N": "Asn", "D": "Asp", "C": "Cys",
    "Q": "Gln", "E": "Glu", "G": "Gly", "H": "His", "I": "Ile",
    "L": "Leu", "K": "Lys", "M": "Met", "F": "Phe", "P": "Pro",
    "S": "Ser", "T": "Thr", "W": "Trp", "Y": "Tyr", "V": "Val",
}
TRES_A_UNA = {v: k for k, v in UNA_A_TRES.items()}


# ---------------------------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------------------------
def cargar_mutaciones():
    with open(_RUTA_MUTACIONES, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_dominios():
    with open(_RUTA_DOMINIOS, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_gen():
    with open(_RUTA_GEN, "r", encoding="utf-8") as f:
        return json.load(f)


def aa_tres_en_posicion(pos):
    """Devuelve el código de 3 letras del aminoácido en la posición `pos`
    (1-indexado) de la secuencia canónica, o None si está fuera de rango.
    """
    seq = cargar_gen()["secuencia_aa"]
    if 1 <= pos <= len(seq):
        return UNA_A_TRES.get(seq[pos - 1])
    return None


def dominio_en_posicion(pos):
    """Devuelve (clave, info) del dominio que contiene la posición `pos`, o
    (None, {}) si la posición no cae en ningún dominio anotado.
    """
    for clave, d in cargar_dominios().items():
        if d.get("inicio") and d.get("fin") and d["inicio"] <= pos <= d["fin"]:
            return clave, d
    return None, {}


def mutacion_catalogada(pos, aa_mutado_tres):
    """Si (posición, aminoácido mutado) coincide con una de las mutaciones
    curadas, devuelve su nombre (p. ej. 'R175H'); si no, None.
    """
    for nombre, m in cargar_mutaciones().items():
        if m["posicion"] == pos and m["aa_mutado"] == aa_mutado_tres:
            return nombre
    return None


# ---------------------------------------------------------------------------
# 1. Cambios fisicoquimicos
# ---------------------------------------------------------------------------
def calcular_cambios(aa_original, aa_mutado):
    """Delta de carga, hidrofobicidad y volumen entre dos aminoacidos.

    Los deltas se calculan como (mutado - original) y se redondean a 2 decimales
    para evitar ruido de punto flotante.
    """
    o = AMINOACIDOS[aa_original]
    m = AMINOACIDOS[aa_mutado]

    delta_carga = round(m["carga"] - o["carga"], 2)
    delta_hidrofobicidad = round(m["hidrofobicidad"] - o["hidrofobicidad"], 2)
    delta_volumen = round(m["volumen"] - o["volumen"], 2)

    return {
        "delta_carga": delta_carga,
        "delta_hidrofobicidad": delta_hidrofobicidad,
        "delta_volumen": delta_volumen,
        "polaridad_original": o["polaridad"],
        "polaridad_mutada": m["polaridad"],
        "cambia_polaridad": o["polaridad"] != m["polaridad"],
    }


# ---------------------------------------------------------------------------
# 2. Indice heuristico de impacto biofisico
#
# Pesos de diseño pedagógico (NO calibrados estadísticamente contra un set de
# validación clínica): cada uno se justifica con un argumento biofísico
# concreto, pero los números exactos son una decisión de diseño de este
# proyecto, inspirada en la lógica general de SIFT/PolyPhen — no están
# tomados de una publicación con esos pesos exactos. Ver README / defensa
# para la justificación de cada peso.
# ---------------------------------------------------------------------------
PESO_CARGA = 3          # union proteina-ADN es electrostatica: perder carga
                         # positiva (contacto directo con fosfatos) es lo mas grave
PESO_HIDROFOBICIDAD = 2  # cambio de empaquetamiento interno / exposicion al solvente
PESO_VOLUMEN = 2         # riesgo de choque esterico o cavidad
PESO_POLARIDAD = 2       # incompatibilidad categorica con el entorno (enterrado/expuesto)
PESO_DOMINIO_UNION_ADN = 2        # la mayoria de mutaciones clinicas de TP53 caen aqui (IARC)
PESO_DOMINIO_OLIGOMERIZACION = 1  # interfaz funcional, pero mas localizada
PESO_CONSERVADO = 1      # bonus simple, no es un score de alineamiento evolutivo real

UMBRAL_CARGA = 1
UMBRAL_HIDROFOBICIDAD = 2
UMBRAL_VOLUMEN = 50

# Maximo teorico DERIVADO de los pesos de arriba (no escrito a mano en cada
# pagina): así nunca queda desincronizado si se ajustan los pesos.
SCORE_MAXIMO = (
    PESO_CARGA + PESO_HIDROFOBICIDAD + PESO_VOLUMEN + PESO_POLARIDAD
    + max(PESO_DOMINIO_UNION_ADN, PESO_DOMINIO_OLIGOMERIZACION) + PESO_CONSERVADO
)


def calcular_impacto(cambios, dominio, conservado):
    """Indice heuristico de impacto biofisico.

    Inspirado en la logica de predictores tipo SIFT/PolyPhen (conservacion +
    severidad del cambio fisicoquimico), pero deliberadamente SIMPLIFICADO y
    transparente para fines didacticos. No es un predictor clinico.

    Devuelve (nivel, score). El score maximo posible es SCORE_MAXIMO.
    """
    score = 0

    if abs(cambios["delta_carga"]) >= UMBRAL_CARGA:
        score += PESO_CARGA
    if abs(cambios["delta_hidrofobicidad"]) >= UMBRAL_HIDROFOBICIDAD:
        score += PESO_HIDROFOBICIDAD
    if abs(cambios["delta_volumen"]) >= UMBRAL_VOLUMEN:
        score += PESO_VOLUMEN
    if cambios["cambia_polaridad"]:
        score += PESO_POLARIDAD

    if dominio == "union_ADN":
        score += PESO_DOMINIO_UNION_ADN
    elif dominio == "oligomerizacion":
        score += PESO_DOMINIO_OLIGOMERIZACION

    if conservado:
        score += PESO_CONSERVADO

    if score <= 3:
        nivel = "Bajo"
    elif score <= 7:
        nivel = "Moderado"
    else:
        nivel = "Alto"

    return nivel, score


# ---------------------------------------------------------------------------
# 3. Interpretacion completa de una mutacion
# ---------------------------------------------------------------------------
def interpretar_mutacion(nombre):
    """Carga la mutacion y su dominio, calcula cambios e impacto y devuelve un
    diccionario completo con todos los datos.
    """
    mutaciones = cargar_mutaciones()
    dominios = cargar_dominios()

    if nombre not in mutaciones:
        raise KeyError("Mutacion no encontrada: %s" % nombre)

    mut = mutaciones[nombre]
    dominio_clave = mut["dominio"]
    dominio = dominios.get(dominio_clave, {})

    cambios = calcular_cambios(mut["aa_original"], mut["aa_mutado"])
    nivel, score = calcular_impacto(cambios, dominio_clave, mut["conservado"])

    resultado = dict(mut)  # copia de todos los campos de la mutacion
    resultado.update({
        "dominio_clave": dominio_clave,
        "dominio_info": dominio,
        "cambios": cambios,
        "nivel_impacto": nivel,
        "score_impacto": score,
    })
    return resultado


# ---------------------------------------------------------------------------
# 4. Texto interpretativo automatico
# ---------------------------------------------------------------------------
def generar_interpretacion(resultado):
    """Genera un parrafo explicativo del mecanismo biofisico segun los cambios."""
    c = resultado["cambios"]
    dominio_clave = resultado["dominio_clave"]
    nombre_dominio = resultado.get("dominio_info", {}).get("nombre", dominio_clave)
    frases = []

    # --- Carga ---
    if c["delta_carga"] < 0:
        txt = ("La mutación elimina %s unidad(es) de carga positiva "
               "(Δcarga = %+.2f)." % (abs(int(c["delta_carga"])), c["delta_carga"]))
        if dominio_clave == "union_ADN":
            txt += (" En el dominio de unión al ADN esta carga positiva es la que "
                    "atrae al esqueleto fosfato del ADN, cargado negativamente; su "
                    "pérdida debilita directamente el contacto proteína-ADN.")
        frases.append(txt)
    elif c["delta_carga"] > 0:
        frases.append("La mutación agrega carga positiva (Δcarga = %+.2f), lo que "
                      "puede introducir repulsiones o contactos electrostáticos anómalos."
                      % c["delta_carga"])
    else:
        frases.append("La carga neta del residuo no cambia (Δcarga = 0).")

    # --- Hidrofobicidad ---
    if abs(c["delta_hidrofobicidad"]) >= 2:
        direccion = "más hidrofóbico" if c["delta_hidrofobicidad"] > 0 else "más hidrofílico"
        txt = ("El residuo se vuelve %s (Δhidrofobicidad = %+.2f, escala "
               "Kyte-Doolittle)." % (direccion, c["delta_hidrofobicidad"]))
        if dominio_clave == "oligomerizacion":
            txt += (" En el dominio de oligomerización, alterar la hidrofobicidad de la "
                    "interfaz perturba el empaquetamiento del tetrámero.")
        frases.append(txt)

    # --- Volumen ---
    if c["delta_volumen"] >= 50:
        frases.append("El aminoácido mutante es mucho más voluminoso (Δvolumen = "
                      "%+.2f Å³), lo que puede provocar colisiones estéricas que "
                      "distorsionan el plegamiento local." % c["delta_volumen"])
    elif c["delta_volumen"] <= -50:
        frases.append("El aminoácido mutante es mucho más pequeño (Δvolumen = "
                      "%+.2f Å³), lo que puede dejar una cavidad interna que "
                      "desestabiliza el núcleo de la proteína." % c["delta_volumen"])

    # --- Polaridad ---
    if c["cambia_polaridad"]:
        frases.append("Además hay un cambio de polaridad (%s → %s), que altera el tipo "
                      "de interacciones que el residuo puede formar en su entorno."
                      % (c["polaridad_original"], c["polaridad_mutada"]))

    # --- Efecto dominante negativo ---
    dne = str(resultado.get("dne", "")).lower()
    if dne == "yes":
        frases.append("Por su efecto dominante negativo, la subunidad mutante secuestra "
                      "a las subunidades normales dentro del tetrámero, inactivando "
                      "también al alelo sano.")
    elif dne == "moderate":
        frases.append("Presenta un efecto dominante negativo moderado sobre el tetrámero.")

    return " ".join(frases)


# ---------------------------------------------------------------------------
# 5. Implicancias (clinica, terapeutica, conceptual)
# ---------------------------------------------------------------------------
def generar_implicancias(resultado):
    """Devuelve 3 implicancias como lista de tuplas (titulo, texto)."""
    dne = str(resultado.get("dne", "")).lower()
    afinidad = resultado.get("afinidad_ADN", {})
    clasif = afinidad.get("clasificacion", "")
    perdida_carga = resultado["cambios"]["delta_carga"] < 0

    # Clínica
    if dne == "yes":
        clinica = ("El efecto dominante negativo implica que basta una copia mutada para "
                   "comprometer la función supresora, asociado a un curso típicamente más "
                   "agresivo. Registrada %s veces en IARC (%s)."
                   % (resultado.get("casos_iarc", "?"), resultado.get("clinvar_germinal", "")))
    elif dne == "moderate":
        clinica = ("El efecto dominante negativo moderado matiza el impacto sobre el "
                   "tetrámero. Registrada %s veces en IARC (%s)."
                   % (resultado.get("casos_iarc", "?"), resultado.get("clinvar_germinal", "")))
    else:
        clinica = ("Mutación patogénica registrada %s veces en IARC (%s)."
                   % (resultado.get("casos_iarc", "?"), resultado.get("clinvar_germinal", "")))

    # Terapéutica
    if clasif == "contact" and perdida_carga:
        terapeutica = ("Al ser un defecto de contacto directo (el pliegue se conserva pero "
                       "se pierde la carga que toca el ADN), es un candidato conceptual a "
                       "estrategias que restauran la función tipo PRIMA-1/APR-246, que "
                       "buscan reactivar p53 mutante.")
    elif clasif == "structural":
        terapeutica = ("Al ser un defecto estructural (desestabilización del pliegue), el "
                       "objetivo terapéutico conceptual son moléculas chaperonas que "
                       "reestabilicen el dominio, más que restaurar un único contacto.")
    else:
        terapeutica = ("El mecanismo condiciona la estrategia terapéutica: distinguir "
                       "defecto de contacto vs. estructural orienta si conviene restaurar "
                       "un contacto puntual o reestabilizar el pliegue.")

    # Conceptual
    conceptual = ("Ilustra que «patogénica» no es una etiqueta única: el MISMO fenotipo "
                  "(pérdida de unión al ADN) puede surgir de mecanismos biofísicos distintos "
                  "(contacto vs. estructural), y entender el porqué es clave para razonar "
                  "sobre la proteína, no solo clasificarla.")

    return [
        ("Implicancia clínica", clinica),
        ("Implicancia terapéutica", terapeutica),
        ("Implicancia conceptual", conceptual),
    ]


# ---------------------------------------------------------------------------
# 6. Texto sobre la estabilidad termodinámica del pliegue (ΔΔG)
# ---------------------------------------------------------------------------
def generar_texto_estabilidad(resultado):
    """Párrafo sobre la desestabilización del pliegue (ΔΔG) y su conexión con
    el mecanismo. Usa los datos verificados de `estabilidad` de la mutación y la
    referencia del tipo salvaje (gen_tp53.json). Devuelve texto explicativo.
    """
    est = resultado.get("estabilidad", {})
    ddg = est.get("ddG_kcal_mol")
    if ddg is None:
        return "Datos de estabilidad no disponibles (por verificar)."

    prec = est.get("ddG_precision", "")
    clasif = resultado.get("afinidad_ADN", {}).get("clasificacion", "")
    tm_mut = est.get("tm_celsius")

    wt = cargar_gen().get("estabilidad_wt", {})
    tm_wt = wt.get("tm_celsius")
    t_cuerpo = wt.get("temperatura_corporal_celsius", 37)

    signo = "más de" if prec == "límite inferior" else "cerca de"
    frases = [
        "La mutación desestabiliza el plegamiento del dominio en %s %.0f kcal/mol (%s)."
        % (signo, ddg, prec)
    ]

    if tm_wt:
        frases.append(
            "El dominio silvestre es solo marginalmente estable (Tm ≈ %.1f °C, apenas "
            "por encima de los %d °C corporales), así que una pérdida de esta magnitud "
            "lo empuja hacia el desplegamiento a temperatura fisiológica."
            % (tm_wt, t_cuerpo)
        )

    if ddg >= 3:
        frases.append(
            "Es una de las desestabilizaciones más severas: a 37 °C el dominio queda "
            "mayormente desplegado y no puede unir ADN."
        )
    elif ddg >= 2:
        frases.append(
            "Es una desestabilización moderada, suficiente para comprometer la función "
            "a temperatura corporal."
        )
    else:
        frases.append(
            "Es una desestabilización leve, pero se suma a los demás cambios locales "
            "del residuo."
        )

    if clasif == "contact" and tm_mut:
        frases.append(
            "Aunque su defecto principal es de contacto directo con el ADN, su Tm baja "
            "a %.1f °C: por eso une a temperaturas más bajas pero pierde la unión a "
            "37 °C (ver la sección de dependencia de temperatura)." % tm_mut
        )
    elif clasif == "structural":
        frases.append(
            "Aquí la desestabilización del pliegue ES el mecanismo: el residuo no toca "
            "el ADN, pero sin un pliegue estable no hay unión posible."
        )

    return " ".join(frases)


# ---------------------------------------------------------------------------
# 7. Estabilidad frente a la temperatura (curva de plegamiento)
# ---------------------------------------------------------------------------
def fraccion_plegada(temp_c, tm_c, cooperatividad=1.8):
    """Fracción de proteína plegada a una temperatura dada, según un modelo
    de transición de dos estados (sigmoide centrada en el Tm MEDIDO).

    Es un MODELO ilustrativo: el único dato experimental es el Tm (centro de la
    curva); la forma sigmoide es la del desplegamiento cooperativo estándar.
    `cooperatividad` es el ancho aproximado de la transición en °C.
    """
    return 1.0 / (1.0 + math.exp((temp_c - tm_c) / cooperatividad))


def generar_texto_temperatura(resultado):
    """Texto que explica el comportamiento frente a la temperatura de la mutación,
    usando su Tm medido y/o su dependencia_temperatura documentada; para las que
    solo tienen ΔΔG, lo describe cualitativamente sin inventar un Tm.
    """
    est = resultado.get("estabilidad", {})
    tm = est.get("tm_celsius")
    ddg = est.get("ddG_kcal_mol")
    dep = resultado.get("dependencia_temperatura")
    clasif = resultado.get("afinidad_ADN", {}).get("clasificacion", "")

    if dep:
        une_hasta = dep.get("une_por_debajo_de_celsius", 33)
        no_une = dep.get("no_une_a_celsius", 37)
        return (
            "R248W solo cambió su residuo de contacto, pero su Tm baja a %s °C, apenas "
            "por encima de los %s °C corporales. Por eso a temperaturas de ~25-%s °C el "
            "dominio se pliega y une el ADN, mientras que a %s °C entra en su transición "
            "de desplegamiento y pierde la unión. Es el ejemplo más nítido de que la "
            "función depende de la estabilidad térmica del pliegue."
            % (tm, no_une, une_hasta, no_une)
        )
    if clasif == "structural" and ddg is not None and ddg >= 2:
        return (
            "Con una desestabilización de %s%.0f kcal/mol, su curva de plegamiento se "
            "desplaza hacia temperaturas más bajas que la del tipo salvaje: a 37 °C el "
            "dominio ya está mayormente desplegado y la unión al ADN está abolida. Su Tm "
            "exacto no está reportado (por verificar), así que abajo solo se grafica la "
            "curva del tipo salvaje como referencia."
            % (">" if est.get("ddG_precision") == "límite inferior" else "≈", ddg)
        )
    if ddg is not None:
        return (
            "Su desestabilización es leve (≈%.0f kcal/mol), así que su Tm cae poco respecto "
            "al tipo salvaje; su defecto principal no es térmico sino el cambio local en el "
            "residuo. Su Tm exacto no está reportado (por verificar)." % ddg
        )
    return "Datos de estabilidad térmica no disponibles (por verificar)."


# ---------------------------------------------------------------------------
# Prueba rapida
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # La consola de Windows usa cp1252 por defecto y no imprime acentos/Δ/Å.
    # Forzamos UTF-8 en la salida para la prueba rapida.
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    for nombre in cargar_mutaciones():
        r = interpretar_mutacion(nombre)
        print("=" * 70)
        print("%s  (%s%d%s)  dominio=%s"
              % (r["nombre"], r["aa_original"], r["posicion"], r["aa_mutado"],
                 r["dominio_clave"]))
        print("  Cambios:", r["cambios"])
        print("  Impacto: %s (score %d/%d)" % (r["nivel_impacto"], r["score_impacto"], SCORE_MAXIMO))
        print("  Afinidad:", r["afinidad_ADN"]["clasificacion"])
        print("  Interpretacion:", generar_interpretacion(r))

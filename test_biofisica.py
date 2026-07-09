# -*- coding: utf-8 -*-
"""
Tests del motor biofisico (biofisica.py).

Se escriben con unittest (libreria estandar) para poder ejecutarlos sin
instalar nada:  py -m unittest test_biofisica -v
Tambien son descubribles por pytest si esta disponible:  py -m pytest
"""

import unittest

import biofisica as bf


class TestCalcularCambios(unittest.TestCase):
    def test_delta_carga_arg_a_his(self):
        # Arg (+1) -> His (0): se pierde una carga positiva.
        c = bf.calcular_cambios("Arg", "His")
        self.assertEqual(c["delta_carga"], -1)

    def test_delta_volumen_signo(self):
        # Trp es mucho mas voluminoso que Arg.
        c = bf.calcular_cambios("Arg", "Trp")
        self.assertGreater(c["delta_volumen"], 0)

    def test_cambio_de_polaridad(self):
        # Arg (polar) -> Trp (no_polar): cambia la polaridad.
        c = bf.calcular_cambios("Arg", "Trp")
        self.assertTrue(c["cambia_polaridad"])
        self.assertEqual(c["polaridad_original"], "polar")
        self.assertEqual(c["polaridad_mutada"], "no_polar")

    def test_sin_cambio_mismo_aminoacido(self):
        c = bf.calcular_cambios("Ala", "Ala")
        self.assertEqual(c["delta_carga"], 0)
        self.assertEqual(c["delta_volumen"], 0)
        self.assertFalse(c["cambia_polaridad"])


class TestCalcularImpacto(unittest.TestCase):
    def test_score_no_supera_el_maximo(self):
        # El cambio mas agresivo posible dentro del dominio de union al ADN
        # no debe superar SCORE_MAXIMO.
        cambios = bf.calcular_cambios("Arg", "Trp")
        _, score = bf.calcular_impacto(cambios, "union_ADN", conservado=True)
        self.assertLessEqual(score, bf.SCORE_MAXIMO)

    def test_nivel_bajo_para_cambio_leve(self):
        # Sustitucion conservativa fuera de dominio: impacto bajo.
        cambios = bf.calcular_cambios("Leu", "Ile")
        nivel, _ = bf.calcular_impacto(cambios, None, conservado=False)
        self.assertEqual(nivel, "Bajo")

    def test_dominio_union_pesa_mas_que_oligomerizacion(self):
        cambios = bf.calcular_cambios("Gly", "Ala")
        _, s_union = bf.calcular_impacto(cambios, "union_ADN", conservado=False)
        _, s_oligo = bf.calcular_impacto(cambios, "oligomerizacion", conservado=False)
        self.assertGreater(s_union, s_oligo)


class TestConsistenciaDatos(unittest.TestCase):
    def test_sin_inconsistencias(self):
        problemas = bf.verificar_consistencia_datos()
        self.assertEqual(problemas, [], "Inconsistencias: %s" % problemas)

    def test_aa_original_coincide_con_secuencia(self):
        # Verificacion directa por si el catalogo crece.
        for nombre, m in bf.cargar_mutaciones().items():
            aa_seq = bf.aa_tres_en_posicion(m["posicion"])
            self.assertEqual(
                aa_seq, m["aa_original"],
                "%s: aa_original=%s pero la secuencia tiene %s" % (nombre, m["aa_original"], aa_seq),
            )

    def test_dominio_coincide_con_posicion(self):
        for nombre, m in bf.cargar_mutaciones().items():
            clave_real, _ = bf.dominio_en_posicion(m["posicion"])
            if clave_real is not None:
                self.assertEqual(
                    clave_real, m["dominio"],
                    "%s: dominio declarado %s pero la posicion cae en %s"
                    % (nombre, m["dominio"], clave_real),
                )

    def test_r282w_esta_en_union_adn(self):
        # Regresion explicita del bug corregido (antes decia oligomerizacion).
        m = bf.cargar_mutaciones()["R282W"]
        self.assertEqual(m["dominio"], "union_ADN")


class TestInterpretarMutacion(unittest.TestCase):
    def test_todas_las_mutaciones_interpretan(self):
        for nombre in bf.cargar_mutaciones():
            r = bf.interpretar_mutacion(nombre)
            self.assertIn(r["nivel_impacto"], ("Bajo", "Moderado", "Alto"))
            self.assertIsInstance(bf.generar_interpretacion(r), str)

    def test_r282w_no_menciona_tetramero_en_interpretacion(self):
        # Al estar en union_ADN, el texto ya no debe hablar de empaquetamiento
        # del tetramero (eso era el sintoma del bug de dominio).
        r = bf.interpretar_mutacion("R282W")
        texto = bf.generar_interpretacion(r)
        self.assertNotIn("empaquetamiento del tetrámero", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)

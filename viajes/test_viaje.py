import unittest

class Viaje:
    def calcular_diferencias_gastos(self, valor_cop: float, presupuesto_diario: float) -> float:
        return presupuesto_diario - valor_cop


class TestDiferenciaPresupuesto(unittest.TestCase):

    def setUp(self):
        self.viaje = Viaje()

    def test_diferencia_positiva_si_gasto_menor(self):
        """Debe mostrar diferencia positiva si se gasta menos del presupuesto"""
        resultado = self.viaje.calcular_diferencias_gastos(80000, 100000)
        self.assertGreater(resultado, 0)

    def test_diferencia_cero_si_gasto_igual(self):
        """Debe mostrar diferencia cero si se gasta exactamente el presupuesto"""
        resultado = self.viaje.calcular_diferencias_gastos(100000, 100000)
        self.assertEqual(resultado, 0)

    def test_diferencia_negativa_si_gasto_mayor(self):
        """Debe mostrar diferencia negativa si se gasta más del presupuesto"""
        resultado = self.viaje.calcular_diferencias_gastos(120000, 100000)
        self.assertLess(resultado, 0)


if __name__ == '__main__':
    unittest.main()

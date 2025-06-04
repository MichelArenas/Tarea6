"""
Módulo de pruebas unitarias para la clase Viaje.

Incluye la implementación de la clase Viaje y una batería de pruebas
que validan el cálculo de la diferencia entre el presupuesto diario
y los gastos realizados durante el viaje.
"""

import unittest

class Viaje:
    """
    Representa un viaje con funcionalidad para calcular la diferencia
    entre el presupuesto diario y el gasto registrado.
    """

    def calcular_diferencias_gastos(self, valor_cop: float, presupuesto_diario: float) -> float:
        """
        Calcula la diferencia entre el presupuesto diario y el gasto realizado.

        Args:
            valor_cop (float): Valor del gasto en pesos colombianos.
            presupuesto_diario (float): Monto asignado como presupuesto para ese día.

        Returns:
            float: Diferencia entre presupuesto y gasto. Positiva si se ahorra,
                   cero si el gasto es exacto, negativa si se sobrepasa.
        """
        return presupuesto_diario - valor_cop


class TestDiferenciaPresupuesto(unittest.TestCase):
    """
    Conjunto de pruebas unitarias para validar el método calcular_diferencias_gastos
    de la clase Viaje.
    """

    def setUp(self):
        """Inicializa una instancia de Viaje para usar en las pruebas."""
        self.viaje = Viaje()

    def test_diferencia_positiva_si_gasto_menor(self):
        """Debe mostrar diferencia positiva si se gasta menos del presupuesto."""
        resultado = self.viaje.calcular_diferencias_gastos(80000, 100000)
        self.assertGreater(resultado, 0)

    def test_diferencia_cero_si_gasto_igual(self):
        """Debe mostrar diferencia cero si se gasta exactamente el presupuesto."""
        resultado = self.viaje.calcular_diferencias_gastos(100000, 100000)
        self.assertEqual(resultado, 0)

    def test_diferencia_negativa_si_gasto_mayor(self):
        """Debe mostrar diferencia negativa si se gasta más del presupuesto."""
        resultado = self.viaje.calcular_diferencias_gastos(120000, 100000)
        self.assertLess(resultado, 0)


if __name__ == '__main__':
    unittest.main()

import unittest
from datetime import date
from Tarea6.controladores.control_gasto import ControlGasto
from Tarea6.modelos.viaje import Viaje
from Tarea6.modelos.gasto import Gasto
from Tarea6.enums.medio_pago import MedioPago
from Tarea6.enums.tipo_gasto import TipoGasto
from Tarea6.enums.tipo_viaje import TipoViaje
from Tarea6.modelos.destino import Destino


class TestCalcularDiferenciaPresupuesto(unittest.TestCase):
    """
    Pruebas unitarias para el método calcular_diferencia_presupuesto del controlador de gastos.
    Se evalúan distintos escenarios para validar la lógica de diferencia entre presupuesto
    y gastos diarios en pesos colombianos.
    """

    def crear_control_gasto(self, valor_cop, presupuesto_diario):
        """
        Crea un objeto ControlGasto con un gasto registrado en una fecha específica.

        Args:
            valor_cop (float): Valor del gasto en COP. Si es None, no se registra ningún gasto.
            presupuesto_diario (float): Presupuesto diario asignado al viaje.

        Returns:
            ControlGasto: Instancia inicializada para pruebas.
        """
        viaje = Viaje(
            fecha_inicio=date(2025, 6, 1),
            fecha_fin=date(2025, 6, 10),
            presupuesto_diario=presupuesto_diario,
            destino=Destino("Bogotá", "Cundinamarca", "Colombia", "COP"),
            tipo_viaje=TipoViaje.NACIONAL
        )
        control = ControlGasto(viaje, None)

        if valor_cop is not None:
            gasto = Gasto(
                fecha=date(2025, 6, 2),
                valor=valor_cop,
                medio_pago=MedioPago.EFECTIVO,
                tipo_gasto=TipoGasto.ALIMENTACION,
                valor_cop=valor_cop
            )
            viaje.agregar_gasto(gasto)

        return control

    def test_1_gasto_menor_presupuesto(self):
        """Debe retornar diferencia positiva si el gasto es menor al presupuesto."""
        control = self.crear_control_gasto(80000, 100000)
        self.assertEqual(control.calcular_diferencia_presupuesto(date(2025, 6, 2)), 20000)

    def test_2_gasto_igual_presupuesto(self):
        """Debe retornar cero si el gasto es igual al presupuesto."""
        control = self.crear_control_gasto(100000, 100000)
        self.assertEqual(control.calcular_diferencia_presupuesto(date(2025, 6, 2)), 0)

    def test_3_gasto_mayor_presupuesto(self):
        """Debe retornar diferencia negativa si el gasto excede el presupuesto."""
        control = self.crear_control_gasto(120000, 100000)
        self.assertEqual(control.calcular_diferencia_presupuesto(date(2025, 6, 2)), -20000)

    def test_4_gasto_cero(self):
        """Debe retornar el presupuesto completo si no hubo gasto."""
        control = self.crear_control_gasto(0, 50000)
        self.assertEqual(control.calcular_diferencia_presupuesto(date(2025, 6, 2)), 50000)

    def test_5_presupuesto_cero(self):
        """Debe retornar negativo igual al gasto si el presupuesto es cero."""
        control = self.crear_control_gasto(50000, 0)
        self.assertEqual(control.calcular_diferencia_presupuesto(date(2025, 6, 2)), -50000)

    def test_6_gasto_y_presupuesto_cero(self):
        """Debe retornar cero si tanto el gasto como el presupuesto son cero."""
        control = self.crear_control_gasto(0, 0)
        self.assertEqual(control.calcular_diferencia_presupuesto(date(2025, 6, 2)), 0)

    def test_7_gasto_negativo(self):
        """Debe lanzar ValueError si el gasto tiene valor negativo."""
        with self.assertRaises(ValueError):
            self.crear_control_gasto(-50000, 100000)

    def test_8_presupuesto_negativo(self):
        """Debe lanzar ValueError si el presupuesto diario es negativo."""
        control = self.crear_control_gasto(50000, -100000)
        with self.assertRaises(ValueError):
            control.calcular_diferencia_presupuesto(date(2025, 6, 2))



if __name__ == '__main__':
    unittest.main()

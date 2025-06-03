import unittest
from datetime import date
from todoViaje import *


# Clase de pruebas
class TestCasosReporte(unittest.TestCase):

    def test_dia_con_efectivo_y_tarjeta(self):
        viaje = Viaje()
        viaje.agregarGasto(Gasto(date(2025, 6, 1), 20000, MedioPago.EFECTIVO))
        viaje.agregarGasto(Gasto(date(2025, 6, 1), 30000, MedioPago.TARJETA_DEBITO))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
        self.assertEqual(reporte[date(2025, 6, 1)], {'efectivo': 20000, 'tarjetas': 30000, 'total': 50000})

    def test_dia_solo_tarjeta_credito(self):
        viaje = Viaje()
        viaje.agregarGasto(Gasto(date(2025, 6, 2), 15000, MedioPago.TARJETA_CREDITO))
        viaje.agregarGasto(Gasto(date(2025, 6, 2), 25000, MedioPago.TARJETA_CREDITO))
        viaje.agregarGasto(Gasto(date(2025, 6, 2), 10000, MedioPago.TARJETA_CREDITO))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
        self.assertEqual(reporte[date(2025, 6, 2)], {'efectivo': 0, 'tarjetas': 50000, 'total': 50000})

    def test_dia_solo_efectivo(self):
        viaje = Viaje()
        viaje.agregarGasto(Gasto(date(2025, 6, 3), 5000, MedioPago.EFECTIVO))
        viaje.agregarGasto(Gasto(date(2025, 6, 3), 15000, MedioPago.EFECTIVO))
        viaje.agregarGasto(Gasto(date(2025, 6, 3), 8000, MedioPago.EFECTIVO))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
        self.assertEqual(reporte[date(2025, 6, 3)], {'efectivo': 28000, 'tarjetas': 0, 'total': 28000})

    def test_mezcla_tarjeta_credito_y_debito(self):
        viaje = Viaje()
        viaje.agregarGasto(Gasto(date(2025, 6, 4), 20000, MedioPago.TARJETA_DEBITO))
        viaje.agregarGasto(Gasto(date(2025, 6, 4), 10000, MedioPago.TARJETA_CREDITO))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
        self.assertEqual(reporte[date(2025, 6, 4)], {'efectivo': 0, 'tarjetas': 30000, 'total': 30000})

    def test_sin_gastos(self):
        viaje = Viaje()
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
        self.assertEqual(reporte, {})

    def test_varias_fechas(self):
        viaje = Viaje()
        viaje.agregarGasto(Gasto(date(2025, 6, 1), 20000, MedioPago.EFECTIviajeO))
        viaje.agregarGasto(Gasto(date(2025, 6, 1), 30000, MedioPago.TARJETA_DEBITO))
        viaje.agregarGasto(Gasto(date(2025, 6, 2), 15000, MedioPago.TARJETA_CREDITO))
        viaje.agregarGasto(Gasto(date(2025, 6, 2), 25000, MedioPago.TARJETA_CREDITO))
        viaje.agregarGasto(Gasto(date(2025, 6, 3), 5000, MedioPago.EFECTIVO))
        viaje.agregarGasto(Gasto(date(2025, 6, 3), 15000, MedioPago.EFECTIVO))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
        self.assertEqual(reporte[date(2025, 6, 1)], {'efectivo': 20000, 'tarjetas': 30000, 'total': 50000})
        self.assertEqual(reporte[date(2025, 6, 2)], {'efectivo': 0, 'tarjetas': 40000, 'total': 40000})
        self.assertEqual(reporte[date(2025, 6, 3)], {'efectivo': 20000, 'tarjetas': 0, 'total': 20000})

    def test_mismos_gastos_repetidos(self):
        viaje = Viaje()
        viaje.agregarGasto(Gasto(date(2025, 6, 6), 10000, MedioPago.EFECTIVO))
        viaje.agregarGasto(Gasto(date(2025, 6, 6), 10000, MedioPago.EFECTIVO))
        viaje.agregarGasto(Gasto(date(2025, 6, 6), 10000, MedioPago.TARJETA_CREDITO))
        viaje.agregarGasto(Gasto(date(2025, 6, 6), 10000, MedioPago.TARJETA_CREDITO))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
        self.assertEqual(reporte[date(2025, 6, 6)], {'efectivo': 20000, 'tarjetas': 20000, 'total': 40000})

    def test_valorCOP_negativo(self):
        with self.assertRaises(ValueError):
            Gasto(date(2025, 6, 1), -5000, MedioPago.EFECTIVO)

    def test_valorCOP_tipo_incorrecto(self):
        with self.assertRaises(ValueError):
            Gasto(date(2025, 6, 1), "diez mil", MedioPago.EFECTIVO)

# Para ejecutar las pruebas desde línea de comandos o entorno
if __name__ == '__main__':
    unittest.main()

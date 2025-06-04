import unittest
from datetime import date

from viajes.enums import MedioPago, TipoGasto, TipoViaje
from modelos.destino import Destino
from modelos.gasto import Gasto
from modelos.viaje import Viaje
from controladores.control_reporte import ControlReporte

class TestCasosReporte(unittest.TestCase):

    def setUp(self):
        """Crea una instancia básica de viaje nacional para pruebas."""
        destino = Destino("Bogotá", "Cundinamarca", "Colombia", "cop")
        self.viaje = Viaje(
            fecha_inicio=date(2025, 6, 1),
            fecha_fin=date(2025, 6, 10),
            presupuesto_diario=100000,
            destino=destino,
            tipo_viaje=TipoViaje.NACIONAL
        )

    def test_dia_con_efectivo_y_tarjeta(self):
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 1), 20000, MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, 20000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 1), 30000, MedioPago.TARJETA_DEBITO, TipoGasto.TRANSPORTE, 30000))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        self.assertEqual(reporte[date(2025, 6, 1)], {'efectivo': 20000, 'tarjetas': 30000, 'total': 50000})

    def test_dia_solo_tarjeta_credito(self):
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 2), 15000, MedioPago.TARJETA_CREDITO, TipoGasto.ALIMENTACION, 15000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 2), 25000, MedioPago.TARJETA_CREDITO, TipoGasto.TRANSPORTE, 25000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 2), 10000, MedioPago.TARJETA_CREDITO, TipoGasto.COMPRAS, 10000))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        self.assertEqual(reporte[date(2025, 6, 2)], {'efectivo': 0, 'tarjetas': 50000, 'total': 50000})

    def test_dia_solo_efectivo(self):
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 3), 5000, MedioPago.EFECTIVO, TipoGasto.COMPRAS, 5000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 3), 15000, MedioPago.EFECTIVO, TipoGasto.TRANSPORTE, 15000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 3), 8000, MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, 8000))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        self.assertEqual(reporte[date(2025, 6, 3)], {'efectivo': 28000, 'tarjetas': 0, 'total': 28000})

    def test_mezcla_tarjeta_credito_y_debito(self):
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 4), 20000, MedioPago.TARJETA_DEBITO, TipoGasto.ALIMENTACION, 20000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 4), 10000, MedioPago.TARJETA_CREDITO, TipoGasto.COMPRAS, 10000))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        self.assertEqual(reporte[date(2025, 6, 4)], {'efectivo': 0, 'tarjetas': 30000, 'total': 30000})

    def test_sin_gastos(self):
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        self.assertEqual(reporte, {})

    def test_varias_fechas(self):
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 1), 20000, MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, 20000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 1), 30000, MedioPago.TARJETA_DEBITO, TipoGasto.TRANSPORTE, 30000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 2), 15000, MedioPago.TARJETA_CREDITO, TipoGasto.ALIMENTACION, 15000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 2), 25000, MedioPago.TARJETA_CREDITO, TipoGasto.COMPRAS, 25000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 3), 5000, MedioPago.EFECTIVO, TipoGasto.TRANSPORTE, 5000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 3), 15000, MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, 15000))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        self.assertEqual(reporte[date(2025, 6, 1)], {'efectivo': 20000, 'tarjetas': 30000, 'total': 50000})
        self.assertEqual(reporte[date(2025, 6, 2)], {'efectivo': 0, 'tarjetas': 40000, 'total': 40000})
        self.assertEqual(reporte[date(2025, 6, 3)], {'efectivo': 20000, 'tarjetas': 0, 'total': 20000})

    def test_mismos_gastos_repetidos(self):
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 6), 10000, MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, 10000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 6), 10000, MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, 10000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 6), 10000, MedioPago.TARJETA_CREDITO, TipoGasto.ALIMENTACION, 10000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 6), 10000, MedioPago.TARJETA_CREDITO, TipoGasto.ALIMENTACION, 10000))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        self.assertEqual(reporte[date(2025, 6, 6)], {'efectivo': 20000, 'tarjetas': 20000, 'total': 40000})

    def test_valorCOP_negativo(self):
        with self.assertRaises(ValueError):
            Gasto(date(2025, 6, 1), -5000, MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, -5000)

    def test_valorCOP_tipo_incorrecto(self):
        with self.assertRaises(TypeError):
            Gasto(date(2025, 6, 1), "diez mil", MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, "diez mil")


if __name__ == '__main__':
    unittest.main()
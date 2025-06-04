""""
Pruebas unitarias para el ControlReporte de la aplicación de gestión de viajes.
"""
import unittest
from datetime import date

from Tarea6.enums.medio_pago import MedioPago
from Tarea6.enums.tipo_gasto import TipoGasto
from Tarea6.enums.tipo_viaje import TipoViaje
from Tarea6.modelos.destino import Destino
from Tarea6.modelos.gasto import Gasto
from Tarea6.modelos.viaje import Viaje
from Tarea6.controladores.control_reporte import ControlReporte

class TestCasosReporte(unittest.TestCase):
    """Conjunto de pruebas unitarias para validar el cálculo de reportes de gastos."""

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
        """Debe calcular correctamente los montos si hay efectivo y tarjeta en el mismo día."""
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 1), 20000, MedioPago.EFECTIVO,
            TipoGasto.ALIMENTACION, 20000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 1), 30000, MedioPago.TARJETA_DEBITO,
            TipoGasto.TRANSPORTE, 30000
        ))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(
            None, self.viaje
        )
        self.assertEqual(
            reporte[date(2025, 6, 1)],
            {'efectivo': 20000, 'tarjetas': 30000, 'total': 50000}
        )

    def test_dia_solo_tarjeta_credito(self):
        """Debe mostrar correctamente los montos cuando solo se usan tarjetas de crédito."""
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 2), 15000, MedioPago.TARJETA_CREDITO,
            TipoGasto.ALIMENTACION, 15000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 2), 25000, MedioPago.TARJETA_CREDITO,
            TipoGasto.TRANSPORTE, 25000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 2), 10000, MedioPago.TARJETA_CREDITO,
            TipoGasto.COMPRAS, 10000
        ))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(
            None, self.viaje
        )
        self.assertEqual(
            reporte[date(2025, 6, 2)],
            {'efectivo': 0, 'tarjetas': 50000, 'total': 50000}
        )

    def test_dia_solo_efectivo(self):
        """Debe calcular correctamente los montos cuando solo hay pagos en efectivo."""
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 3), 5000, MedioPago.EFECTIVO,
            TipoGasto.COMPRAS, 5000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 3), 15000, MedioPago.EFECTIVO,
            TipoGasto.TRANSPORTE, 15000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 3), 8000, MedioPago.EFECTIVO,
            TipoGasto.ALIMENTACION, 8000
        ))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(
            None, self.viaje
        )
        self.assertEqual(
            reporte[date(2025, 6, 3)],
            {'efectivo': 28000, 'tarjetas': 0, 'total': 28000}
        )

    def test_mezcla_tarjeta_credito_y_debito(self):
        """Debe sumar ambas tarjetas como 'tarjetas' en el reporte diario."""
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 4), 20000, MedioPago.TARJETA_DEBITO,
            TipoGasto.ALIMENTACION, 20000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 4), 10000, MedioPago.TARJETA_CREDITO,
            TipoGasto.COMPRAS, 10000
        ))
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(
            None, self.viaje
        )
        self.assertEqual(
            reporte[date(2025, 6, 4)],
            {'efectivo': 0, 'tarjetas': 30000, 'total': 30000}
        )


    def test_sin_gastos(self):
        """Debe retornar un diccionario vacío si no hay gastos registrados."""
        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        self.assertEqual(reporte, {})

    def test_varias_fechas(self):
        """Debe separar y acumular correctamente los gastos por fecha."""
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 1), 20000, MedioPago.EFECTIVO,
            TipoGasto.ALIMENTACION, 20000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 1), 30000, MedioPago.TARJETA_DEBITO,
            TipoGasto.TRANSPORTE, 30000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 2), 15000, MedioPago.TARJETA_CREDITO,
            TipoGasto.ALIMENTACION, 15000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 2), 25000, MedioPago.TARJETA_CREDITO,
            TipoGasto.COMPRAS, 25000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 3), 5000, MedioPago.EFECTIVO,
            TipoGasto.TRANSPORTE, 5000
        ))
        self.viaje.agregar_gasto(Gasto(
            date(2025, 6, 3), 15000, MedioPago.EFECTIVO,
            TipoGasto.ALIMENTACION, 15000
        ))

        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)

        self.assertEqual(
            reporte[date(2025, 6, 1)],
            {'efectivo': 20000, 'tarjetas': 30000, 'total': 50000}
        )
        self.assertEqual(
            reporte[date(2025, 6, 2)],
            {'efectivo': 0, 'tarjetas': 40000, 'total': 40000}
        )
        self.assertEqual(
            reporte[date(2025, 6, 3)],
            {'efectivo': 20000, 'tarjetas': 0, 'total': 20000}
        )


    def test_mismos_gastos_repetidos(self):
        """Debe manejar correctamente gastos repetidos en la misma fecha."""
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 6),
                                       10000,
                                       MedioPago.EFECTIVO,
                                        TipoGasto.ALIMENTACION,
                                        10000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 6),
                                       10000, MedioPago.EFECTIVO,
                                       TipoGasto.ALIMENTACION,
                                       10000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 6),
                                       10000,
                                       MedioPago.TARJETA_CREDITO,
                                       TipoGasto.ALIMENTACION,
                                       10000))
        self.viaje.agregar_gasto(Gasto(date(2025, 6, 6),
                                       10000,
                                       MedioPago.TARJETA_CREDITO,
                                       TipoGasto.ALIMENTACION,
                                       10000))

        reporte = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, self.viaje)
        print(reporte[date(2025, 6, 6)])  # depuración

        self.assertEqual(reporte[date(2025, 6, 6)], {
            'efectivo': 20000,
            'tarjetas': 20000,
            'total': 40000
        })

    def test_valor_cop_negativo(self):
        """Debe lanzar ValueError si el valor en COP es negativo."""
        with self.assertRaises(ValueError):
            Gasto(date(2025, 6, 1), -5000, MedioPago.EFECTIVO, TipoGasto.ALIMENTACION, -5000)

    def test_valor_cop_tipo_incorrecto(self):
        """Debe lanzar TypeError si el valor en COP tiene tipo incorrecto (no numérico)."""
        with self.assertRaises(TypeError):
            Gasto(date(2025, 6, 1), "diez mil", MedioPago.EFECTIVO,
                   TipoGasto.ALIMENTACION, "diez mil")


if __name__ == '__main__':
    unittest.main()

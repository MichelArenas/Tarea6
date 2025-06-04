"""
Módulo que define la clase Viaje para gestionar información relacionada con gastos y presupuesto
durante un viaje. Incluye funcionalidades para calcular diferencias presupuestarias.
"""
from enums.tipo_viaje import TipoViaje

from modelos.destino import Destino

from modelos.gasto import Gasto

class Viaje:
    """
    Representa un viaje realizado por un usuario, incluyendo información sobre gastos 
    y presupuesto diario.

    Esta clase permite registrar y analizar los gastos hechos durante el viaje,
    calculando diferencias respecto al presupuesto planeado.
    """

    def __init__(self, fecha_inicio, fecha_fin, presupuesto_diario: float, destino: Destino,
                 tipo_viaje: TipoViaje):
        """
        Inicializa un objeto Viaje con fechas, presupuesto, destino y tipo de viaje.
        """
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.destino = destino
        self.tipo_viaje = tipo_viaje
        self.estado_viaje = True
        self.gastos = []

    def agregar_gasto(self, gasto: Gasto):
        """
        Agrega un gasto al viaje si el viaje está activo.

        Args:
            gasto (Gasto): Objeto Gasto que representa un gasto realizado durante el viaje.

        Raises:
            RuntimeError: Si el viaje ya ha finalizado y no se pueden registrar más gastos.
        """
        if self.estado_viaje:
            self.gastos.append(gasto)
        else:
            raise RuntimeError("El viaje ha finalizado, no se pueden registrar más gastos.")


    def finalizar_viaje(self):
        """
        Marca el viaje como finalizado, impidiendo el registro de nuevos gastos.
        """
        self.estado_viaje = False

    def calcular_gasto_diario(self, fecha):
        """
        Calcula el gasto total realizado en una fecha específica.

        Args:
            fecha (date): Fecha para la cual se desea calcular el gasto.

        Returns:
            float: Suma de los valores en COP de los gastos registrados en esa fecha.
        """
        return sum(g.get_valor_moneda_local_cop() for g in self.gastos if g.get_fecha()== fecha)

    def get_gastos(self):
        """
        Retorna la lista completa de gastos registrados en el viaje.

        Returns:
            list[Gasto]: Lista de todos los gastos asociados al viaje.
        """
        return self.gastos

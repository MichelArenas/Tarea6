"""
    modulo controladora encargada de registrar y validar los gastos realizados durante un viaje.

    Esta clase permite registrar nuevos gastos asociados a una fecha, calcular su conversión a pesos 
    colombianos (COP) en caso de viajes internacionales, y verificar el cumplimiento del presupuesto
    También lanza una excepción si se intenta registrar un gasto en un viaje finalizado.
"""
from enums.tipo_gasto import TipoGasto

from enums.medio_pago import MedioPago

from modelos.viaje import Viaje

from modelos.gasto import Gasto

from .control_api_moneda_intercambio import ControlAPIMonedaIntercambio

class ViajeFinalizadoError(Exception):
    """Se lanza cuando se intenta registrar un gasto en un viaje finalizado.""" 

class ControlGasto:
    """
    Controlador que gestiona los gastos registrados durante un viaje.

    Atributos:
        viaje (Viaje): Objeto del viaje actual.
        control_viaje (ControlViaje): Controlador asociado al viaje.
    """

    def __init__(self, viaje: Viaje, control_viaje):
        """
        Inicializa el controlador de gastos con un viaje y su controlador.

        Args:
            viaje (Viaje): Objeto del viaje actual.
            control_viaje (ControlViaje): Controlador del viaje.
        """
        self.viaje = viaje
        self.control_viaje = control_viaje

    def validar_medio_pago(self, medio_pago) -> bool:
        """
        Verifica que el medio de pago sea una instancia válida de MedioPago.

        Args:
            medio_pago: Objeto a validar.

        Returns:
            bool: True si es un MedioPago válido, False en caso contrario.
        """
        return isinstance(medio_pago, MedioPago)

    def registrar_gasto(self, fecha, valor: float, medio_pago: MedioPago, tipo_gasto: TipoGasto):
        """
        Registra un gasto en el viaje, validando tipo de cambio si es internacional.

        Args:
            fecha: Fecha del gasto.
            valor (float): Valor original del gasto.
            medio_pago (MedioPago): Medio de pago utilizado.
            tipo_gasto (TipoGasto): Tipo del gasto.

        Raises:
            ViajeFinalizadoError: Si el viaje ya fue finalizado.
        """
        if not self.viaje.estado_viaje:
            raise ViajeFinalizadoError("El viaje ha finalizado, no se pueden registrar más gastos.")

        if self.viaje.tipo_viaje == "INTERNACIONAL":
            moneda_destino = self.viaje.destino.get_moneda_local()
            valor_cop = ControlAPIMonedaIntercambio.convertir_moneda(moneda_destino, valor, fecha)
        else:
            valor_cop = valor

        gasto = Gasto(fecha, valor, medio_pago, tipo_gasto, valor_cop)
        self.viaje.agregar_gasto(gasto)
        print(
            f"Se registró un gasto de {valor} {self.viaje.destino.get_moneda_local()} "
            f"-> {valor_cop} COP"
        )
        diferencia = self.calcular_diferencia_presupuesto(fecha)
        if diferencia > 0:
            print(f"Presupuesto restante para {fecha}: {diferencia} COP")
        elif diferencia == 0:
            print(f"Presupuesto agotado para {fecha}")
        else:
            print(f"Presupuesto excedido para {fecha} por {-diferencia} COP")


    def calcular_diferencia_presupuesto(self, fecha) -> float:
        """
        Calcula la diferencia entre el presupuesto diario y los gastos realizados en una fecha.

        Args:
            fecha: Fecha a evaluar.

        Returns:
            float: Diferencia entre presupuesto diario y gasto total en COP.
        """
        total_cop = self.viaje.calcular_gasto_diario(fecha)
        return self.viaje.presupuesto_diario - total_cop

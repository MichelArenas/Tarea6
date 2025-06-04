"""
    Clase encargada de generar reportes analíticos sobre los gastos realizados durante un viaje.

    Proporciona métodos estáticos para calcular estadísticas de gastos por fecha y por tipo,
    diferenciando los medios de pago utilizados (efectivo o tarjeta). Los reportes generados 
    pueden usarse para evaluar el comportamiento financiero del usuario durante el viaje.
"""

from enums.medio_pago import MedioPago

from enums.tipo_gasto import TipoGasto

from modelos.viaje import Viaje

class ControlReporte:
    """
    Clase encargada de generar reportes sobre los gastos realizados durante un viaje.
    """

    @staticmethod
    def calcular_reporte_gastos_todos_los_dias(_, viaje: Viaje) -> dict:
        """
        Calcula un reporte diario de gastos, diferenciando entre efectivo y tarjeta.

        Args:
            _ (ignored): Parámetro ignorado (usado por compatibilidad).
            viaje (Viaje): Objeto del viaje del cual se extraen los gastos.

        Returns:
            dict: Diccionario donde cada clave es una fecha y el valor es otro
                  diccionario con los montos totales por medio de pago y el total general.
        """
        reporte = {}
        for gasto in viaje.get_gastos():
            fecha = gasto.get_fecha()
            if fecha not in reporte:
                reporte[fecha] = {'efectivo': 0, 'tarjetas': 0, 'total': 0}
            if gasto.get_medio_pago() == MedioPago.EFECTIVO:
                reporte[fecha]['efectivo'] += gasto.get_valor_moneda_local_cop()
            else:
                reporte[fecha]['tarjetas'] += gasto.get_valor_moneda_local_cop()
            reporte[fecha]['total'] += gasto.get_valor_moneda_local_cop()
        return reporte

    @staticmethod
    def reporte_por_tipo(viaje: Viaje) -> dict:
        """
        Calcula un reporte de gastos agrupados por tipo de gasto,
          diferenciando entre efectivo y tarjeta.

        Args:
            viaje (Viaje): Objeto del viaje del cual se extraen los gastos.

        Returns:
            dict: Diccionario donde cada clave es un tipo de gasto y el valor es otro
                  diccionario con los montos totales por medio de pago y el total general.
        """
        reporte = {}
        for tipo in TipoGasto:
            reporte[tipo.name] = {'efectivo': 0, 'tarjetas': 0, 'total': 0}

        for gasto in viaje.get_gastos():
            tipo = gasto.get_tipo_gasto().name
            if gasto.get_medio_pago() == MedioPago.EFECTIVO:
                reporte[tipo]['efectivo'] += gasto.get_valor_moneda_local_cop()
            else:
                reporte[tipo]['tarjetas'] += gasto.get_valor_moneda_local_cop()
            reporte[tipo]['total'] += gasto.get_valor_moneda_local_cop()
        return reporte

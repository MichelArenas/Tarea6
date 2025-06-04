"""
    Clase que representa un gasto registrado durante un viaje.

    Esta clase almacena tanto la información original del gasto como su equivalente en 
    pesos colombianos (COP), permitiendo realizar análisis financieros 
    y comparaciones con el presupuesto.
"""

from enums.tipo_gasto import TipoGasto

from enums.medio_pago import MedioPago

class Gasto:
    """
    Representa un gasto realizado durante un viaje.

    Atributos:
        fecha (date): Fecha en la que se realizó el gasto.
        valor (float): Valor del gasto en la moneda original.
        medio_pago (MedioPago): Medio de pago utilizado (efectivo o tarjeta).
        tipo_gasto (TipoGasto): Tipo de gasto (alojamiento, transporte, etc.).
        valor_cop (float): Valor del gasto convertido a pesos colombianos (COP).
    """

    def __init__(self, fecha, valor: float, medio_pago: MedioPago,
                 tipo_gasto: TipoGasto, valor_cop: float):
        """Inicializa un gasto con fecha, valor, medio de pago, tipo y valor en COP."""
        self.fecha = fecha
        self.valor = valor
        self.medio_pago = medio_pago
        self.tipo_gasto = tipo_gasto
        self.valor_cop = valor_cop

    def get_fecha(self):
        """Retorna la fecha en la que se realizó el gasto."""
        return self.fecha

    def get_valor(self):
        """Retorna el valor original del gasto."""
        return self.valor

    def get_medio_pago(self):
        """Retorna el medio de pago utilizado para el gasto."""
        return self.medio_pago

    def get_tipo_gasto(self):
        """Retorna el tipo de gasto realizado."""
        return self.tipo_gasto

    def get_valor_moneda_local_cop(self):
        """Retorna el valor del gasto convertido a COP (pesos colombianos)."""
        return self.valor_cop

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
        valor (float): Valor original del gasto (en moneda local si es internacional).
        medio_pago (MedioPago): Medio utilizado para realizar el gasto (efectivo, tarjeta).
        tipo_gasto (TipoGasto): Categoría del gasto (transporte, alojamiento, etc.).
        valor_cop (float): Valor del gasto convertido a pesos colombianos (COP).
    """

    def __init__(self, fecha, valor: float, medio_pago: MedioPago,
                 tipo_gasto: TipoGasto, valor_cop: float):
        """
        Inicializa una nueva instancia de Gasto, validando los tipos y valores.

        Args:
            fecha (date): Fecha del gasto.
            valor (float): Monto original del gasto.
            medio_pago (MedioPago): Medio de pago utilizado.
            tipo_gasto (TipoGasto): Categoría del gasto.
            valor_cop (float): Monto convertido a pesos colombianos (COP).

        Raises:
            TypeError: Si los valores no son numéricos.
            ValueError: Si los montos son negativos.
        """
        if not isinstance(valor, (int, float)):
            raise TypeError("El valor debe ser un número (int o float).")

        if not isinstance(valor_cop, (int, float)):
            raise TypeError("El valor en COP debe ser un número (int o float).")

        if valor < 0:
            raise ValueError("El valor original no puede ser negativo.")
        if valor_cop < 0:
            raise ValueError("El valor en COP no puede ser negativo.")

        self.fecha = fecha
        self.valor = valor
        self.medio_pago = medio_pago
        self.tipo_gasto = tipo_gasto
        self.valor_cop = valor_cop

    def get_fecha(self):
        """
        Retorna la fecha en que se realizó el gasto.

        Returns:
            date: Fecha del gasto.
        """
        return self.fecha

    def get_valor(self):
        """
        Retorna el valor original del gasto.

        Returns:
            float: Valor en moneda local.
        """
        return self.valor

    def get_medio_pago(self):
        """
        Retorna el medio de pago utilizado.

        Returns:
            MedioPago: Medio de pago del gasto.
        """
        return self.medio_pago

    def get_tipo_gasto(self):
        """
        Retorna el tipo o categoría del gasto.

        Returns:
            TipoGasto: Tipo del gasto.
        """
        return self.tipo_gasto

    def get_valor_moneda_local_cop(self):
        """
        Retorna el valor del gasto convertido a pesos colombianos (COP).

        Returns:
            float: Valor del gasto en COP.
        """
        return self.valor_cop

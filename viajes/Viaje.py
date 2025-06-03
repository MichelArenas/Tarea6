"""
Módulo que define la clase Viaje para gestionar información relacionada con gastos y presupuesto
durante un viaje. Incluye funcionalidades para calcular diferencias presupuestarias.
"""

class Viaje:
    """
    Representa un viaje realizado por un usuario, incluyendo información sobre gastos 
    y presupuesto diario.

    Esta clase permite registrar y analizar los gastos hechos durante el viaje,
    calculando diferencias respecto al presupuesto planeado.
    """

    def calcular_diferencias_gastos(self, valor_cop: float, presupuesto_diario: float) -> float:
        """
        Calcula la diferencia entre el presupuesto diario y el gasto registrado.

        Args:
            valor_cop (float): Valor del gasto convertido a pesos colombianos.
            presupuesto_diario (float): Monto asignado como presupuesto para ese día.

        Returns:
            float: Diferencia entre el presupuesto y el gasto. Puede ser positiva (ahorro),
                   cero (gasto exacto) o negativa (exceso de gasto).
        """
        return presupuesto_diario - valor_cop

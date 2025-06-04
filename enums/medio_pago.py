"""
Módulo que define los enumerados usados para clasificar los medios de pago 
en la aplicación de registro de gastos de viaje.
"""

from enum import Enum

class MedioPago(Enum):
    """
    Enumeración que representa los medios de pago disponibles para registrar un gasto.

    - EFECTIVO
    - TARJETA CREDITO
    - TARJETA DEBITO
    """
    EFECTIVO = "EFECTIVO"
    TARJETA_CREDITO = "TARJETA CREDITO"
    TARJETA_DEBITO = "TARJETA DEBITO"

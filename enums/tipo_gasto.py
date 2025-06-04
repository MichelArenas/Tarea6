"""
Módulo que define los enumerados usados para clasificar los tipos de gasto
en la aplicación de registro de gastos de viaje.
"""

from enum import Enum

class TipoGasto(Enum):
    """
    Enumeración que representa los tipos posibles de gasto durante el viaje.

    Incluye categorías como transporte, alojamiento, alimentación, entretenimiento, etc.
    """
    TRANSPORTE = "TRANSPORTE"
    ALOJAMIENTO = "ALOJAMIENTO"
    ALIMENTACION = "ALIMENTACION"
    ENTRETENIMIENTO = "ENTRETENIMIENTO"
    COMPRAS = "COMPRAS"
    OTROS = "OTROS"

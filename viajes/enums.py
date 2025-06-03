"""
Módulo que define los enumerados usados para clasificar los viajes, tipos de gasto
y medios de pago en la aplicación de registro de gastos de viaje.
"""

from enum import Enum

class TipoViaje(Enum):
    """
    Enumeración que representa el tipo de viaje.

    - NACIONAL: Viaje dentro del país.
    - INTERNACIONAL: Viaje fuera del país.
    """
    NACIONAL = "NACIONAL"
    INTERNACIONAL = "INTERNACIONAL"

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

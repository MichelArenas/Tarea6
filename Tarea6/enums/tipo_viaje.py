"""
Módulo que define los enumerados usados para clasificar los viajes,
en la aplicación de registro de gastos de viaje.
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

"""
Clase controladora que gestiona la creación, validación y actualización del estado de un viaje.

Esta clase actúa como intermediario entre la lógica de negocio y los datos del objeto Viaje,
facilitando el proceso de registro, verificación y control de la información asociada al viaje.
"""

from datetime import date

from enums.tipo_viaje import TipoViaje

from modelos.viaje import Viaje

from modelos.destino import Destino

class ControlViaje:
    """
    Controlador que gestiona las operaciones relacionadas con un viaje.

    Atributos:
        viaje (Viaje): Instancia del viaje actual.
    """

    def __init__(self):
        """Inicializa el controlador con un viaje en None."""
        self.viaje = None

    def registrar_viaje(self, fecha_inicio: date, fecha_fin: date,
                        presupuesto_diario: float, destino: Destino, tipo_viaje: TipoViaje):
        """
        Crea una nueva instancia de Viaje con los datos proporcionados.

        Args:
            fecha_inicio (date): Fecha de inicio del viaje.
            fecha_fin (date): Fecha de fin del viaje.
            presupuesto_diario (float): Presupuesto diario asignado.
            destino (Destino): Lugar al que se realizará el viaje.
            tipo_viaje (TipoViaje): Tipo de viaje (NACIONAL o INTERNACIONAL).
        """
        self.viaje = Viaje(fecha_inicio, fecha_fin, presupuesto_diario, destino, tipo_viaje)

    def validar_destino(self):
        """
        Verifica si el destino del viaje ha sido definido.

        Returns:
            bool: True si el destino existe, False si no.
        """
        return self.viaje.destino is not None

    def iniciar_viaje(self):
        """
        Cambia el estado del viaje a activo.
        """
        self.viaje.estado_viaje = True

    def finalizar_viaje(self):
        """
        Finaliza el viaje si la fecha actual es mayor o igual a la fecha de fin.
        """
        hoy = date.today()
        if hoy >= self.viaje.fecha_fin:
            self.viaje.finalizar_viaje()
            print("El viaje se ha finalizado")
        else:
            print("El viaje está aún activo. Fecha de finalización:", self.viaje.fecha_fin)

    def get_viaje(self):
        """
        Retorna la instancia actual del viaje.

        Returns:
            Viaje: Objeto viaje activo en el controlador.
        """
        return self.viaje

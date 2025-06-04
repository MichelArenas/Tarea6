"""
Módulo para la gestión de clientes dentro del sistema de viajes.

Contiene la clase Cliente, que representa a una persona registrada en el sistema,
junto con sus datos personales, y proporciona métodos para acceder a dicha información.
"""
class Cliente:
    """
    Representa a un cliente que va a realizar un viaje.

    Atributos:
        nombre_completo (str): Nombre completo del cliente.
        cedula (str): Número de cédula o identificación del cliente.
        telefono (str): Número de contacto del cliente.
        correo (str): Correo electrónico del cliente.
    """

    def __init__(self, nombre_completo: str, cedula: str, telefono: str, correo: str):
        """Inicializa un objeto Cliente con sus datos personales."""
        self.nombre_completo = nombre_completo
        self.cedula = cedula
        self.telefono = telefono
        self.correo = correo

    def get_nombre(self):
        """Retorna el nombre completo del cliente."""
        return self.nombre_completo

    def get_cedula(self):
        """Retorna la cédula del cliente."""
        return self.cedula

    def get_telefono(self):
        """Retorna el número de teléfono del cliente."""
        return self.telefono

    def get_correo(self):
        """Retorna el correo electrónico del cliente."""
        return self.correo

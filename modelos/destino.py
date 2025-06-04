"""
    Clase que representa el destino asociado a un viaje.

    Contiene la información geográfica y monetaria del lugar de destino, 
    la cual es útil para calcular conversiones de divisas y reportes.
"""
class Destino:
    """
    Representa el destino de un viaje.

    Atributos:
        ciudad (str): Nombre de la ciudad del destino.
        departamento (str): Departamento o región administrativa del destino.
        pais (str): País del destino.
        moneda_local (str): Código de la moneda local del destino (por ejemplo, 'cop', 'usd').
    """

    def __init__(self, ciudad: str, departamento: str, pais: str, moneda_local: str):
        """Inicializa un objeto Destino con ciudad, departamento, país y moneda local."""
        self.ciudad = ciudad
        self.departamento = departamento
        self.pais = pais
        self.moneda_local = moneda_local

    def get_ciudad(self):
        """Retorna el nombre de la ciudad del destino."""
        return self.ciudad

    def get_departamento(self):
        """Retorna el nombre del departamento del destino."""
        return self.departamento

    def get_pais(self):
        """Retorna el nombre del país del destino."""
        return self.pais

    def get_moneda_local(self):
        """Retorna el código de la moneda local del destino."""
        return self.moneda_local

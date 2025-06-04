"""
Módulo para la gestión de viajes, clientes, destinos, gastos y el control de moneda.
Incluye clases para representar entidades del sistema y controladores que manejan
la lógica del negocio.
"""

from datetime import date

import requests

from .tipo_gasto import TipoGasto

from .tipo_viaje import TipoViaje

from ..enums.medio_pago import MedioPago

class ViajeFinalizadoError(Exception):
    """Se lanza cuando se intenta registrar un gasto en un viaje finalizado."""

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



class Viaje:
    """
    Representa un viaje realizado por un cliente.

    Atributos:
        fecha_inicio (date): Fecha de inicio del viaje.
        fecha_fin (date): Fecha de finalización del viaje.
        presupuesto_diario (float): Presupuesto asignado por día.
        destino (Destino): Destino del viaje.
        tipo_viaje (TipoViaje): Tipo de viaje (nacional o internacional).
        estado_viaje (bool): Estado actual del viaje (activo o finalizado).
        gastos (list[Gasto]): Lista de objetos Gasto asociados al viaje.
    """

    def __init__(self, fecha_inicio, fecha_fin, presupuesto_diario: float, destino: Destino,
                 tipo_viaje: TipoViaje):
        """
        Inicializa un objeto Viaje con fechas, presupuesto, destino y tipo de viaje.
        """
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.destino = destino
        self.tipo_viaje = tipo_viaje
        self.estado_viaje = True
        self.gastos = []

    def agregar_gasto(self, gasto: Gasto):
        """
        Agrega un gasto al viaje si el viaje está activo.

        Args:
            gasto (Gasto): Objeto Gasto que representa un gasto realizado durante el viaje.

        Raises:
            RuntimeError: Si el viaje ya ha finalizado y no se pueden registrar más gastos.
        """
        if self.estado_viaje:
            self.gastos.append(gasto)
        else:
            raise RuntimeError("El viaje ha finalizado, no se pueden registrar más gastos.")


    def finalizar_viaje(self):
        """
        Marca el viaje como finalizado, impidiendo el registro de nuevos gastos.
        """
        self.estado_viaje = False

    def calcular_gasto_diario(self, fecha):
        """
        Calcula el gasto total realizado en una fecha específica.

        Args:
            fecha (date): Fecha para la cual se desea calcular el gasto.

        Returns:
            float: Suma de los valores en COP de los gastos registrados en esa fecha.
        """
        return sum(g.get_valor_moneda_local_cop() for g in self.gastos if g.get_fecha()== fecha)

    def get_gastos(self):
        """
        Retorna la lista completa de gastos registrados en el viaje.

        Returns:
            list[Gasto]: Lista de todos los gastos asociados al viaje.
        """
        return self.gastos


class ControlAPIMonedaIntercambio:
    """
    Clase encargada de obtener y convertir tasas de cambio entre monedas utilizando una API pública.

    Métodos:
        obtener_tasa_cambio(moneda_origen: str, fecha: date) -> float:
            Obtiene la tasa de cambio entre la moneda de origen y COP para una fehca especifica.
        
        convertir_moneda(moneda_origen: str, valor: float, fecha. date) -> float:
            Convierte un valor monetario desde la moneda de origen a COP.
    """
    moneda_local = "cop"
    @staticmethod
    def obtener_tasa_cambio(moneda_destino: str, fecha: date) -> float:
        """
        Obtiene la tasa de cambio entre la moneda de origen y 
        COP usando la API pública de Fawaz Ahmed.
        Usa la fecha actual para construir la URL de la API.

        Args:
            moneda_origen (str): Código de la moneda de origen (ej. 'usd', 'eur').
            fecha (date): Fecha en la que se desea obtener la tasa de cambio.

        Returns:
            float: Tasa de cambio redondeada a 2 decimales.

        Raises:
            RuntimeError: Si ocurre un error en la solicitud o los datos no son válidos.
        """
        moneda_destino = moneda_destino.lower()
        fecha_actual = fecha.strftime("%Y-%m-%d")
        url = (
    f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{fecha_actual}/v1/"
    f"currencies/{moneda_destino}.json"
)
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # lanza HTTPError si status_code != 200

            data = response.json()
            tasa = data[moneda_destino][ControlAPIMonedaIntercambio.moneda_local]
            return round(tasa, 2)

        except requests.exceptions.Timeout:
            print("[ERROR] La solicitud a la API excedió el tiempo de espera.")
        except requests.exceptions.HTTPError as e:
            print(f"[ERROR] Error HTTP al acceder a la API: {e}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error de conexión o petición a la API: {e}")
        except KeyError:
            print(f"[ERROR] La respuesta no contiene tasa para {moneda_destino} -> {ControlAPIMonedaIntercambio.moneda_local}")

        raise RuntimeError("No se pudo obtener una tasa de cambio válida.")
    @staticmethod

    def convertir_moneda(moneda_destino: str, valor: float, fecha:date) -> float:
        """
        Convierte un valor monetario desde la moneda de origen a pesos colombianos (COP),
        utilizando la tasa de cambio actual proporcionada por la API.

        Args:
            moneda_destino (str): Código de la moneda de origen (por ejemplo, 'usd', 'eur').
            valor (float): Monto a convertir.
             fecha (date): Fecha en la que se realizo el gasto y en base a esta se da la tasa de cambio .

        Returns:
            float: Valor convertido a COP, redondeado a 2 decimales.
        """
        tasa = ControlAPIMonedaIntercambio.obtener_tasa_cambio(moneda_destino, fecha)
        print(f"Tasa de cambio {moneda_destino.upper()} -> COPen {fecha.strftime("%Y-%m-%d")}: {tasa}")
        return round(valor * tasa, 2)





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



class ControlGasto:
    """
    Controlador que gestiona los gastos registrados durante un viaje.

    Atributos:
        viaje (Viaje): Objeto del viaje actual.
        control_viaje (ControlViaje): Controlador asociado al viaje.
    """

    def __init__(self, viaje: Viaje, control_viaje: ControlViaje):
        """
        Inicializa el controlador de gastos con un viaje y su controlador.

        Args:
            viaje (Viaje): Objeto del viaje actual.
            control_viaje (ControlViaje): Controlador del viaje.
        """
        self.viaje = viaje
        self.control_viaje = control_viaje

    def validar_medio_pago(self, medio_pago) -> bool:
        """
        Verifica que el medio de pago sea una instancia válida de MedioPago.

        Args:
            medio_pago: Objeto a validar.

        Returns:
            bool: True si es un MedioPago válido, False en caso contrario.
        """
        return isinstance(medio_pago, MedioPago)

    def registrar_gasto(self, fecha, valor: float, medio_pago: MedioPago, tipo_gasto: TipoGasto):
        """
        Registra un gasto en el viaje, validando tipo de cambio si es internacional.

        Args:
            fecha: Fecha del gasto.
            valor (float): Valor original del gasto.
            medio_pago (MedioPago): Medio de pago utilizado.
            tipo_gasto (TipoGasto): Tipo del gasto.

        Raises:
            ViajeFinalizadoError: Si el viaje ya fue finalizado.
        """
        if not self.viaje.estado_viaje:
            raise ViajeFinalizadoError("El viaje ha finalizado, no se pueden registrar más gastos.")

        if self.viaje.tipo_viaje == TipoViaje.INTERNACIONAL:
            moneda_destino = self.viaje.destino.get_moneda_local()
            valor_cop = ControlAPIMonedaIntercambio.convertir_moneda(moneda_destino, valor, fecha)
        else:
            valor_cop = valor

        gasto = Gasto(fecha, valor, medio_pago, tipo_gasto, valor_cop)
        self.viaje.agregar_gasto(gasto)
        print(
            f"Se registró un gasto de {valor} {self.viaje.destino.get_moneda_local()} "
            f"-> {valor_cop} COP"
        )
        diferencia = self.calcular_diferencia_presupuesto(fecha)
        if diferencia > 0:
            print(f"Presupuesto restante para {fecha}: {diferencia} COP")
        elif diferencia == 0:
            print(f"Presupuesto agotado para {fecha}")
        else:
            print(f"Presupuesto excedido para {fecha} por {-diferencia} COP")


    def calcular_diferencia_presupuesto(self, fecha) -> float:
        """
        Calcula la diferencia entre el presupuesto diario y los gastos realizados en una fecha.

        Args:
            fecha: Fecha a evaluar.

        Returns:
            float: Diferencia entre presupuesto diario y gasto total en COP.
        """
        total_cop = self.viaje.calcular_gasto_diario(fecha)
        return self.viaje.presupuesto_diario - total_cop


class ControlReporte:
    """
    Clase encargada de generar reportes sobre los gastos realizados durante un viaje.
    """

    @staticmethod
    def calcular_reporte_gastos_todos_los_dias(_, viaje: Viaje) -> dict:
        """
        Calcula un reporte diario de gastos, diferenciando entre efectivo y tarjeta.

        Args:
            _ (ignored): Parámetro ignorado (usado por compatibilidad).
            viaje (Viaje): Objeto del viaje del cual se extraen los gastos.

        Returns:
            dict: Diccionario donde cada clave es una fecha y el valor es otro
                  diccionario con los montos totales por medio de pago y el total general.
        """
        reporte = {}
        for gasto in viaje.get_gastos():
            fecha = gasto.get_fecha()
            if fecha not in reporte:
                reporte[fecha] = {'efectivo': 0, 'tarjetas': 0, 'total': 0}
            if gasto.get_medio_pago() == MedioPago.EFECTIVO:
                reporte[fecha]['efectivo'] += gasto.get_valor_moneda_local_cop()
            else:
                reporte[fecha]['tarjetas'] += gasto.get_valor_moneda_local_cop()
            reporte[fecha]['total'] += gasto.get_valor_moneda_local_cop()
        return reporte

    @staticmethod
    def reporte_por_tipo(viaje: Viaje) -> dict:
        """
        Calcula un reporte de gastos agrupados por tipo de gasto,
          diferenciando entre efectivo y tarjeta.

        Args:
            viaje (Viaje): Objeto del viaje del cual se extraen los gastos.

        Returns:
            dict: Diccionario donde cada clave es un tipo de gasto y el valor es otro
                  diccionario con los montos totales por medio de pago y el total general.
        """
        reporte = {}
        for tipo in TipoGasto:
            reporte[tipo.name] = {'efectivo': 0, 'tarjetas': 0, 'total': 0}

        for gasto in viaje.get_gastos():
            tipo = gasto.get_tipo_gasto().name
            if gasto.get_medio_pago() == MedioPago.EFECTIVO:
                reporte[tipo]['efectivo'] += gasto.get_valor_moneda_local_cop()
            else:
                reporte[tipo]['tarjetas'] += gasto.get_valor_moneda_local_cop()
            reporte[tipo]['total'] += gasto.get_valor_moneda_local_cop()
        return reporte

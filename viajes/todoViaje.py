import requests
from datetime import date
from enums import TipoViaje, TipoGasto, MedioPago


class Cliente:
    def __init__(self, nombreCompleto: str, cedula: str, telefono: str, correo: str):
        self.nombreCompleto = nombreCompleto
        self.cedula = cedula
        self.telefono = telefono
        self.correo = correo

    def getNombre(self): return self.nombreCompleto
    def getCedula(self): return self.cedula
    def getTelefono(self): return self.telefono
    def getCorreo(self): return self.correo


class Destino:
    def __init__(self, ciudad: str, departamento: str, pais: str, monedaLocal: str):
        self.ciudad = ciudad
        self.departamento = departamento
        self.pais = pais
        self.monedaLocal = monedaLocal

    def getCiudad(self): return self.ciudad
    def getDepartamento(self): return self.departamento
    def getPais(self): return self.pais
    def getMonedaLocal(self): return self.monedaLocal


class Gasto:
    def __init__(self, fecha, valor: float, medioPago: MedioPago, tipoGasto: TipoGasto, valorCOP: float):
        self.fecha = fecha
        self.valor = valor
        self.medioPago = medioPago
        self.tipoGasto = tipoGasto
        self.valorCOP = valorCOP

    def getFecha(self): return self.fecha
    def getValor(self): return self.valor
    def getMedioPago(self): return self.medioPago
    def getTipoGasto(self): return self.tipoGasto
    def getValorCOP(self): return self.valorCOP


class Viaje:
    def __init__(self, fechaInicio, fechaFin, presupuestoDiario: float, destino: Destino, tipoViaje: TipoViaje):
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.presupuestoDiario = presupuestoDiario
        self.destino = destino  # ✅ corregido
        self.tipoViaje = tipoViaje
        self.estadoViaje = True
        self.gastos = []

    def agregarGasto(self, gasto: Gasto):
        if self.estadoViaje:
            self.gastos.append(gasto)
        else:
            raise Exception("El viaje ha finalizado, no se pueden registrar más gastos.")

    def finalizarViaje(self):
        self.estadoViaje = False

    def getGastosPorFecha(self, fecha):
        return [g for g in self.gastos if g.getFecha() == fecha]

    def getGastos(self):
        return self.gastos


class ControlAPIMonedaIntercambio:
    @staticmethod
    def obtenerTasaCambio(moneda_origen: str) -> float:
        moneda_origen = moneda_origen.lower()
        moneda_local = "cop"
        fecha_actual = date.today().strftime("%Y-%m-%d")  # formato YYYY-MM-DD

        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{fecha_actual}/v1/currencies/{moneda_origen}.json"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                tasa = data[moneda_origen][moneda_local]
                return round(tasa, 2)
            else:
                print(f"[ERROR] Código de respuesta de la API: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] No se pudo acceder a la API: {e}")

        raise Exception("No se pudo obtener la tasa de cambio válida para la moneda.")

    @staticmethod
    def convertirMoneda(moneda_origen: str, valor: float) -> float:
        tasa = ControlAPIMonedaIntercambio.obtenerTasaCambio(moneda_origen)
        print(f"Tasa de cambio {moneda_origen.upper()} -> COP: {tasa}")
        return round(valor * tasa, 2)




class ControlViaje:
    def __init__(self):
        self.viaje = None

    def registrarViaje(self, fechaInicio: date, fechaFin: date, presupuestoDiario: float, destino: Destino, tipoViaje: TipoViaje):
        self.viaje = Viaje(fechaInicio, fechaFin, presupuestoDiario, destino, tipoViaje)

    def validarDestino(self):
        return self.viaje.destino is not None

    def iniciarViaje(self):
        self.viaje.estadoViaje = True

    def finalizarViaje(self):
        hoy = date.today()
        if hoy >= self.viaje.fechaFin:
            self.viaje.finalizarViaje()
            print("El viaje se ha finalizado")
        else:
            print("El viaje está aún activo. Fecha de finalización:", self.viaje.fechaFin)

    def getViaje(self):
        return self.viaje


class ControlGasto:
    def __init__(self, viaje: Viaje, control_viaje: ControlViaje):
        self.viaje = viaje
        self.control_viaje = control_viaje

    def validarMedioPago(self, medioPago) -> bool:
        return isinstance(medioPago, MedioPago)

    def registrarGasto(self, fecha, valor: float, medioPago: MedioPago, tipoGasto: TipoGasto):
        if not self.viaje.estadoViaje:
            raise Exception("El viaje ha finalizado, no se pueden registrar más gastos.")

        if self.viaje.tipoViaje == TipoViaje.INTERNACIONAL:
            monedaDestino = self.viaje.destino.getMonedaLocal()
            valorCOP = ControlAPIMonedaIntercambio.convertirMoneda(monedaDestino, valor)
        else:
            valorCOP = valor

        gasto = Gasto(fecha, valor, medioPago, tipoGasto, valorCOP)
        self.viaje.agregarGasto(gasto)
        print(f"Se registró un gasto de {valor} {self.viaje.destino.getMonedaLocal()} -> {valorCOP} COP")

    def calcularDiferenciaPresupuesto(self, fecha) -> float:
        gastos_fecha = self.viaje.getGastosPorFecha(fecha)
        total_cop = sum(g.getValorCOP() for g in gastos_fecha)
        return self.viaje.presupuestoDiario - total_cop


class ControlReporte:
    @staticmethod
    def calcular_reporte_gastos_todos_los_dias(_, viaje: Viaje) -> dict:
        reporte = {}
        for gasto in viaje.getGastos():
            fecha = gasto.getFecha()
            if fecha not in reporte:
                reporte[fecha] = {'efectivo': 0, 'tarjetas': 0, 'total': 0}
            if gasto.getMedioPago() == MedioPago.EFECTIVO:
                reporte[fecha]['efectivo'] += gasto.getValorCOP()
            else:
                reporte[fecha]['tarjetas'] += gasto.getValorCOP()
            reporte[fecha]['total'] += gasto.getValorCOP()
        return reporte

    @staticmethod
    def reportePorTipo(viaje: Viaje) -> dict:
        reporte = {}
        for tipo in TipoGasto:
            reporte[tipo.name] = {'efectivo': 0, 'tarjetas': 0, 'total': 0}

        for gasto in viaje.getGastos():
            tipo = gasto.getTipoGasto().name
            if gasto.getMedioPago() == MedioPago.EFECTIVO:
                reporte[tipo]['efectivo'] += gasto.getValorCOP()
            else:
                reporte[tipo]['tarjetas'] += gasto.getValorCOP()
            reporte[tipo]['total'] += gasto.getValorCOP()
        return reporte

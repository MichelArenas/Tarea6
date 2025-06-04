"""
Módulo para la conversión de monedas utilizando una API pública.

Este módulo permite obtener la tasa de cambio entre una moneda extranjera y pesos colombianos (COP)
para una fecha específica, así como realizar conversiones monetarias automáticas. Utiliza la API de
Fawaz Ahmed para acceder a datos históricos y actuales de tasas de cambio.

Dependencias:
    - requests: Para realizar solicitudes HTTP a la API.
    - datetime.date: Para manejar fechas asociadas a los gastos.
"""

from datetime import date

import requests

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

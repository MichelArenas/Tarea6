"""
Módulo para la conversión de monedas utilizando una API pública.

Este módulo permite obtener la tasa de cambio entre una moneda extranjera y pesos colombianos (COP)
para una fecha específica, así como realizar conversiones monetarias automáticas. Utiliza la API de
Fawaz Ahmed para acceder a datos históricos y actuales de tasas de cambio.

Dependencias:
    - requests: Para realizar solicitudes HTTP a la API.
    - datetime.date: Para manejar fechas asociadas a los gastos.
"""

from datetime import date, timedelta
import requests

class ControlAPIMonedaIntercambio:
    """
    Clase para obtener y convertir tasas de cambio usando la API de Fawaz Ahmed.
    """
    moneda_local = "cop"

    @staticmethod
    def obtener_tasa_cambio(moneda_destino: str, fecha: date) -> float:
        """
        Intenta obtener la tasa de cambio para la fecha dada, y si no existe,
        retrocede un día hasta encontrar una fecha válida.
        """
        moneda_destino = moneda_destino.lower()
        intentos = 7  # intenta con máximo 7 días hacia atrás
        while intentos > 0:
            fecha_str = fecha.strftime("%Y-%m-%d")
            url = (
                f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{fecha_str}/v1/"
                f"currencies/{moneda_destino}.json"
            )
            try:
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                data = response.json()
                tasa = data[moneda_destino][ControlAPIMonedaIntercambio.moneda_local]
                print(f"Tasa de cambio {moneda_destino.upper()} -> COP en {fecha_str}: {tasa}")
                return round(tasa, 2)

            except requests.exceptions.HTTPError as e:
                if response.status_code == 404:
                    fecha -= timedelta(days=1)
                    intentos -= 1
                    continue  # intenta con un día anterior
                else:
                    print(f"[ERROR] Error HTTP: {e}")
            except Exception as e:
                print(f"[ERROR] Otro error: {e}")
                break

        raise RuntimeError("No se pudo obtener una tasa de cambio válida en los últimos días.")

    @staticmethod
    def convertir_moneda(moneda_destino: str, valor: float, fecha: date) -> float:
        """
        Convierte un monto a COP usando la tasa de cambio más cercana disponible.
        """
        tasa = ControlAPIMonedaIntercambio.obtener_tasa_cambio(moneda_destino, fecha)
        return round(valor * tasa, 2)

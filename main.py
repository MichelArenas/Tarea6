"""
Módulo principal de la aplicación de registro de gastos de viaje.

Permite a los usuarios registrar un viaje (nacional o internacional), 
agregar gastos durante las fechas del viaje, y ver reportes por día o por tipo de gasto. 
En caso de viajes internacionales, convierte automáticamente los valores a COP.

El registro se realiza por consola y la información puede mantenerse en memoria.
"""

from datetime import  datetime
from enums.tipo_viaje import TipoViaje
from enums.tipo_gasto import TipoGasto
from enums.medio_pago import MedioPago
from modelos.destino import Destino
from controladores.control_viaje import ControlViaje
from controladores.control_gasto import ControlGasto
from controladores.control_reporte import ControlReporte

def leer_fecha(mensaje):
    """
    Solicita una fecha al usuario y la valida con formato YYYY-MM-DD.

    Args:
        mensaje (str): Mensaje a mostrar al usuario.

    Returns:
        date: Objeto datetime.date válido.
    """
    while True:
        try:
            entrada = input(mensaje + " (formato YYYY-MM-DD): ")
            return datetime.strptime(entrada, "%Y-%m-%d").date()
        except ValueError:
            print("⚠️ Fecha inválida, intenta de nuevo.")

def mostrar_menu_gastos():
    """
    Muestra el menú interactivo para ingresar un gasto.

    Returns:
        tuple: Contiene la fecha, valor, medio de pago y tipo de gasto.
    """
    print("\n--- Registrar gasto ---")
    fecha = leer_fecha("Fecha del gasto")
    valor = float(input("Valor gastado: "))
    print("Medio de pago:\n1. Efectivo\n2. Tarjeta débito\n3. Tarjeta crédito")
    medio_pago = {
        "1": MedioPago.EFECTIVO,
        "2": MedioPago.TARJETA_DEBITO,
        "3": MedioPago.TARJETA_CREDITO
    }[input("Selecciona opción: ")]

    print("Tipo de gasto:\n1. Transporte\n2. Alojamiento\n3. Alimentación\n4. " \
    "Entretenimiento\n5. Compras")
    tipo_gasto = {
        "1": TipoGasto.TRANSPORTE,
        "2": TipoGasto.ALOJAMIENTO,
        "3": TipoGasto.ALIMENTACION,
        "4": TipoGasto.ENTRETENIMIENTO,
        "5": TipoGasto.COMPRAS
    }[input("Selecciona opción: ")]

    return fecha, valor, medio_pago, tipo_gasto

def main():
    """
    Función principal que gestiona el flujo de la aplicación por consola.

    Permite:
    - Registrar un nuevo viaje.
    - Registrar gastos durante el viaje.
    - Generar reportes diarios y por tipo de gasto.
    - Finalizar el viaje y bloquear nuevos registros.
    """
    print(" Bienvenido al registro de gastos de viaje")

    # --- Registro del viaje ---
    tipo = input("¿El viaje es nacional o internacional? (n/i): ").lower()
    tipo_viaje = TipoViaje.NACIONAL if tipo == "n" else TipoViaje.INTERNACIONAL

    ciudad = input("Ciudad destino: ")
    departamento = input("Departamento: ")
    pais = input("País: ")
    moneda = input("Moneda local (ej: cop, usd, eur): ").lower()

    destino = Destino(ciudad, departamento, pais, moneda)
    fecha_inicio = leer_fecha("Fecha de inicio del viaje")
    fecha_fin = leer_fecha("Fecha de fin del viaje")
    presupuesto_diario = float(input("Presupuesto diario en COP: "))

    control_viaje = ControlViaje()
    control_viaje.registrar_viaje(fecha_inicio, fecha_fin, presupuesto_diario, destino, tipo_viaje)
    viaje = control_viaje.get_viaje()
    control_gasto = ControlGasto(viaje, control_viaje)

    # --- Registro de gastos ---
    while viaje.estado_viaje:
        print("\n--- MENÚ ---")
        print("1. Registrar gasto")
        print("2. Finalizar viaje")
        print("3. Ver reporte diario")
        print("4. Ver reporte por tipo")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            try:
                datos = mostrar_menu_gastos()
                control_gasto.registrar_gasto(*datos)
            except Exception as e:
                print(f" Error: {e}")

        elif opcion == "2":
            control_viaje.finalizar_viaje()

        elif opcion == "3":
            reporte_dia = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
            print("\n--- Reporte por día ---")
            for fecha, datos in reporte_dia.items():
                print(f"{fecha}: {datos}")

        elif opcion == "4":
            reporte_tipo = ControlReporte.reporte_por_tipo(viaje)
            print("\n--- Reporte por tipo de gasto ---")
            for tipo, datos in reporte_tipo.items():
                print(f"{tipo}: {datos}")

        else:
            print(" Opción inválida")

    print("\n El viaje ha sido finalizado. No se permiten más gastos.")
    print("--- Reporte final por día ---")
    reporte_dia = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
    for fecha, datos in reporte_dia.items():
        print(f"{fecha}: {datos}")

    print("\n--- Reporte final por tipo ---")
    reporte_tipo = ControlReporte.reporte_por_tipo(viaje)
    for tipo, datos in reporte_tipo.items():
        print(f"{tipo}: {datos}")

if __name__ == "__main__":
    main()

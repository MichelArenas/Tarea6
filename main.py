from datetime import date

from enums.tipo_gasto import TipoGasto

from enums.tipo_viaje import TipoViaje

from enums.medio_pago import MedioPago

from modelos.destino import Destino

from controladores.control_viaje import ControlViaje

from controladores.control_gasto import ControlGasto

from controladores.control_reporte import ControlReporte

# Crear destino internacional (EE.UU.)
destino = Destino("Miami", "Florida", "Estados Unidos", "usd")

# Crear controlador de viaje
control_viaje = ControlViaje()
control_viaje.registrar_viaje(
    fecha_inicio=date(2025, 6, 1),
    fecha_fin=date(2025, 6, 2),
    presupuesto_diario=400000,  # presupuesto diario en COP
    destino=destino,
    tipo_viaje=TipoViaje.INTERNACIONAL
)

# Obtener viaje y asociar control de gasto
viaje = control_viaje.get_viaje()
control_gasto = ControlGasto(viaje, control_viaje)

# Registrar gastos
print("\n--- Registro de gastos ---")
control_gasto.registrar_gasto(
    fecha=date(2025, 6, 1),
    valor=50,  # USD
    medio_pago=MedioPago.TARJETA_CREDITO,
    tipo_gasto=TipoGasto.COMPRAS
)

control_gasto.registrar_gasto(
    fecha=date(2025, 6, 1),
    valor=20,  # USD
    medio_pago=MedioPago.EFECTIVO,
    tipo_gasto=TipoGasto.ALIMENTACION
)

control_gasto.registrar_gasto(
    fecha=date(2025, 6, 2),
    valor=80,  # USD
    medio_pago=MedioPago.TARJETA_CREDITO,
    tipo_gasto=TipoGasto.ALOJAMIENTO
)

# Finalizar viaje (simulación manual, normalmente lo hace solo si la fecha actual >= fechaFin)
print("\n--- Finalizando el viaje ---")
control_viaje.finalizar_viaje()

# Mostrar reportes
print("\n--- Reporte por día ---")
reporte_dia = ControlReporte.calcular_reporte_gastos_todos_los_dias(None, viaje)
for fecha, datos in reporte_dia.items():
    print(f"{fecha}: {datos}")

print("\n--- Reporte por tipo de gasto ---")
reporte_tipo = ControlReporte.reporte_por_tipo(viaje)
for tipo, datos in reporte_tipo.items():
    print(f"{tipo}: {datos}")

# Intentar registrar un nuevo gasto después de finalizar
print("\n--- Intentar registrar gasto luego de finalizar ---")
try:
    control_gasto.registrar_gasto(
        fecha=date(2025, 6, 3),
        valor=30,
        medio_pago=MedioPago.EFECTIVO,
        tipo_gasto=TipoGasto.TRANSPORTE
    )
except Exception as e:
    print(" Error al registrar gasto:", e)

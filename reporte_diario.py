"""
Reporte diario automático por WhatsApp.
"""
import os
from twilio.rest import Client
from utils.excel_reader import get_ultimo_dia, get_acumulado_mes, get_calendario_mes
from datetime import date

def formatear_num(n, decimales=0):
    if n is None: return "-"
    if decimales == 0:
        return f"{int(round(n)):,}".replace(",", ".")
    return f"{n:,.{decimales}f}".replace(",", ".")

def calcular_proyectado(año, mes):
    """Calcula la producción proyectada al cierre del mes."""
    acum = get_acumulado_mes(año, mes)
    cal = get_calendario_mes(año, mes)
    if not acum or not cal:
        return None, None

    prod_real = acum["total_tn"]
    efic_prom = acum["efic_prom"]

    # Días pendientes según calendario
    plan_detalle = cal["plan"]["detalle"]
    hoy = date.today()
    dias_pendientes = [
        d for d, info in plan_detalle.items()
        if info["tipo"] == "produccion"
        and date(año, mes, d) > hoy
    ]
    target_pendiente = sum(
        plan_detalle[d]["target_tn"]
        for d in dias_pendientes
    )

    proyectado = prod_real + target_pendiente
    return round(proyectado, 1), efic_prom

def generar_mensaje(dia=None):
    if dia is None:
        dia = get_ultimo_dia()
    if not dia:
        return "No hay datos disponibles."

    fecha = dia["fecha"]
    año, mes = fecha.year, fecha.month
    fecha_str = dia["fecha_str"]

    # Stock
    stock_hamb = dia.get("stock_hamburguesas")
    stock_hamb_tn = round(stock_hamb / 1000, 1) if stock_hamb else None

    # Proyectado
    proy, efic_acum = calcular_proyectado(año, mes)
    acum = get_acumulado_mes(año, mes)
    efic_acum = acum["efic_prom"] if acum else None

    lineas = [
        f"*Info {fecha_str}*",
        "",
        f"*Produccion:* {formatear_num(dia['prod_total_kg'])} kg | {dia['efic_total_pct']}% | Merma: {dia['merma_pct']}%",
        f"  TM: {formatear_num(dia['prod_tm_kg'])} kg | {dia['efic_tm_pct']}%",
        f"  TT: {formatear_num(dia['prod_tt_kg'])} kg | {dia['efic_tt_pct']}%",
    ]

    if stock_hamb_tn:
        lineas.append(f"*Stock Hamb:* {stock_hamb_tn} tn")

    if proy and efic_acum:
        lineas.append(f"*Proyectado cierre:* {proy} tn | Efic acum: {efic_acum}%")

    return "\n".join(lineas)

DESTINATARIOS = [
    {"numero": "whatsapp:+5491151201504", "nombre": "Nacho"},
    {"numero": "whatsapp:+5491169478423", "nombre": "Romi"},
    {"numero": "whatsapp:+5491125239121", "nombre": "Justi"},
    {"numero": "whatsapp:+5491131124273", "nombre": "Julito"},
    {"numero": "whatsapp:+5491139165742", "nombre": "Migue"},
]

def enviar_reporte(solo_preview=False):
    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token  = os.environ["TWILIO_AUTH_TOKEN"]
    from_number = os.environ["TWILIO_WHATSAPP_FROM"]

    client = None
    if not solo_preview:
        client = Client(account_sid, auth_token)

    base_mensaje = generar_mensaje()

    for dest in DESTINATARIOS:
        numero = dest["numero"]
        nombre = dest["nombre"]
        mensaje = f"Buen dia {nombre}!\n" + base_mensaje
        print(f"--- Mensaje para {nombre} ({numero}) ---")
        print(mensaje)
        print()
        if not solo_preview:
            try:
                msg = client.messages.create(
                    body=mensaje,
                    from_=from_number,
                    to=numero
                )
                print(f"✅ Enviado a {nombre} - SID: {msg.sid}")
            except Exception as e:
                print(f"❌ Error enviando a {nombre}: {e}")

if __name__ == "__main__":
    enviar_reporte()

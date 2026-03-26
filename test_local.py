"""
Probá el bot localmente sin necesitar WhatsApp.
Ejecutar: python test_local.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from utils.excel_reader import get_contexto_completo, get_ultimo_dia, get_resumen_mensual
from utils.claude_handler import preguntar_a_claude

print("=" * 60)
print("BOT DE OPERACIONES - Modo prueba local")
print("Escribí tu pregunta o 'salir' para terminar")
print("=" * 60)

# Verificar que el Excel está cargado
try:
    ultimo = get_ultimo_dia()
    if ultimo:
        print(f"\n✅ Excel cargado. Último día con datos: {ultimo['fecha_str']}")
    else:
        print("\n⚠️  Excel cargado pero sin datos de producción aún.")
except Exception as e:
    print(f"\n❌ Error al leer el Excel: {e}")
    print("   Asegurate de que el archivo esté en data/operaciones.xlsx")
    sys.exit(1)

print()

while True:
    try:
        pregunta = input("Vos: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nChau!")
        break

    if pregunta.lower() in ("salir", "exit", "quit"):
        print("Chau!")
        break

    if not pregunta:
        continue

    print("\nBot: ", end="", flush=True)
    try:
        contexto = get_contexto_completo(pregunta)
        respuesta = preguntar_a_claude(pregunta, contexto)
        print(respuesta)
    except Exception as e:
        print(f"Error: {e}")
    print()

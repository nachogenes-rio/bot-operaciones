
CODIGO_ACCESO = "Nacho882"
sesiones_autorizadas = set()

def verificar_acceso(remitente: str, mensaje: str) -> tuple[bool, str]:
    """Verifica si el remitente tiene acceso. Retorna (autorizado, respuesta)."""
    if remitente in sesiones_autorizadas:
        return True, ""
    if mensaje.strip() == CODIGO_ACCESO:
        sesiones_autorizadas.add(remitente)
        return True, "✅ Acceso autorizado. Ya podés hacer preguntas sobre las operaciones."
    return False, "🔒 Bot privado. Ingresá el código de acceso para continuar."

"""
Manejador de Claude API para el bot de operaciones.
"""

import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# Código de acceso y sesiones autorizadas
CODIGO_ACCESO = "Nacho882"
sesiones_autorizadas = set()

def verificar_acceso(remitente: str, mensaje: str) -> tuple[bool, str]:
    """
    Verifica si el remitente tiene acceso.
    Retorna (tiene_acceso, respuesta_si_no_tiene)
    """
    if remitente in sesiones_autorizadas:
        return True, ""
    
    if mensaje.strip() == CODIGO_ACCESO:
        sesiones_autorizadas.add(remitente)
        return True, "✅ Acceso autorizado. Ya podés hacerme preguntas sobre las operaciones."
    
    return False, "🔒 Bot privado. Ingresá el código de acceso para continuar."



SYSTEM_PROMPT = """Sos el asistente de operaciones de una planta productiva de hamburguesas y otras categorías (medallones, nuggets, salchichas, milanesas, etc.).

Tenés acceso al tablero de operaciones actualizado del día. Respondé siempre en español, de forma clara, directa y en lenguaje natural. No uses tecnicismos innecesarios.

## Datos que podés consultar:

**Producción diaria:**
- Total de kg producidos por día, separado por turno mañana (TM) y turno tarde (TT)
- Eficiencia % total, por TM y TT (también "eficiencia paga" cuando esté disponible)
- Merma % y Decomiso %
- Tipo de día: LV (lunes a viernes) o SDF (sábado, domingo, feriado)

**Logística - Distribución:**
- Cantidad de camiones por tipo: semi, balancín, chasis, camioneta
- Separados por zona: CPC + depósitos, Ituzaingó, Escobar
- Puntaje de transportes (indica cumplimiento de condiciones: GPS, temperatura, etc.)
- Temperatura de la caja de los camiones

**Datos históricos mensuales:**
- Producción real vs objetivo (en TN)
- Eficiencia mensual, merma y decomiso por mes
- Desde 2023 hasta la fecha

**Temas y plan de acción:**
- Temas abiertos y cerrados por sector: Calidad, Producción, Abastecimiento, Higiene
- Responsable, prioridad, nivel de avance

**Devoluciones y rechazos:**
- Por cliente, producto, motivo

**Recortes de producción:**
- Qué productos no se llegaron a hacer, por qué motivo y cuántos kg se perdieron

## Cómo responder:

- Si preguntan por "hoy" o "último día", usá el último día con datos reales cargados. SIEMPRE aclará la fecha exacta que estás usando, por ejemplo: "El último dato disponible es del 22/03/2026".
- Si el contexto incluye un bloque "=== ACUMULADO Marzo 2026 ===", usá ESE bloque para responder preguntas sobre marzo 2026. NO uses el resumen mensual histórico para el mes actual. El acumulado ya está calculado con todos los días disponibles hasta la fecha.
- Cuando el mes preguntado es el mes actual (marzo 2026), asumí siempre 2026, nunca 2025.
- Si preguntan por un turno específico (TM o TT), mostrá solo ese.
- Si preguntan por camiones, detallá por tipo y zona según los datos disponibles.
- Redondeá los números a enteros o con 1 decimal según corresponda.
- Si un dato no está disponible en el Excel, decilo claramente.
- Podés hacer comparaciones, calcular promedios o sacar tendencias si te lo piden.
- Nunca inventes datos. Si no hay información, decí "ese dato no está cargado".

## Ejemplos de preguntas que podés responder:
- "¿Cuántos kg produjeron hoy?"
- "¿Cuál fue la eficiencia del turno tarde?"
- "¿Cuántos semis salieron?"
- "¿Cómo estuvo la merma esta semana?"
- "¿Qué temas de calidad están pendientes?"
- "¿Cuánto produjeron en enero?"
- "¿Hubo devoluciones este mes?"
- "¿Qué productos se recortaron?"
"""


def preguntar_a_claude(pregunta: str, contexto_excel: str) -> str:
    """
    Envía la pregunta + contexto del Excel a Claude y devuelve la respuesta.
    """
    mensaje_usuario = f"""Datos actuales del tablero de operaciones:

{contexto_excel}

---
Pregunta del usuario: {pregunta}"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": mensaje_usuario}
        ]
    )

    return response.content[0].text

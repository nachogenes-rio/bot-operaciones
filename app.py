"""
Bot de WhatsApp para operaciones de planta.
Recibe mensajes de Twilio, lee el Excel y consulta a Claude.
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils.excel_reader import get_contexto_completo
from utils.claude_handler import preguntar_a_claude
import schedule
import time
import threading
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

def job_reporte():
    from reporte_diario import enviar_reporte
    enviar_reporte()

schedule.every().day.at("10:30").do(job_reporte)

def correr_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(30)

hilo = threading.Thread(target=correr_scheduler, daemon=True)
hilo.start()


@app.route("/webhook", methods=["POST"])
def webhook():
    pregunta = request.form.get("Body", "").strip()
    remitente = request.form.get("From", "")

    from utils.claude_handler import verificar_acceso
    autorizado, msg_acceso = verificar_acceso(remitente, pregunta)

    if not autorizado:
        respuesta = msg_acceso
    elif not pregunta:
        respuesta = "Hola! Mandame tu pregunta sobre las operaciones de la planta."
    else:
        try:
            contexto = get_contexto_completo(pregunta)
            respuesta = preguntar_a_claude(pregunta, contexto)
        except Exception as e:
            respuesta = f"Hubo un error al procesar tu consulta: {str(e)}"

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respuesta)
    return str(resp)


@app.route("/", methods=["GET"])
def index():
    return "Bot de operaciones activo ✅", 200


if __name__ == "__main__":
    app.run(debug=False, port=5000)

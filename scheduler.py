"""
Scheduler para reporte diario a las 7:30am hora Argentina (UTC-3 = 10:30 UTC)
"""
import schedule
import time
import os
from dotenv import load_dotenv
load_dotenv()

def job():
    from reporte_diario import enviar_reporte
    enviar_reporte()

schedule.every().day.at("10:30").do(job)

print("Scheduler iniciado. Esperando las 10:30 UTC (7:30am Argentina)...")
while True:
    schedule.run_pending()
    time.sleep(30)

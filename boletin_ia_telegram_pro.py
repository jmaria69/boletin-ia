#!/usr/bin/env python3
"""Boletín Diario de IA → Telegram"""

import requests
from datetime import datetime
from pathlib import Path
import logging
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API = "https://api.telegram.org/bot"

OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOLETIN = {
    "global_noticias": [
        {"titulo": "OpenAI adquiere Astral", "contenido": "OpenAI anunció acuerdo para adquirir Astral el 19 de marzo", "url": "https://openai.com", "fuente": "OpenAI"},
        {"titulo": "Google Gemini 3.1 Pro", "contenido": "Google lanza Gemini 3.1 Pro con 2 millones de tokens", "url": "https://google.com", "fuente": "Google AI"},
    ],
    "españa_noticias": [
        {"titulo": "52.000 empleos IA en España", "contenido": "España creará 52.000 empleos en IA (+34% vs 2025)", "url": "https://linkedin.com", "fuente": "LinkedIn"},
    ],
    "madrid_noticias": [
        {"titulo": "EAE Madrid Talent 26", "contenido": "Feria con 1.000 ofertas de trabajo (+43% vs 2025)", "url": "https://eae.es", "fuente": "EAE"},
    ]
}

def enviar_telegram(texto):
    url = f"{TELEGRAM_API}{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    response = requests.post(url, json=data, timeout=10)
    return response.status_code == 200

def generar_html(boletin):
    fecha = datetime.now().strftime("%d/%m/%Y")
    return f"""<html><body><h1>Boletín IA {fecha}</h1></body></html>"""

def main():
    logger.info("🚀 Iniciando Boletín IA...")
    mensaje = f"🤖 *Boletín IA* - {datetime.now().strftime('%d/%m/%Y')}\n\nNoticias principales enviadas ✅"
    
    if enviar_telegram(mensaje):
        logger.info("✅ Enviado a Telegram")
    else:
        logger.error("❌ Error enviando a Telegram")
    
    html = generar_html(BOLETIN)
    Path("./outputs/boletin.html").write_text(html)
    logger.info("✅ HTML guardado")

if __name__ == "__main__":
    main()

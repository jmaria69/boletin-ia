#!/usr/bin/env python3
"""
Boletín Diario de IA → Telegram + Gmail
- Envía 3 mensajes a Telegram (uno por nivel)
- Envía HTML completo por Gmail
"""

import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
import logging
import os

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN — variables de entorno (secretos de GitHub)
# ═══════════════════════════════════════════════════════════════

TELEGRAM_TOKEN   = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API     = "https://api.telegram.org/bot"

GMAIL_USER     = os.getenv("GMAIL_USER", "jmaria.romero79@gmail.com")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")   # contraseña de aplicación Gmail

OUTPUT_DIR = Path("./outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# NOTICIAS — actualiza este bloque cada vez que quieras nuevas
# ═══════════════════════════════════════════════════════════════



# ═══════════════════════════════════════════════════════════════
# TELEGRAM — 3 mensajes separados (uno por nivel)
# ═══════════════════════════════════════════════════════════════

def enviar_telegram(texto: str) -> bool:
    """Envía un mensaje a Telegram."""
    url = f"{TELEGRAM_API}{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }
    try:
        r = requests.post(url, json=data, timeout=10)
        if r.status_code == 200:
            logger.info("✅ Mensaje Telegram enviado")
            return True
        logger.error(f"❌ Error Telegram: {r.text}")
        return False
    except Exception as e:
        logger.error(f"❌ Excepción Telegram: {e}")
        return False


def construir_bloque(noticias: list, titulo: str) -> str:
    """Construye un bloque de noticias para Telegram en Markdown."""
    texto = f"{titulo}\n\n"
    for i, n in enumerate(noticias, 1):
        texto += f"*{i}. {n['titulo']}*\n"
        texto += f"{n['contenido']}\n"
        if n.get("url"):
            texto += f"[Leer más →]({n['url']})\n"
        texto += "\n"
    texto += f"_Boletín IA · {datetime.now().strftime('%d/%m/%Y %H:%M')}_"
    return texto


def enviar_boletin_telegram():
    """Envía el boletín a Telegram en 3 mensajes separados."""
    fecha = datetime.now().strftime("%d/%m/%Y")

    # Cabecera
    enviar_telegram(f"📰 *BOLETÍN DIARIO DE IA — {fecha}*\n\n_Edición en 3 bloques: Global 🌍 · España 🇪🇸 · Madrid 🏛️_")

    # Nivel 1 — Global
    enviar_telegram(construir_bloque(NOTICIAS_GLOBAL, "🌍 *NIVEL 1 — GLOBAL*"))

    # Nivel 2 — España
    enviar_telegram(construir_bloque(NOTICIAS_ESPANA, "🇪🇸 *NIVEL 2 — ESPAÑA*"))

    # Nivel 3 — Madrid
    enviar_telegram(construir_bloque(NOTICIAS_MADRID, "🏛️ *NIVEL 3 — MADRID*"))

    logger.info("✅ Boletín completo enviado a Telegram en 4 mensajes")


# ═══════════════════════════════════════════════════════════════
# GMAIL — HTML completo
# ═══════════════════════════════════════════════════════════════

def generar_html() -> str:
    """Genera el HTML completo del boletín."""
    fecha = datetime.now().strftime("%d de %B de %Y")

    def cards(noticias, titulo):
        html = f"<h2 style='color:#667eea;border-bottom:2px solid #667eea;padding-bottom:8px;margin-top:30px;'>{titulo}</h2>"
        for n in noticias:
            html += f"""
            <div style='background:#f9f9f9;border-left:4px solid #667eea;padding:16px;margin:12px 0;border-radius:4px;'>
                <h3 style='color:#333;margin:0 0 8px;font-size:16px;'>{n['titulo']}</h3>
                <p style='color:#555;font-size:14px;margin:0 0 8px;line-height:1.6;'>{n['contenido']}</p>
                <small style='color:#999;'>Fuente: {n['fuente']}</small>
                {'<br><a href="' + n["url"] + '" style="color:#667eea;font-weight:bold;text-decoration:none;">Leer más →</a>' if n.get('url') else ''}
            </div>"""
        return html

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boletín IA Diario — {fecha}</title>
</head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Segoe UI',Arial,sans-serif;">
    <div style="max-width:700px;margin:20px auto;background:#fff;border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.1);overflow:hidden;">
        <div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:40px 30px;text-align:center;">
            <div style="font-size:48px;">📰</div>
            <h1 style="color:#fff;margin:10px 0 4px;font-size:28px;">Boletín Diario de IA</h1>
            <p style="color:rgba(255,255,255,0.85);margin:0;font-size:14px;">{fecha}</p>
        </div>
        <div style="padding:30px;">
            {cards(NOTICIAS_GLOBAL, '🌍 NIVEL 1 — GLOBAL')}
            {cards(NOTICIAS_ESPANA, '🇪🇸 NIVEL 2 — ESPAÑA')}
            {cards(NOTICIAS_MADRID, '🏛️ NIVEL 3 — MADRID')}
        </div>
        <div style="text-align:center;padding:20px;background:#f9f9f9;color:#999;font-size:12px;border-top:1px solid #eee;">
            Boletín generado automáticamente · roco26_bot · {datetime.now().strftime('%Y-%m-%d %H:%M')}
        </div>
    </div>
</body>
</html>"""


def enviar_gmail(html: str) -> bool:
    """Envía el boletín HTML por Gmail."""
    if not GMAIL_PASSWORD:
        logger.error("❌ GMAIL_APP_PASSWORD no configurado")
        return False

    fecha = datetime.now().strftime("%d/%m/%Y")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"📰 Boletín IA Diario — {fecha}"
    msg["From"]    = GMAIL_USER
    msg["To"]      = GMAIL_USER
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())
        logger.info("✅ Boletín enviado por Gmail")
        return True
    except Exception as e:
        logger.error(f"❌ Error Gmail: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    logger.info(f"🚀 Iniciando Boletín IA — {datetime.now().strftime('%H:%M:%S')}")

    # 1. Telegram
    enviar_boletin_telegram()

    # 2. Gmail
    html = generar_html()
    enviar_gmail(html)

    # 3. Guardar HTML localmente
    fecha_str = datetime.now().strftime("%Y%m%d_%H%M")
    filepath = OUTPUT_DIR / f"boletin_ia_{fecha_str}.html"
    filepath.write_text(html, encoding="utf-8")
    logger.info(f"✅ HTML guardado: {filepath}")

    logger.info("✅ Boletín completado")


if __name__ == "__main__":
    main()

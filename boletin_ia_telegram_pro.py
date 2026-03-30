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

NOTICIAS_GLOBAL = [
    {
        "titulo": "OpenAI adquiere Astral: revolución en el ecosistema Python",
        "contenido": "OpenAI anunció el 19 de marzo su acuerdo para adquirir Astral, la organización detrás de herramientas de código abierto ampliamente usadas en la comunidad Python. Esta adquisición fortalece la posición de OpenAI en infraestructura de desarrollo.",
        "url": "https://openai.com",
        "fuente": "OpenAI News"
    },
    {
        "titulo": "Google lanza Gemini 3.1 Pro con contexto de 2 millones de tokens",
        "contenido": "Google contraatacó en marzo con Gemini 3.1 Pro, expandiendo la capacidad de contexto a 2 millones de tokens. Esta mejora permite procesar documentos enormes y proyectos complejos en una sola sesión.",
        "url": "https://blog.google/technology/ai/",
        "fuente": "Google AI Blog"
    },
    {
        "titulo": "OpenAI lanza GPT-5.4 optimizado para razonamiento avanzado",
        "contenido": "El 5 de marzo, OpenAI presentó GPT-5.4 enfocado en razonamiento paso a paso y programación avanzada con mayor eficiencia de costo en API. Representa un refinamiento significativo en la capacidad de resolver problemas técnicos complejos.",
        "url": "https://openai.com/blog",
        "fuente": "OpenAI News"
    },
    {
        "titulo": "SpaceX anuncia planes para adquirir xAI de Elon Musk por $1,25 billones",
        "contenido": "SpaceX comunicó el acuerdo para adquirir xAI en una transacción que valora la entidad combinada en aproximadamente $1,25 billones de dólares, consolidando el control empresarial sobre tecnología de IA de punta.",
        "url": "https://techcrunch.com",
        "fuente": "TechCrunch"
    },
    {
        "titulo": "NVIDIA GTC 2026: Groq 3 LPX y previsión de $1 billón en chips IA",
        "contenido": "El CEO Jensen Huang presentó en GTC 2026 el rack de inferencia Groq 3 LPX y proyectó una demanda de $1 billón en chips de IA a través de 2027. También presentó guardias NemoClaw para agentes de IA.",
        "url": "https://nvidia.com",
        "fuente": "NVIDIA"
    },
    {
        "titulo": "OpenAI lanza Sora 2: generación de video con seguridad incorporada",
        "contenido": "El 23 de marzo, OpenAI publicó Sora 2 para generar videos asistidos por IA con seguridad incorporada desde el inicio. La plataforma busca establecer estándares éticos en síntesis de video.",
        "url": "https://openai.com/sora",
        "fuente": "OpenAI"
    },
]

NOTICIAS_ESPANA = [
    {
        "titulo": "España creará 52.000 nuevos puestos en IA durante 2026",
        "contenido": "Según LinkedIn y el ONTSI, España creará más de 52.000 empleos en IA (+34% vs 2025). Madrid concentra el 45% de las ofertas con salario medio de 54.000€, seguida de Barcelona (30%) y Valencia (8%).",
        "url": "https://www.javadex.es/blog/empleos-ia-espana-nuevos-puestos-mercado-laboral-2026",
        "fuente": "Javadex / ONTSI"
    },
    {
        "titulo": "UGT presenta estudio sobre empleo tecnológico en España 2026",
        "contenido": "El sindicato UGT publicó su análisis del impacto de la automatización y la IA en el mercado laboral español, subrayando la necesidad urgente de reskilling y políticas de transición justa para los trabajadores.",
        "url": "https://www.ugt.es/ugt-presenta-el-estudio-empleo-tecnologico-en-el-mercado-laboral-espanol-2026",
        "fuente": "UGT"
    },
    {
        "titulo": "67% de trabajadores españoles se sienten poco preparados para el cambio",
        "contenido": "Una encuesta reveló que el 67% de los trabajadores españoles se siente poco preparado para encontrar nuevo empleo en 2026, mientras que el 58% considera que la búsqueda de trabajo es más complicada que hace un año.",
        "url": "https://www.bolsamania.com/capitalbolsa/noticias_amp/social/la-ia-marca-el-empleo-de-2026",
        "fuente": "Bolsamania"
    },
    {
        "titulo": "27,4% de empleos españoles expuestos a la IA generativa",
        "contenido": "España supera la media europea con un 27,4% de empleos expuestos a la IA generativa. Expertos coinciden en que la IA reconfigurará perfiles en lugar de sustituir masivamente al empleo, acelerando la necesidad de reskilling continuo.",
        "url": "https://vandal.elespanol.com/random/espana-perdera-15-millones-de-puestos-de-trabajo-en-2026",
        "fuente": "El Español"
    },
    {
        "titulo": "LinkedIn revela los empleos más demandados en España para 2026",
        "contenido": "Ingenieros de IA/ML, arquitectos Cloud (AWS, Azure, GCP), expertos en ciberseguridad y analistas de datos lideran la demanda. La IA, ingeniería y logística son los sectores con mayor crecimiento según LinkedIn.",
        "url": "https://www.marketingdirecto.com/digital-general/digital/linkedin-revela-empleos-auge-2026-ia-redefine-futuro-laboral-espana",
        "fuente": "LinkedIn / Marketing Directo"
    },
]

NOTICIAS_MADRID = [
    {
        "titulo": "EAE Madrid Talent 26: récord con 1.000 ofertas de empleo",
        "contenido": "La 11ª edición reunió a más de 100 empresas y 1.000 estudiantes para debatir cómo la IA redefine la empleabilidad. La feria superó todos sus récords con un 43% más de ofertas que en 2025.",
        "url": "https://comunidaria.com/eae-madrid-talent-26-ia-tiktok-definen-empleo/",
        "fuente": "Comunidaria"
    },
    {
        "titulo": "Comunidad de Madrid amplía formación en IA para 200.000 empleados públicos",
        "contenido": "El plan de formación 2026 incluye 1.246 cursos para 200.000 empleados públicos, con 64.607 plazas y prioridades en transformación digital, IA aplicada a procedimientos administrativos y emprendimiento interno.",
        "url": "https://www.eldiariodemadrid.es/articulo/educacion/plan-formacion-2026-comunidad-madrid",
        "fuente": "El Diario de Madrid"
    },
    {
        "titulo": "CEI ofrece Curso de IA presencial en Madrid (180h)",
        "contenido": "Próximos inicios: 13 de abril o 29 de junio 2026. Duración 2-3 meses en modalidad presencial. Cubre fundamentos de IA, Machine Learning y aplicaciones prácticas.",
        "url": "https://cei.es/cei-curso/curso-inteligencia-artificial-ia-madrid/",
        "fuente": "CEI Madrid"
    },
    {
        "titulo": "Universidad Europea lanza Máster en IA con opciones online y presencial",
        "contenido": "El Máster en Inteligencia Artificial ofrece inicio online en abril 2026 y presencial en octubre 2026, formando especialistas en aplicaciones prácticas de IA para empresa.",
        "url": "https://universidadeuropea.com/master-inteligencia-artificial-madrid/",
        "fuente": "Universidad Europea"
    },
]


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

#!/usr/bin/env python3
"""
Boletín Diario de IA → Telegram (Versión Pro)

Envía dos mensajes a Telegram:
1. Mensaje conciso con 3-4 noticias principales por nivel
2. Archivo HTML completo con todas las noticias
"""

import requests
from datetime import datetime
from typing import TypedDict, Optional
from pathlib import Path
import logging

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════

TELEGRAM_TOKEN = "8678147787:AAEAHxSrm4WOcQRE8zY4JiWwWEcAat_NH5g"
TELEGRAM_CHAT_ID = "867107949"
TELEGRAM_API = "https://api.telegram.org/bot"

OUTPUT_DIR = Path("/sessions/brave-keen-goldberg/mnt/outputs")

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
# TIPOS
# ═══════════════════════════════════════════════════════════════

class Noticia(TypedDict):
    """Estructura de una noticia de IA."""
    titulo: str
    contenido: str
    url: Optional[str]
    fuente: str


class Boletin(TypedDict):
    """Estructura del boletín completo."""
    global_noticias: list[Noticia]
    españa_noticias: list[Noticia]
    madrid_noticias: list[Noticia]


# ═══════════════════════════════════════════════════════════════
# FUNCIONES DE BÚSQUEDA
# ═══════════════════════════════════════════════════════════════

async def buscar_noticias_nivel(
    nivel: str,
    keywords: list[str],
    max_results: int = 8
) -> list[Noticia]:
    """
    Busca noticias para un nivel específico.

    Args:
        nivel: "global", "españa" o "madrid"
        keywords: palabras clave para la búsqueda
        max_results: máximo de noticias a retornar

    Returns:
        Lista de noticias encontradas
    """
    noticias = []

    # Simulación de búsqueda (en producción, usar WebSearch real)
    logger.info(f"Buscando noticias para nivel: {nivel}")

    # En una implementación real, aquí irían las búsquedas de WebSearch
    # Por ahora retornamos datos de ejemplo

    return noticias[:max_results]


def generar_mensaje_telegram(boletin: Boletin) -> str:
    """
    Genera un mensaje conciso para Telegram (3-4 noticias por nivel).

    Args:
        boletin: Datos del boletín

    Returns:
        Texto formateado en Markdown para Telegram
    """
    fecha = datetime.now().strftime("%d/%m/%Y")

    mensaje = f"🤖 *BOLETÍN IA DIARIO — {fecha}*\n\n"

    # NIVEL 1 - GLOBAL
    mensaje += "🌍 *GLOBAL* (Top 3)\n"
    for i, noticia in enumerate(boletin["global_noticias"][:3], 1):
        mensaje += f"\n{i}. *{noticia['titulo']}*\n"
        mensaje += f"_{noticia['contenido'][:100]}..._\n"
        if noticia.get("url"):
            mensaje += f"[Leer →]({noticia['url']})\n"

    # NIVEL 2 - ESPAÑA
    mensaje += "\n" + "━" * 40 + "\n"
    mensaje += "\n🇪🇸 *ESPAÑA* (Top 3)\n"
    for i, noticia in enumerate(boletin["españa_noticias"][:3], 1):
        mensaje += f"\n{i}. *{noticia['titulo']}*\n"
        mensaje += f"_{noticia['contenido'][:100]}..._\n"
        if noticia.get("url"):
            mensaje += f"[Leer →]({noticia['url']})\n"

    # NIVEL 3 - MADRID
    mensaje += "\n" + "━" * 40 + "\n"
    mensaje += "\n🏛️ *MADRID* (Top 2-3)\n"
    for i, noticia in enumerate(boletin["madrid_noticias"][:3], 1):
        mensaje += f"\n{i}. *{noticia['titulo']}*\n"
        mensaje += f"_{noticia['contenido'][:100]}..._\n"
        if noticia.get("url"):
            mensaje += f"[Leer →]({noticia['url']})\n"

    mensaje += f"\n\n📄 Boletín completo en archivo HTML anexado\n"
    mensaje += f"_Generado automáticamente • roco26_"

    return mensaje


def generar_html(boletin: Boletin) -> str:
    """
    Genera un HTML completo con todas las noticias.

    Args:
        boletin: Datos del boletín

    Returns:
        HTML formateado
    """
    fecha = datetime.now().strftime("%d de %B de %Y")

    # Generar tarjetas de noticias
    def generar_cards(noticias: list[Noticia], titulo: str) -> str:
        cards = f"<h2 style='color:#667eea;margin-top:30px;border-bottom:2px solid #667eea;padding-bottom:10px;'>{titulo}</h2>\n"
        for noticia in noticias:
            cards += f"""
            <div style="background:#f9f9f9;border-left:4px solid #667eea;padding:15px;margin:15px 0;border-radius:4px;">
                <h3 style="color:#333;margin:0 0 8px 0;font-size:16px;">{noticia['titulo']}</h3>
                <p style="color:#666;font-size:13px;margin:0 0 8px 0;line-height:1.5;">{noticia['contenido']}</p>
                <small style="color:#999;">Fuente: {noticia['fuente']}</small>
                {f'<br><a href="{noticia["url"]}" style="color:#667eea;text-decoration:none;font-weight:bold;">Leer más →</a>' if noticia.get('url') else ''}
            </div>
            """
        return cards

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Boletín IA Diario - {fecha}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                padding: 40px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 30px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2em;
            }}
            .header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
            }}
            a {{
                color: #667eea;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📰 Boletín Diario de IA</h1>
                <p>Noticias relevantes sobre inteligencia artificial</p>
                <p><small>{fecha}</small></p>
            </div>

            {generar_cards(boletin['global_noticias'], '🌍 NIVEL 1 — GLOBAL')}
            {generar_cards(boletin['españa_noticias'], '🇪🇸 NIVEL 2 — ESPAÑA')}
            {generar_cards(boletin['madrid_noticias'], '🏛️ NIVEL 3 — MADRID')}

            <hr style="margin-top: 40px; border: none; border-top: 1px solid #ddd;">
            <p style="text-align: center; color: #999; font-size: 12px;">
                Boletín generado automáticamente • roco26_bot • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </p>
        </div>
    </body>
    </html>
    """
    return html


def enviar_telegram_mensaje(texto: str) -> bool:
    """
    Envía un mensaje de texto a Telegram.

    Args:
        texto: Contenido del mensaje

    Returns:
        True si se envió exitosamente
    """
    url = f"{TELEGRAM_API}{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False,
    }

    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            logger.info("✅ Mensaje enviado a Telegram exitosamente")
            return True
        else:
            logger.error(f"❌ Error al enviar mensaje: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Excepción al enviar mensaje: {e}")
        return False


def enviar_telegram_documento(html_content: str, filename: str) -> bool:
    """
    Envía un documento HTML a Telegram.

    Args:
        html_content: Contenido HTML
        filename: Nombre del archivo

    Returns:
        True si se envió exitosamente
    """
    # Guardar HTML temporalmente
    temp_path = OUTPUT_DIR / filename
    temp_path.write_text(html_content, encoding="utf-8")

    url = f"{TELEGRAM_API}{TELEGRAM_TOKEN}/sendDocument"

    try:
        with open(temp_path, "rb") as f:
            files = {"document": f}
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "caption": "📄 Boletín completo en HTML",
            }
            response = requests.post(url, files=files, data=data, timeout=15)

        if response.status_code == 200:
            logger.info(f"✅ Documento enviado: {filename}")
            return True
        else:
            logger.error(f"❌ Error al enviar documento: {response.text}")
            return False
    except Exception as e:
        logger.error(f"❌ Excepción al enviar documento: {e}")
        return False


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    """Función principal."""
    logger.info("🚀 Iniciando Boletín IA...")

    # Crear directorio de outputs si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Buscar noticias (placeholder - en producción usar WebSearch real)
    logger.info("📰 Buscando noticias...")

    # Datos de ejemplo para demostración
    boletin: Boletin = {
        "global_noticias": [
            {
                "titulo": "OpenAI adquiere Astral: revolución en Python",
                "contenido": "OpenAI anunció el 19 de marzo su acuerdo para adquirir Astral, la organización detrás de herramientas de código abierto ampliamente usadas en la comunidad Python.",
                "url": "https://example.com/astral",
                "fuente": "OpenAI News"
            },
            {
                "titulo": "Google Gemini 3.1 Pro: 2 millones de tokens",
                "contenido": "Google contraatacó en marzo con Gemini 3.1 Pro, expandiendo significativamente la capacidad de contexto a 2 millones de tokens.",
                "url": "https://example.com/gemini",
                "fuente": "Google AI"
            },
            {
                "titulo": "GPT-5.4: optimizado para razonamiento",
                "contenido": "El 5 de marzo, OpenAI presentó GPT-5.4, enfocado en razonamiento paso a paso y programación avanzada.",
                "url": "https://example.com/gpt54",
                "fuente": "OpenAI News"
            },
            {
                "titulo": "SpaceX-xAI: transacción de $1.25 billones",
                "contenido": "SpaceX comunicó el acuerdo para adquirir xAI de Elon Musk en una valuación de aproximadamente $1,25 billones.",
                "url": "https://example.com/spacex-xai",
                "fuente": "Tech News"
            },
        ],
        "españa_noticias": [
            {
                "titulo": "España creará 52.000 empleos en IA en 2026",
                "contenido": "Según LinkedIn y el ONTSI, España creará más de 52.000 empleos en IA (+34% vs 2025). Madrid concentra el 45% con salario medio de 54.000€.",
                "url": "https://example.com/empleos-ia",
                "fuente": "LinkedIn Spain"
            },
            {
                "titulo": "UGT publica estudio sobre empleo tecnológico",
                "contenido": "El sindicato UGT publicó un análisis del impacto de la automatización y la IA en el mercado laboral español 2026.",
                "url": "https://example.com/ugt-tech",
                "fuente": "UGT"
            },
            {
                "titulo": "67% de trabajadores españoles se sienten poco preparados",
                "contenido": "Una encuesta reveló que el 67% de trabajadores se siente poco preparado para encontrar nuevo empleo en 2026.",
                "url": "https://example.com/encuesta",
                "fuente": "CIS"
            },
        ],
        "madrid_noticias": [
            {
                "titulo": "EAE Madrid Talent 26: récord con 1.000 ofertas",
                "contenido": "La 11ª edición reunió a 100+ empresas con 1.000 ofertas de trabajo (+43% vs 2025).",
                "url": "https://comunidaria.com/eae-madrid-talent-26",
                "fuente": "EAE"
            },
            {
                "titulo": "CEI ofrece Curso de IA presencial (180h)",
                "contenido": "Próximos inicios: 13 de abril o 29 de junio 2026. Modalidad presencial en Madrid.",
                "url": "https://cei.es/cei-curso/curso-inteligencia-artificial-ia-madrid/",
                "fuente": "CEI"
            },
        ]
    }

    # Generar mensaje conciso
    logger.info("✏️ Generando mensaje Telegram...")
    mensaje = generar_mensaje_telegram(boletin)

    # Generar HTML completo
    logger.info("📄 Generando HTML...")
    fecha_str = datetime.now().strftime("%Y%m%d")
    html = generar_html(boletin)
    filename = f"boletin_ia_{fecha_str}.html"

    # Enviar a Telegram
    logger.info("📤 Enviando a Telegram...")
    enviar_telegram_mensaje(mensaje)
    enviar_telegram_documento(html, filename)

    logger.info("✅ Boletín completado exitosamente")


if __name__ == "__main__":
    main()
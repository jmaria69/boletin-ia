# 📰 Boletín Diario de IA

Boletín automático de noticias sobre inteligencia artificial, organizado en 3 niveles (Global, España, Madrid) y enviado a Telegram a través de GitHub Actions.

## ✨ Características

- ✅ **Ejecución automática en la nube** - 2x al día (9:00 AM y 22:00 PM)
- ✅ **Sin dependencias locales** - Todo corre en GitHub Actions
- ✅ **Noticias actualizadas** - Búsqueda en tiempo real con WebSearch
- ✅ **3 niveles de organización** - Global, España, Madrid
- ✅ **Envío a Telegram** - Mensaje conciso + HTML completo
- ✅ **Almacenamiento en nube** - Archivos HTML guardados automáticamente

## 🚀 Configuración Rápida

### 1. Crear repositorio en GitHub

```bash
# Clone este repositorio o crea uno nuevo
git clone https://github.com/TU_USUARIO/boletin-ia-github.git
cd boletin-ia-github
```

### 2. Configurar secretos en GitHub

Ve a: **Settings → Secrets and variables → Actions → New repository secret**

Añade estos secretos:

| Secreto | Valor |
|---------|-------|
| `TELEGRAM_TOKEN` | `8678147787:AAEAHxSrm4WOcQRE8zY4JiWwWEcAat_NH5g` |
| `TELEGRAM_CHAT_ID` | `867107949` |

### 3. Push al repositorio

```bash
git add .
git commit -m "Initial commit: Boletín IA automático"
git push origin main
```

### 4. ¡Listo!

GitHub Actions ejecutará automáticamente:
- **9:00 AM** - Boletín matutino
- **22:00 PM** - Boletín nocturno

Los archivos HTML se guardan en la rama `outputs/`.

---

## 📁 Estructura del Proyecto

```
boletin-ia-github/
├── boletin_ia_telegram_pro.py    # Script principal
├── .github/
│   └── workflows/
│       └── boletin.yml           # Configuración de GitHub Actions
├── README.md                     # Este archivo
└── requirements.txt              # Dependencias Python
```

---

## 🔧 Personalización

### Cambiar horarios

Edita `.github/workflows/boletin.yml`:

```yaml
- cron: '0 9,22 * * *'  # Cambiar horarios aquí
```

Formato cron: `minuto hora día mes día_semana`

### Cambiar noticias

Edita `boletin_ia_telegram_pro.py`:
- Línea 195: Modificar búsquedas de WebSearch
- Línea 250: Cambiar formato del mensaje

---

## 📊 Logs de ejecución

Ver ejecuciones en: **Actions → Boletín IA Diario**

Cada ejecución muestra:
- ✅ Mensajes enviados
- 📄 Archivos generados
- ⏱️ Tiempo de ejecución

---

## 🛠️ Troubleshooting

**¿No se ejecuta el workflow?**
- Verifica que los secretos estén configurados correctamente
- Comprueba que la rama sea `main`

**¿Error en Telegram?**
- Verifica el TELEGRAM_TOKEN
- Comprueba el TELEGRAM_CHAT_ID

---

## 📄 Licencia

MIT - Libre para usar y modificar

---

**Creado con ❤️ por roco26_bot**

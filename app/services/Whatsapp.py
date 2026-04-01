"""
Servicio de envío de tickets por WhatsApp usando CallMeBot (gratuito).

ACTIVACIÓN — el cliente debe hacerlo UNA SOLA VEZ:
  1. Agregar el número +34 644 44 44 16 a sus contactos de WhatsApp
  2. Enviarle el mensaje exacto: "I allow callmebot to send me messages"
  3. Recibirá su apikey personal por WhatsApp

Configura en .env:
    CALLMEBOT_APIKEY=123456    ← la apikey que el cliente recibe
"""
import httpx
from urllib.parse import quote
from app.core.config import settings
from fastapi import HTTPException


def _construir_mensaje(venta_id: int, total: float, detalles: list[dict]) -> str:
    lineas = [f"🧾 *Ticket de compra — Folio #{venta_id}*\n"]
    for d in detalles:
        lineas.append(f"• {d['producto']} x{d['cantidad']} — ${d['subtotal']:.2f}")
    lineas.append(f"\n*Total: ${total:.2f}*")
    lineas.append("\n_Gracias por su compra_ 🙌")
    return "\n".join(lineas)


def enviar_ticket_whatsapp(
    numero: str,
    venta_id: int,
    total: float,
    detalles: list[dict],
) -> None:
    """
    Envía el ticket por WhatsApp vía CallMeBot.
    `numero` debe incluir código de país sin '+', ej: '529511234567'
    """
    # CallMeBot espera el número sin '+' ni espacios
    numero_limpio = numero.replace("+", "").replace(" ", "").replace("-", "")

    mensaje = _construir_mensaje(venta_id, total, detalles)
    mensaje_encoded = quote(mensaje)

    url = (
        f"https://api.callmebot.com/whatsapp.php"
        f"?phone={numero_limpio}"
        f"&text={mensaje_encoded}"
        f"&apikey={settings.CALLMEBOT_APIKEY}"
    )

    response = httpx.get(url, timeout=10)

    if response.status_code != 200 or "Message queued" not in response.text:
        raise HTTPException(
            502,
            f"CallMeBot no pudo enviar el mensaje. Respuesta: {response.text}"
        )
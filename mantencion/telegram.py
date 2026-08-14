import os
import requests


def enviar_mensaje_telegram(chat_id, mensaje):

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise Exception("No está configurado TELEGRAM_BOT_TOKEN")

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    datos = {
        "chat_id": chat_id,
        "text": mensaje
    }

    respuesta = requests.post(
        url,
        data=datos,
        timeout=10
    )

    respuesta.raise_for_status()

    return respuesta.json()
from django.core.management.base import BaseCommand
from django.utils import timezone

from mantencion.models import (
    Mantencion,
    TelegramDestinatario,
    TelegramAvisoAceite,
)

from mantencion.telegram import enviar_mensaje_telegram


class Command(BaseCommand):

    help = "Revisa los cambios de aceite y envía alertas por Telegram"

    def handle(self, *args, **kwargs):

        mantenciones = Mantencion.objects.select_related("vehiculo").all()

        destinatarios = TelegramDestinatario.objects.filter(
            activo=True
        )

        for p in mantenciones:

            if (
                p.kilometraje is None
                or p.kilometraje_cambio_aceite is None
            ):
                continue

            faltan = p.kilometraje_cambio_aceite - p.kilometraje

            # Determinar el tipo de aviso
            if faltan <= 0:
                tipo_aviso = "VENCIDO"
                texto_aviso = "🚨 CAMBIO DE ACEITE VENCIDO"

            elif faltan <= 300:
                tipo_aviso = "300"
                texto_aviso = "🔔 CAMBIO DE ACEITE PRÓXIMO - 300 KM"

            elif faltan <= 500:
                tipo_aviso = "500"
                texto_aviso = "🔔 CAMBIO DE ACEITE PRÓXIMO - 500 KM"

            elif faltan <= 1000:
                tipo_aviso = "1000"
                texto_aviso = "🔔 CAMBIO DE ACEITE PRÓXIMO - 1000 KM"

            else:
                continue

            # Comprobar si este aviso ya fue enviado
            aviso_existente = TelegramAvisoAceite.objects.filter(
                vehiculo=p.vehiculo,
                tipo_aviso=tipo_aviso
            ).exists()

            if aviso_existente:
                continue

            mensaje = (
                f"{texto_aviso}\n\n"
                f"Vehículo: {p.vehiculo.patente}\n"
                f"Kilometraje actual: {p.kilometraje:,} km\n"
                f"Kilometraje cambio de aceite: "
                f"{p.kilometraje_cambio_aceite:,} km\n"
                f"Kilómetros restantes: {max(faltan, 0):,} km"
            )

            # Enviar a todos los destinatarios activos
            envio_exitoso = True

            for destinatario in destinatarios:

                try:

                    enviar_mensaje_telegram(
                        destinatario.chat_id,
                        mensaje
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Telegram enviado a "
                            f"{destinatario.nombre} - "
                            f"{p.vehiculo.patente} - "
                            f"{tipo_aviso}"
                        )
                    )

                except Exception as e:

                    envio_exitoso = False

                    self.stdout.write(
                        self.style.ERROR(
                            f"Error enviando Telegram a "
                            f"{destinatario.nombre}: {e}"
                        )
                    )

            # Registrar el aviso solamente si todos los envíos fueron exitosos
            if envio_exitoso:

                TelegramAvisoAceite.objects.create(
                    vehiculo=p.vehiculo,
                    tipo_aviso=tipo_aviso
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Aviso registrado: "
                        f"{p.vehiculo.patente} - {tipo_aviso}"
                    )
                )
import asyncio
import threading

from application.daemons.email import EmailDaemon
from application.daemons.sms import SMSDaemon
from application.daemons.whatsapp import WhatsappDaemon
from application.database.models.message import MessageType
from application.external_sources.email.client import EmailClient
from application.external_sources.smsc.client import SMSCClient
from application.external_sources.wapico.client import WapicoClient


async def main():
    threading.Thread(
        target=asyncio.run,
        args=(
            EmailDaemon(
                email_client=EmailClient(), message_type=MessageType.immediate
            ).run(),
        ),
        daemon=True,
    ).start()
    threading.Thread(
        target=asyncio.run,
        args=(
            EmailDaemon(
                email_client=EmailClient(), message_type=MessageType.newsletter
            ).run(),
        ),
        daemon=True,
    ).start()

    threading.Thread(
        target=asyncio.run,
        args=(WhatsappDaemon(whatsapp_client=WapicoClient()).run(),),
        daemon=True,
    ).start()

    threading.Thread(
        target=asyncio.run,
        args=(SMSDaemon(smsc_client=SMSCClient()).run(),),
        daemon=True,
    ).start()

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

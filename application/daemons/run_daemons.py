import asyncio

from application.daemons.email import EmailDaemon
from application.daemons.sms import SMSDaemon
from application.daemons.whatsapp import WhatsappDaemon
from application.database.models.message import MessageType
from application.external_sources.email.client import EmailClient
from application.external_sources.smsc.client import SMSCClient
from application.external_sources.wapico.client import WapicoClient


async def main():
    tasks = (  # noqa
        asyncio.create_task(
            EmailDaemon(
                email_client=EmailClient(), message_type=MessageType.immediate
            ).run()
        ),
        asyncio.create_task(
            EmailDaemon(
                email_client=EmailClient(), message_type=MessageType.newsletter
            ).run()
        ),
        asyncio.create_task(
            WhatsappDaemon(whatsapp_client=WapicoClient()).run()
        ),
        asyncio.create_task(SMSDaemon(smsc_client=SMSCClient()).run()),
    )
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

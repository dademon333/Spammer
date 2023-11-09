import asyncio
import threading

from application.daemons.email import EmailDaemon
from application.database.models.message import MessageType
from application.external_sources.email.client import EmailClient


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

    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())

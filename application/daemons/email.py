import asyncio
import logging

from application.database.models.message import (
    MessageType,
    MessagePlatform,
    MessageStatus,
    Message,
)
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.di.repositories import get_message_repository
from application.external_sources.email.client import EmailClient
from application.utils.di import DependencyInjector

logger = logging.getLogger(__name__)


class EmailDaemon:
    def __init__(self, email_client: EmailClient, message_type: MessageType):
        self.email_client = email_client
        self.message_type = message_type

    async def run(self):
        while True:
            try:
                messages = await self.get_messages()
                if not messages:
                    await asyncio.sleep(5)
                    continue

                await self.process_messages(messages)
            except Exception:
                logger.exception(
                    "Произошла ошибка при рассылке сообщений на почту"
                )
                await self.on_process_error(messages)

    async def get_messages(self) -> list[Message]:
        async with DependencyInjector() as injector:
            message_repository: MessageRepository = await injector.solve(
                get_message_repository
            )
            return await message_repository.take_to_work(
                message_type=self.message_type,
                platform=MessagePlatform.email,
                count=100,
            )

    async def process_messages(self, messages: list[Message]) -> None:
        await asyncio.gather(
            *[
                self.email_client.send_message(
                    to=message.address,
                    subject=message.subject,
                    message=message.text,
                )
                for message in messages
            ]
        )
        async with DependencyInjector() as injector:
            message_repository: MessageRepository = await injector.solve(
                get_message_repository
            )
            await message_repository.update_statuses(
                message_ids=[x.id for x in messages], status=MessageStatus.done
            )

    async def on_process_error(self, messages: list[Message]) -> None:
        async with DependencyInjector() as injector:
            message_repository: MessageRepository = await injector.solve(
                get_message_repository
            )
            await message_repository.update_statuses(
                message_ids=[x.id for x in messages],
                status=MessageStatus.failed,
            )

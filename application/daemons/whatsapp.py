import asyncio
import logging

from application.database.models.message import (
    Message,
    MessageType,
    MessagePlatform,
    MessageStatus,
)
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.di.repositories import get_message_repository
from application.external_sources.wapico.client import WapicoClient
from application.utils.di import DependencyInjector

logger = logging.getLogger(__name__)


class WhatsappDaemon:
    def __init__(self, whatsapp_client: WapicoClient):
        self.whatsapp_client = whatsapp_client

    async def run(self):
        while True:
            try:
                messages = await self.get_messages()
                if not messages:
                    await asyncio.sleep(5)
                    continue

                await self.process_messages(messages)
                logger.info(
                    f"Отправлено {len(messages)} сообщений на whatsapp"
                )
            except Exception:
                logger.exception(
                    "Произошла ошибка при рассылке сообщений на whatsapp"
                )

    @staticmethod
    async def get_messages() -> list[Message]:
        async with DependencyInjector() as injector:
            message_repository: MessageRepository = await injector.solve(
                get_message_repository
            )
            return await message_repository.take_to_work(
                message_type=MessageType.immediate,
                platform=MessagePlatform.whatsapp,
                count=3,
            )

    async def process_messages(self, messages: list[Message]) -> None:
        async with DependencyInjector() as injector:
            message_repository: MessageRepository = await injector.solve(
                get_message_repository
            )
            for message in messages:
                try:
                    await self.whatsapp_client.send_message(
                        phone_number=message.address,
                        message=message.text,
                        instance_id=message.access_token,
                    )
                    await message_repository.update_status(
                        message_id=message.id, new_status=MessageStatus.done
                    )
                    logger.info(
                        f"Отправлено сообщение на whatsapp {message.address}"
                    )
                    await asyncio.sleep(1)
                except Exception:
                    logger.exception(
                        f"Произошла ошибка при отправке сообщения"
                        f" на whatsapp {message.address}"
                    )
                    await message_repository.update_status(
                        message_id=message.id, new_status=MessageStatus.failed
                    )
                    await asyncio.sleep(3)

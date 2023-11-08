import logging

from application.database.models.message import Message, MessageType
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.use_cases.messages.dto import CreateNewsletterInputDTO

logger = logging.getLogger(__name__)


class CreateNewsletterUseCase:
    def __init__(
        self,
        message_repository: MessageRepository,
    ):
        self.message_repository = message_repository

    async def execute(
        self,
        input_dto: CreateNewsletterInputDTO,
    ) -> None:
        logger.info(
            (
                f"Создание новостной рассылки"
                f" на {len(input_dto.messages)} сообщений"
                f" вида {input_dto.platform}"
            )
        )

        messages = [
            Message(
                text=message.text,
                address=message.address,
                subject=message.subject,
                type=MessageType.newsletter,
                platform=input_dto.platform,
                access_token=message.access_token,
            )
            for message in input_dto.messages
        ]
        await self.message_repository.bulk_create(messages)
        logger.info("Сообщения загружены в бд")

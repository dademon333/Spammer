import logging

from application.database.models.message import Message
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.use_cases.messages.dto import (
    CreateMessageInputDTO,
    CreateMessageOutputDTO,
)

logger = logging.getLogger(__name__)


class CreateMessageUseCase:
    def __init__(
        self,
        message_repository: MessageRepository,
    ):
        self.message_repository = message_repository

    async def execute(
        self, input_dto: CreateMessageInputDTO
    ) -> CreateMessageOutputDTO:
        logger.info(
            (
                f"Создание сообщения"
                f" для {input_dto.address}"
                f" на {input_dto.platform}"
                f" типа {input_dto.type}"
            )
        )

        message = await self.message_repository.create(
            Message.parse_obj(input_dto)
        )
        logger.info(f"Создали сообщение с id {message.id}")
        return CreateMessageOutputDTO(id=message.id)

from datetime import datetime
from textwrap import dedent

from pydantic import BaseModel, Field, root_validator

from application.database.models.message import MessageType, MessagePlatform
from application.utils.formatters import normalize_phone


class CreateMessageInputDTO(BaseModel):
    text: str = Field(..., description="Текст сообщения")
    address: str = Field(
        ...,
        description=(
            "Куда отправить сообщение: email адрес/номера телефона/etc"
        ),
    )
    type: MessageType = Field(
        ...,
        description=dedent(
            """
                Тип сообщения:
                - immediate - Отправить сразу
                - newsletter - Массовая рассылка
                - scheduled - Отложенное сообщение
            """
        ),
    )
    platform: MessagePlatform = Field(
        ..., description="Куда отправить сообщение"
    )
    scheduled_at: datetime | None = Field(
        None,
        description="Только для отложенных сообщений. Когда нужно отправить",
    )

    @root_validator
    def check_address(cls, values) -> str:
        platforms_with_phone = [
            MessagePlatform.sms,
            MessagePlatform.whatsapp,
        ]
        if values["platform"] in platforms_with_phone:
            address = normalize_phone(values["address"])
            if len(address) != 11:
                raise ValueError("Неверный формат телефона")
            values["address"] = address
        return values

    @root_validator
    def check_scheduled_at(cls, values):
        # scheduled_at можно указывать только для отложенных сообщений
        # У остальных будет None
        if values["scheduled_at"] and values["type"] != MessageType.scheduled:
            raise ValueError("scheduled_at только для отложенных сообщений")
        return values


class CreateMessageOutputDTO(BaseModel):
    id: int = Field(..., description="ID созданного сообщения")


class CreateNewsletterMessageInputDTO(BaseModel):
    text: str = Field(..., description="Текст сообщения")
    address: str = Field(
        ...,
        description=(
            "Куда отправить сообщение: email адрес/номера телефона/etc"
        ),
    )


class CreateNewsletterInputDTO(BaseModel):
    messages: list[CreateNewsletterMessageInputDTO] = Field(
        ..., description="Список сообщений с адресатами"
    )
    platform: MessagePlatform = Field(
        ..., description="Куда отправить сообщение"
    )
    scheduled_at: datetime | None = Field(
        None,
        description="Если нужна отложенная рассылка. Когда нужно отправить",
    )

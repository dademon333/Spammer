from textwrap import dedent

from pydantic import BaseModel, Field

from application.database.models.message import MessageType, MessagePlatform


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
            """
        ),
    )
    platform: MessagePlatform = Field(
        ..., description="Куда отправить сообщение"
    )
    access_token: str | None = Field(
        None, description="Токен для отправки сообщения (если требуется)"
    )


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
    access_token: str | None = Field(
        None, description="Токен для отправки сообщения (если требуется)"
    )


class CreateNewsletterInputDTO(BaseModel):
    messages: list[CreateNewsletterMessageInputDTO] = Field(
        ..., description="Список сообщений с адресатами"
    )
    platform: MessagePlatform = Field(
        ..., description="Куда отправить сообщение"
    )

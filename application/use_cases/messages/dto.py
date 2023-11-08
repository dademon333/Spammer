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
    subject: str | None = Field(None, description="Тема сообщения (для email)")
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
        None,
        description=(
            "Токен клиента Firebase/Instance ID Wapico для отправки сообщения"
        ),
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
    subject: str | None = Field(None, description="Тема сообщения (для email)")
    access_token: str | None = Field(
        None,
        description=(
            "Токен клиента Firebase/Instance ID Wapico для отправки сообщения"
        ),
    )


class CreateNewsletterInputDTO(BaseModel):
    messages: list[CreateNewsletterMessageInputDTO] = Field(
        ..., description="Список сообщений с адресатами"
    )
    platform: MessagePlatform = Field(
        ..., description="Куда отправить сообщение"
    )

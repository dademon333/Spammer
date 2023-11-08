from datetime import datetime
from enum import StrEnum

from pydantic import Field

from application.database.models.base import ModelBase, UpdateModelBase


class MessageType(StrEnum):
    immediate = "immediate"  # Отправлять сразу
    newsletter = "newsletter"  # Массовая рассылка


class MessagePlatform(StrEnum):
    notification = "notification"
    email = "email"
    sms = "sms"
    whatsapp = "whatsapp"


class MessageStatus(StrEnum):
    new = "new"
    in_work = "in_work"
    done = "done"
    failed = "failed"


class Message(ModelBase):
    text: str
    address: str
    subject: str | None  # Тема сообщения (для email)
    status: MessageStatus = MessageStatus.new
    type: MessageType
    platform: MessagePlatform
    access_token: str | None  # Токен для отправки оповещения (если нужен)
    created_at: datetime = Field(  # Когда создали сообщение
        default_factory=lambda: datetime.utcnow()
    )
    taken_to_work_at: datetime | None  # Когда сообщение взято в работу


class UpdateMessage(UpdateModelBase):
    text: str | None
    address: str | None
    subject: str | None
    status: MessageStatus | None
    type: MessageType | None
    platform: MessagePlatform | None
    access_token: str | None
    taken_to_work_at: datetime | None

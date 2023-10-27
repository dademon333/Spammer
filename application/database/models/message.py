from datetime import datetime
from enum import StrEnum

from pydantic import Field

from application.database.models.base import ModelBase, UpdateModelBase


class MessageType(StrEnum):
    immediate = "immediate"  # Отправлять сразу
    newsletter = "newsletter"  # Массовая рассылка
    scheduled = "scheduled"  # Отложенное сообщение


class MessagePlatform(StrEnum):
    ios_notification = "ios_notification"
    android_notification = "android_notification"
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
    status: MessageStatus = MessageStatus.new
    type: MessageType
    platform: MessagePlatform
    scheduled_at: datetime | None  # Во сколько нужно отправить сообщение
    created_at: datetime = Field(  # Когда создали сообщение
        default_factory=lambda: datetime.utcnow()
    )
    taken_to_work_at: datetime | None  # Когда сообщение взято в работу


class UpdateMessage(UpdateModelBase):
    text: str | None
    address: str | None
    status: MessageStatus | None
    type: MessageType | None
    platform: MessagePlatform | None
    scheduled_at: datetime | None
    taken_to_work_at: datetime | None

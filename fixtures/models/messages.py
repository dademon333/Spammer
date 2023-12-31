import pytest

from application.database.models.message import (
    Message,
    MessageType,
    MessagePlatform,
)
from application.database.repositories.message_repository import (
    MessageRepository,
)


@pytest.fixture()
async def email_message_list() -> list[Message]:
    return [
        Message(
            text="Hello, dear",
            address="client@mail.ru",
            subject="Test message",
            type=MessageType.immediate,
            platform=MessagePlatform.email,
        ),
        Message(
            text="Reminder: Meeting at 2 PM",
            address="artyom@mail.ru",
            subject="Reminder",
            type=MessageType.immediate,
            platform=MessagePlatform.email,
        ),
    ]


@pytest.fixture()
async def email_mixed_message_list() -> list[Message]:
    return [
        Message(
            text="Hello, dear",
            address="client@mail.ru",
            subject="Test message",
            type=MessageType.immediate,
            platform=MessagePlatform.email,
        ),
        Message(
            text="Reminder: Meeting at 2 PM",
            address="artyom@mail.ru",
            subject="Reminder",
            type=MessageType.immediate,
            platform=MessagePlatform.email,
        ),
        Message(
            text="Join our community",
            address="barsuk@mail.ru",
            subject="Very important message",
            type=MessageType.newsletter,
            platform=MessagePlatform.email,
        ),
        Message(
            text="Congratulations on your promotion",
            address="jane@example.com",
            subject="Good News",
            type=MessageType.newsletter,
            platform=MessagePlatform.email,
        ),
    ]


@pytest.fixture()
async def email_message_list_in_db(
    email_message_list: list[Message], message_repository: MessageRepository
) -> list[Message]:
    await message_repository.bulk_create(email_message_list)
    return email_message_list


@pytest.fixture()
async def email_mixed_message_list_in_db(
    email_mixed_message_list: list[Message],
    message_repository: MessageRepository,
) -> list[Message]:
    await message_repository.bulk_create(email_mixed_message_list)
    return email_mixed_message_list


@pytest.fixture()
async def whatsapp_message_list() -> list[Message]:
    return [
        Message(
            text="Hello, dear",
            address="+79061001122",
            type=MessageType.immediate,
            platform=MessagePlatform.whatsapp,
            access_token="642D8BD6EEA12",  # test wapico instance id
        ),
        Message(
            text="Reminder: Meeting at 2 PM",
            address="+79061001123",
            type=MessageType.immediate,
            platform=MessagePlatform.whatsapp,
            access_token="642D8BD6EEA12",  # test wapico instance id
        ),
    ]


@pytest.fixture()
async def whatsapp_message_list_in_db(
    whatsapp_message_list: list[Message], message_repository: MessageRepository
) -> list[Message]:
    await message_repository.bulk_create(whatsapp_message_list)
    return whatsapp_message_list


@pytest.fixture()
async def sms_message_list() -> list[Message]:
    return [
        Message(
            text="Hello, dear",
            address="+79061001122",
            type=MessageType.immediate,
            platform=MessagePlatform.sms,
        ),
        Message(
            text="Reminder: Meeting at 2 PM",
            address="+79061001123",
            type=MessageType.immediate,
            platform=MessagePlatform.sms,
        ),
    ]


@pytest.fixture()
async def sms_message_list_in_db(
    sms_message_list: list[Message], message_repository: MessageRepository
) -> list[Message]:
    await message_repository.bulk_create(sms_message_list)
    return sms_message_list

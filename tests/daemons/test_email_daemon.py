from unittest.mock import Mock, AsyncMock

import pytest

from application.daemons.email import EmailDaemon
from application.database.models.message import (
    MessageType,
    Message,
    MessageStatus,
)
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.external_sources.email.client import EmailClient


@pytest.fixture()
def daemon() -> EmailDaemon:
    return EmailDaemon(
        email_client=Mock(spec=EmailClient), message_type=MessageType.immediate
    )


async def test_get_messages(
    email_mixed_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: EmailDaemon,
):
    messages = await daemon.get_messages()

    immediate_messages = [
        x
        for x in email_mixed_message_list_in_db
        if x.type == MessageType.immediate
    ]
    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in immediate_messages]
    )

    assert set(x.text for x in messages) == set(
        x.text for x in immediate_messages
    )
    assert all(x.status == MessageStatus.in_work for x in messages_in_db)


async def test_process_messages(
    email_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: EmailDaemon,
):
    daemon.email_client.send_message = AsyncMock()

    await daemon.process_messages(email_message_list_in_db)

    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in email_message_list_in_db]
    )

    daemon.email_client.send_message.assert_awaited()
    assert all(x.status == MessageStatus.done for x in messages_in_db)


async def test_on_process_error(
    email_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: EmailDaemon,
):
    await daemon.on_process_error(email_message_list_in_db)

    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in email_message_list_in_db]
    )
    assert all(x.status == MessageStatus.failed for x in messages_in_db)

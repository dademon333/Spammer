from unittest.mock import Mock, AsyncMock

import pytest
from pytest_mock import MockerFixture

from application.daemons.sms import SMSDaemon
from application.database.models.message import Message, MessageStatus
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.external_sources.smsc.client import SMSCClient


@pytest.fixture()
def daemon() -> SMSDaemon:
    return SMSDaemon(smsc_client=Mock(spec=SMSCClient))


async def test_get_messages(
    sms_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: SMSDaemon,
):
    messages = await daemon.get_messages()

    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in sms_message_list_in_db]
    )

    assert set(x.text for x in messages) == set(
        x.text for x in sms_message_list_in_db
    )
    assert all(x.status == MessageStatus.in_work for x in messages_in_db)


async def test_process_messages_success(
    sms_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: SMSDaemon,
    mocker: MockerFixture,
):
    mock = mocker.patch("asyncio.sleep")

    await daemon.process_messages(sms_message_list_in_db)

    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in sms_message_list_in_db]
    )

    mock.assert_awaited_with(1)
    assert all(x.status == MessageStatus.done for x in messages_in_db)


async def test_process_messages_error(
    sms_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: SMSDaemon,
    mocker: MockerFixture,
):
    mock = mocker.patch("asyncio.sleep")
    daemon.smsc_client.send_message = AsyncMock(side_effect=Exception("test"))

    await daemon.process_messages(sms_message_list_in_db)

    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in sms_message_list_in_db]
    )

    mock.assert_awaited_with(3)
    assert all(x.status == MessageStatus.failed for x in messages_in_db)

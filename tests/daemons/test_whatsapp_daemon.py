from unittest.mock import Mock, AsyncMock

import pytest
from pytest_mock import MockerFixture

from application.daemons.whatsapp import WhatsappDaemon
from application.database.models.message import Message, MessageStatus
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.external_sources.wapico.client import WapicoClient


@pytest.fixture()
def daemon() -> WhatsappDaemon:
    return WhatsappDaemon(whatsapp_client=Mock(spec=WapicoClient))


async def test_get_messages(
    whatsapp_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: WhatsappDaemon,
):
    messages = await daemon.get_messages()

    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in whatsapp_message_list_in_db]
    )

    assert set(x.text for x in messages) == set(
        x.text for x in whatsapp_message_list_in_db
    )
    assert all(x.status == MessageStatus.in_work for x in messages_in_db)


async def test_process_messages_success(
    whatsapp_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: WhatsappDaemon,
    mocker: MockerFixture,
):
    mock = mocker.patch("asyncio.sleep")

    await daemon.process_messages(whatsapp_message_list_in_db)

    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in whatsapp_message_list_in_db]
    )

    mock.assert_awaited_with(1)
    assert all(x.status == MessageStatus.done for x in messages_in_db)


async def test_process_messages_error(
    whatsapp_message_list_in_db: list[Message],
    message_repository: MessageRepository,
    daemon: WhatsappDaemon,
    mocker: MockerFixture,
):
    mock = mocker.patch("asyncio.sleep")
    daemon.whatsapp_client.send_message = AsyncMock(
        side_effect=Exception("test")
    )

    await daemon.process_messages(whatsapp_message_list_in_db)

    messages_in_db = await message_repository.get_by_ids(
        [x.id for x in whatsapp_message_list_in_db]
    )

    mock.assert_awaited_with(3)
    assert all(x.status == MessageStatus.failed for x in messages_in_db)

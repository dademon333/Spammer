import pytest
from httpx import AsyncClient

from application.database.models.message import (
    MessageType,
    MessagePlatform,
    MessageStatus,
    Message,
)
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.use_cases.messages.dto import CreateMessageInputDTO


@pytest.fixture()
def input_dto() -> CreateMessageInputDTO:
    return CreateMessageInputDTO(
        text="hello, dear",
        address="+79061001122",
        type=MessageType.immediate,
        platform=MessagePlatform.whatsapp,
    )


async def test_success(
    auth_token: str,
    input_dto: CreateMessageInputDTO,
    message_repository: MessageRepository,
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/api/v1/messages",
        json=input_dto.dict(),
        headers={"authorization": auth_token},
    )
    result = response.json()

    message = await message_repository.get_by_id(result["id"])

    assert response.status_code == 200
    assert message == Message(
        id=message.id,
        text=input_dto.text,
        address="+79061001122",
        status=MessageStatus.new,
        type=MessageType.immediate,
        platform=MessagePlatform.whatsapp,
        created_at=message.created_at,
        taken_to_work_at=None,
    )


async def test_unauthorized(
    input_dto: CreateMessageInputDTO,
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/api/v1/messages",
        json=input_dto.dict(),
    )
    result = response.json()

    assert response.status_code == 401
    assert result["detail"] == "Unauthorized"

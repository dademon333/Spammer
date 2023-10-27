from httpx import AsyncClient

from application.database.models.message import MessagePlatform
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.use_cases.messages.dto import (
    CreateNewsletterInputDTO,
    CreateNewsletterMessageInputDTO,
)
from application.web.views.common_responses import OkResponse


async def test_success(
    auth_token: str,
    message_repository: MessageRepository,
    async_client: AsyncClient,
):
    input_dto = CreateNewsletterInputDTO(
        messages=[
            CreateNewsletterMessageInputDTO(
                text="hello, dear", address="foo@mail.ru"
            ),
            CreateNewsletterMessageInputDTO(
                text="join out community", address="bar@mail.ru"
            ),
        ],
        platform=MessagePlatform.email,
    )
    response = await async_client.post(
        "/api/v1/messages/newsletter",
        json=input_dto.dict(),
        headers={"authorization": auth_token},
    )
    result = response.json()

    messages_in_db = await message_repository.get_by_ids([1, 2, 3, 4, 5])

    assert response.status_code == 200
    assert result == OkResponse()

    assert len(messages_in_db) == 2
    assert all(x.platform == MessagePlatform.email for x in messages_in_db)
    assert all(x.scheduled_at is None for x in messages_in_db)
    assert set(x.address for x in messages_in_db) == {
        "foo@mail.ru",
        "bar@mail.ru",
    }
    assert set(x.text for x in messages_in_db) == {
        "hello, dear",
        "join out community",
    }

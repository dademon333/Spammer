from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.database.models.message import MessagePlatform
from application.database.orm_models import MessageORM
from application.use_cases.messages.dto import (
    CreateNewsletterInputDTO,
    CreateNewsletterMessageInputDTO,
)
from application.web.views.common_responses import OkResponse


async def test_success(
    auth_token: str,
    db_session: AsyncSession,
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

    messages_in_db = (await db_session.scalars(select(MessageORM))).all()

    assert response.status_code == 200
    assert result == OkResponse()

    assert len(messages_in_db) == 2
    assert all(x.platform == MessagePlatform.email for x in messages_in_db)
    assert set(x.address for x in messages_in_db) == {
        "foo@mail.ru",
        "bar@mail.ru",
    }
    assert set(x.text for x in messages_in_db) == {
        "hello, dear",
        "join out community",
    }

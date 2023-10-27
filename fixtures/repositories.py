import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.database.repositories.service_token_repository import (
    ServiceTokenRepository,
)


@pytest.fixture()
def service_token_repository(
    db_session: AsyncSession,
) -> ServiceTokenRepository:
    return ServiceTokenRepository(db_session=db_session)


@pytest.fixture()
def message_repository(
    db_session: AsyncSession,
) -> MessageRepository:
    return MessageRepository(db_session=db_session)

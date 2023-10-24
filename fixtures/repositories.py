import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from application.database.repositories.service_token_repository import (
    ServiceTokenRepository,
)


@pytest.fixture()
def service_token_repository(
    db_session: AsyncSession,
) -> ServiceTokenRepository:
    return ServiceTokenRepository(db_session=db_session)

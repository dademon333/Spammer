from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.database.connection import async_session
from application.database.repositories.message_repository import (
    MessageRepository,
)
from application.database.repositories.service_token_repository import (
    ServiceTokenRepository,
)


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session.begin() as session:
        yield session


def get_service_token_repository(db=Depends(get_db)) -> ServiceTokenRepository:
    return ServiceTokenRepository(db_session=db)


def get_message_repository(db=Depends(get_db)) -> MessageRepository:
    return MessageRepository(db_session=db)

import logging

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)

from application.config import POSTGRESQL_URL

logger = logging.getLogger(__name__)


def create_connection(connection_url: str) -> AsyncEngine:
    from uuid import uuid4
    from asyncpg import Connection

    class CConnection(Connection):
        def _get_unique_id(self, prefix: str) -> str:
            return f"__asyncpg_{prefix}_{uuid4()}__"

    return create_async_engine(
        connection_url,
        echo=False,
        connect_args={
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
            "connection_class": CConnection,
        },
    )


async_engine = create_connection(POSTGRESQL_URL)
async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

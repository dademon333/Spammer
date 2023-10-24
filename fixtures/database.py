from typing import AsyncGenerator, Generator

import alembic.command
import asyncpg
import pytest
from alembic.config import Config
from asyncpg import Connection
from sqlalchemy import ForeignKeyConstraint, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from application.database.connection import async_engine, async_session
from application.database.orm_models import Base
from config import (
    POSTGRESQL_DATABASE,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_HOST,
    POSTGRESQL_USER,
    POSTGRESQL_PORT,
)


@pytest.fixture(scope="session")
def db_name() -> str:
    return POSTGRESQL_DATABASE


async def kill_database_connections(cursor: Connection, db_name: str) -> None:
    """Убивает все подключения к бд.

    Используется перед каждым drop database (иначе выбросит ошибку).
    """
    await cursor.execute(
        f"""
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname='{db_name}'
    """
    )


@pytest.fixture(scope="session")
async def engine(db_name: str) -> AsyncGenerator[AsyncEngine, None]:
    cursor = await asyncpg.connect(
        password=POSTGRESQL_PASSWORD,
        host=POSTGRESQL_HOST,
        user=POSTGRESQL_USER,
        port=POSTGRESQL_PORT,
    )

    db_user = POSTGRESQL_USER
    try:
        # Пытаемся создать тестовую базу
        await cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user}")
    except Exception:
        # База с таким именем существует.
        # Сбрасываем все коннекты и создаём новую
        await kill_database_connections(cursor, db_name)
        await cursor.execute(f"DROP DATABASE {db_name}")
        await cursor.execute(f"CREATE DATABASE {db_name} OWNER {db_user}")

    # Отдаем движок в приложение
    yield async_engine

    # Удаляем тестовую базу
    await kill_database_connections(cursor, db_name)
    await cursor.execute(f"DROP DATABASE {db_name}")
    await cursor.close()


def get_dependencies_map() -> dict[str, list[str]]:
    dependencies: dict[str, list[str]] = {
        table: [] for table in Base.metadata.tables.keys()
    }

    for table_name, table in Base.metadata.tables.items():
        for constraint in table.constraints:
            if isinstance(constraint, ForeignKeyConstraint):
                dependencies[str(constraint.referred_table)].append(table_name)

    return dependencies


def get_cleaning_order(dependencies_map: dict[str, list[str]]) -> list[str]:
    cleaning_order = []
    checked_tables = {table: 0 for table in dependencies_map}

    def dfs(table):
        if checked_tables[table] == 1:
            return

        checked_tables[table] = 1

        # Рекурсивно обходим все зависимые таблицы
        for dependent_table in dependencies_map[table]:
            dfs(dependent_table)

        # Добавляем текущую таблицу в конец списка очистки
        cleaning_order.append(table)

    for table in dependencies_map:
        dfs(table)

    return cleaning_order


async def truncate_db():
    """
    Чистка таблиц после каждого теста. Самый быстрый способ очистить бд
    - пройтись по всем таблицам DELETE.
    Но если на строку  в родительской таблице есть foreign keys из других,
    postgres не даст её удалить.
    Поэтому мы собираем граф зависимостей - {таблица: [зависимые_от_неё]},
    затем алгоритмом топологической сортировки определяем порядок чистки:
    сначала зависимые таблицы, потом родительская.
    POWERED BY ChatGPT
    """
    dependencies_map = get_dependencies_map()
    cleaning_order = get_cleaning_order(dependencies_map)

    async with async_engine.connect() as conn:
        for table_name in cleaning_order:
            await conn.execute(text(f"DELETE FROM {table_name}"))

        await conn.commit()


@pytest.fixture(scope="session")
def migration(engine: AsyncEngine) -> Generator[None, None, None]:
    alembic_config = Config("alembic.ini")
    alembic.command.upgrade(alembic_config, "head")
    yield
    alembic.command.downgrade(alembic_config, "base")


@pytest.fixture()
async def db_session(migration) -> AsyncSession:
    """Асинхронная сессия."""
    async with async_session() as session_:
        await session_.connection(
            execution_options={"isolation_level": "AUTOCOMMIT"}
        )
        yield session_

    await truncate_db()

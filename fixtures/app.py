import asyncio
import os
from pathlib import Path
from typing import Generator, Callable, Any

import pytest
from aioresponses import aioresponses
from fastapi import FastAPI
from httpx import AsyncClient, ByteStream
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(autouse=True, scope="session")
def chdir():
    """При запуске одиночных тестов pycharm устанавливает current working
    directory в папку с самим тестом.

    Эта фикстура меняет её на корень проекта
    """
    os.chdir(Path(__file__).parent.parent)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Цикл событий."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def override_httpx_content_encode_json():
    """Небольшой костыль, который фиксит ошибку
    "Object of type datetime is not JSON serializable"
    в тестах, которая возникает где-то под капотом async_client.post()
    за счет использования `default=str` аргумента метода `json.dumps`
    """
    from json import dumps as json_dumps
    from httpx import _content as module_override

    def wrap(json):
        body = json_dumps(json, default=str).encode("utf-8")
        content_length = str(len(body))
        content_type = "application/json"
        headers = {
            "Content-Length": content_length,
            "Content-Type": content_type,
        }
        return headers, ByteStream(body)

    module_override.encode_json = wrap


@pytest.fixture()
def app() -> FastAPI:
    from main import app

    return app


@pytest.fixture()
def di_override(
    app: FastAPI,
) -> Generator[Callable[[Any, Any], None], None, None]:
    """Перезаписывает возвращаемые значения в FastAPI DI

    Пример использования:
    def some_test(di_override, db_mock, redis_mock):
        di_override(get_db, db_mock)
        di_override(get_redis, redis_mock)
    """

    def override(old: Any, new: Any) -> None:
        app.dependency_overrides[old] = lambda: new

    yield override
    app.dependency_overrides = {}


@pytest.fixture()
async def async_client(
    app: FastAPI,
    migration: None,
    db_session: AsyncSession,
) -> AsyncClient:
    async with AsyncClient(
        app=app, base_url="http://0.0.0.0:5000"
    ) as async_client:
        yield async_client


@pytest.fixture
def mock_aioresponse() -> aioresponses:
    with aioresponses() as m:
        yield m

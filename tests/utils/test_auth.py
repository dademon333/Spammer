from unittest.mock import Mock, AsyncMock

import pytest

from application.common_exceptions import UnauthorizedError
from application.database.models.service_token import ServiceToken
from application.database.repositories.service_token_repository import (
    ServiceTokenRepository,
)
from application.utils.auth import parse_auth_token, get_auth_token


@pytest.mark.parametrize(
    "auth_token, expected",
    (
        (None, None),
        ("", None),
        ("Bearer ", ""),
        ("Bearer token123", "token123"),
    ),
)
def test_parse_auth_token(
    auth_token: str,
    expected: str | None,
):
    result = parse_auth_token(auth_token)
    assert result == expected


async def test_get_auth_token_token_not_passed():
    with pytest.raises(UnauthorizedError):
        await get_auth_token(auth_token=None, service_token_repository=Mock())


async def test_get_auth_token_token_not_found():
    mock = Mock(spec=ServiceTokenRepository)
    mock.get_by_token = AsyncMock(return_value=None)

    with pytest.raises(UnauthorizedError):
        await get_auth_token(
            auth_token="some_unknown_token", service_token_repository=mock
        )


async def test_get_auth_token_success(service_token: ServiceToken):
    mock = Mock(spec=ServiceTokenRepository)
    mock.get_by_token = AsyncMock(return_value=service_token)

    result = await get_auth_token(
        auth_token="some_known_token", service_token_repository=mock
    )
    assert result == service_token

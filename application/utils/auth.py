import random
from string import ascii_lowercase, digits

from fastapi import Header, Depends

from application.common_exceptions import UnauthorizedError
from application.database.models.service_token import ServiceToken
from application.di.repositories import get_service_token_repository


def parse_auth_token(
    auth_header: str = Header(None, alias="Authorization")
) -> str | None:
    if not auth_header:
        return None

    return auth_header.removeprefix("Bearer ")


async def get_auth_token(
    auth_token=Depends(parse_auth_token),
    service_token_repository=Depends(get_service_token_repository),
) -> ServiceToken:
    if not auth_token:
        raise UnauthorizedError()

    token = await service_token_repository.get_by_token(auth_token)
    if not token:
        raise UnauthorizedError()
    return token


async def check_auth(token=Depends(get_auth_token)) -> None:  # noqa
    """Ensures that request is authenticated.

    If not, raises 401 UNAUTHORIZED.
    Usage example:
    @router.get(
        '/test_endpoint',
        dependencies=[Depends(check_auth)]
    )
    async def do_foo():
        ...

    """


def generate_access_token() -> str:
    return "".join(random.choices(ascii_lowercase + digits, k=32))

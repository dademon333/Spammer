import pytest

from application.database.models.service_token import ServiceToken
from application.database.repositories.service_token_repository import (
    ServiceTokenRepository,
)


@pytest.fixture()
def service_token() -> ServiceToken:
    return ServiceToken(
        service_name="main_backend",
        token="pk2ax2yqrm0ku0rqa0d5da7zrhr813jv",
    )


@pytest.fixture()
async def service_token_in_db(
    service_token: ServiceToken,
    service_token_repository: ServiceTokenRepository,
) -> ServiceToken:
    await service_token_repository.create(service_token)
    return service_token


@pytest.fixture()
def auth_token(service_token_in_db: ServiceToken) -> str:
    return f"Bearer {service_token_in_db.token}"

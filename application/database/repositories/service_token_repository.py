from application.database.models.service_token import (
    ServiceToken,
    UpdateServiceToken,
)
from application.database.orm_models import ServiceTokenORM
from application.database.repositories.base_repository import BaseDbRepository


class TokenRepository(
    BaseDbRepository[ServiceToken, UpdateServiceToken, ServiceTokenORM]
):
    _table = ServiceTokenORM
    _model = ServiceToken

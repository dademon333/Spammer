from sqlalchemy import select

from application.database.models.service_token import (
    ServiceToken,
    UpdateServiceToken,
)
from application.database.orm_models import ServiceTokenORM
from application.database.repositories.base_repository import BaseDbRepository


class ServiceTokenRepository(
    BaseDbRepository[ServiceToken, UpdateServiceToken, ServiceTokenORM]
):
    _table = ServiceTokenORM
    _model = ServiceToken

    async def get_by_token(self, token: str) -> ServiceToken | None:
        row = await self.db_session.scalars(
            select(ServiceTokenORM).where(ServiceTokenORM.token == token)
        )
        token = row.one_or_none()
        return ServiceToken.from_orm(token) if token else None

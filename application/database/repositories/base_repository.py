from datetime import datetime

from sqlalchemy import select
from sqlalchemy import update as update_
from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.ext.asyncio import AsyncSession

from application.database.orm_models.meta import Base
from application.database.models.base import ModelBase, UpdateModelBase

from abc import ABC, abstractmethod


class BaseDbRepository[
    Model: ModelBase, UpdateModel: UpdateModelBase, Table: Base
](ABC):
    """Базовый класс для ВСЕХ репозиториев подключения к БД."""

    @property
    @abstractmethod
    def _table(self) -> type[Table]:
        ...

    @property
    @abstractmethod
    def _model(self) -> type[Model]:
        ...

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, entry_id: int) -> Model | None:
        row = await self.db_session.get(self._table, entry_id)
        if not row:
            return None
        return self._model.from_orm(row)

    async def get_by_ids(self, ids: list[int]) -> list[Model]:
        if not ids:
            return []
        result = await self.db_session.scalars(
            select(self._table)
            .where(self._table.id.in_(ids))
            .order_by(self._table.id)
        )
        return [self._model.from_orm(x) for x in result.all()]

    async def create(self, model: Model) -> Model:
        result = await self.db_session.scalars(
            insert(self._table)
            .values(model.dict(exclude_unset=True))
            .returning(self._table)
        )
        return self._model.from_orm(result.one())

    async def bulk_create(self, models: list[Model]) -> list[Model]:
        if not models:
            return []

        result = await self.db_session.scalars(
            insert(self._table)
            .values([model.dict(exclude_unset=True) for model in models])
            .returning(self._table)
        )
        return [self._model.from_orm(x) for x in result.all()]

    async def update(self, params: UpdateModel) -> None:
        update_values = params.dict(exclude_unset=True, exclude={"id"})
        update_values["updated_at"] = datetime.utcnow()
        await self.db_session.execute(
            update_(self._table)
            .where(self._table.id == params.id)
            .values(**update_values)
        )

from datetime import datetime, timedelta

from sqlalchemy import select, and_, or_, update

from application.database.models.message import (
    Message,
    UpdateMessage,
    MessageType,
    MessageStatus,
    MessagePlatform,
)
from application.database.orm_models import MessageORM
from application.database.repositories.base_repository import BaseDbRepository


class MessageRepository(BaseDbRepository[Message, UpdateMessage, MessageORM]):
    _table = MessageORM
    _model = Message

    async def take_to_work(
        self,
        message_type: MessageType,
        platform: MessagePlatform,
        count: int,
    ) -> list[Message]:
        # Если сообщение в работе уже 15 минут, скорее всего, что-то наебнулось
        # Попробуем отправить еще раз
        work_timeout = datetime.utcnow() - timedelta(minutes=15)
        rows = await self.db_session.scalars(
            select(MessageORM)
            .where(
                and_(
                    MessageORM.type == message_type,
                    MessageORM.platform == platform,
                    or_(
                        MessageORM.status == MessageStatus.new.value,
                        and_(
                            MessageORM.status == MessageStatus.in_work.value,
                            MessageORM.taken_to_work_at < work_timeout,
                        ),
                    ),
                )
            )
            .order_by(self._table.id)
            .limit(count)
            .with_for_update(skip_locked=True)
        )
        messages = rows.all()
        if not messages:
            return []

        await self.db_session.execute(
            update(MessageORM)
            .values(
                status=MessageStatus.in_work.value,
                taken_to_work_at=datetime.utcnow(),
            )
            .where(MessageORM.id.in_([x.id for x in messages]))
        )
        return [Message.from_orm(x) for x in messages]

    async def update_status(
        self, message_id: int, new_status: MessageStatus
    ) -> None:
        await self.db_session.execute(
            update(MessageORM)
            .where(MessageORM.id == message_id)
            .values(status=new_status.value)
        )

    async def update_statuses(
        self, message_ids: list[int], new_status: MessageStatus
    ) -> None:
        await self.db_session.execute(
            update(MessageORM)
            .where(MessageORM.id.in_(message_ids))
            .values(status=new_status.value)
        )

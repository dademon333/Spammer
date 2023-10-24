from sqlalchemy import Column, BigInteger, Text, VARCHAR, DateTime

from application.database.orm_models.meta import Base


class MessageORM(Base):
    __tablename__ = "messages"

    id = Column(BigInteger, primary_key=True)
    text = Column(Text, nullable=False)
    address = Column(VARCHAR, nullable=False, index=True)
    status = Column(VARCHAR, nullable=False, index=True)
    type = Column(VARCHAR, nullable=False)
    platform = Column(VARCHAR, nullable=False)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    taken_to_work_at = Column(DateTime(timezone=True), nullable=True)

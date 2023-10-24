from sqlalchemy import Column, BigInteger, VARCHAR

from application.database.orm_models import Base


class ServiceTokenORM(Base):
    __tablename__ = "service_tokens"

    id = Column(BigInteger, primary_key=True)
    service_name = Column(VARCHAR, nullable=False)
    token = Column(VARCHAR, nullable=False)

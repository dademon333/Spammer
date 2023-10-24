from application.database.models.base import ModelBase, UpdateModelBase


class ServiceToken(ModelBase):
    service_name: str
    token: str


class UpdateServiceToken(UpdateModelBase):
    service_name: str | None
    token: str | None

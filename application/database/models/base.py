from enum import Enum

from pydantic import BaseModel


class EnumDictSerializer(BaseModel):
    # Костыль для перевода enum items в int/str/etc при вызове model.dict()
    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        for field_name in data.keys():
            if isinstance(data[field_name], Enum):
                data[field_name] = data[field_name].value
        return data


class ModelBase(EnumDictSerializer):
    id: int = 1  # default value will be ignored in create methods

    class Config:
        orm_mode = True


class UpdateModelBase(EnumDictSerializer):
    id: int

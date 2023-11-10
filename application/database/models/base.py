from pydantic import BaseModel


class ModelBase(BaseModel):
    id: int = 1  # default value will be ignored in create methods

    class Config:
        orm_mode = True
        use_enum_values = True


class UpdateModelBase(ModelBase):
    id: int

    class Config:
        use_enum_values = True

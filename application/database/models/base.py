from pydantic import BaseModel


class ModelBase(BaseModel):
    id: int = 1  # default value will be ignored in create methods

    class Config:
        orm_mode = True


class UpdateModelBase(BaseModel):
    id: str

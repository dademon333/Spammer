from pydantic import BaseModel


class OkResponse(BaseModel):
    result: str = "ok"

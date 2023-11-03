from pydantic import BaseModel


class SMSCSuccessfulResponse(BaseModel):
    id: int
    cnt: int
    cost: float
    balance: float


class SMSCErrorResponse(BaseModel):
    error: str
    error_code: str
    id: str | None

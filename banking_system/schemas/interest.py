from pydantic import BaseModel


class InterestRequest(BaseModel):
    account_id: int
    years: int


class InterestResponse(BaseModel):
    interest: float

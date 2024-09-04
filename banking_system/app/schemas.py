from pydantic import BaseModel
from typing import Optional


class AccountBase(BaseModel):
    owner: str
    balance: float
    account_type: str
    interest_rate: Optional[float] = None


class AccountCreate(AccountBase):
    pass


class UpdateAccount(BaseModel):
    balance: float
    account_type: str


class AccountResponse(AccountBase):
    id: int
    fee: float


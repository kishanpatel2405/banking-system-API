from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class TransactionBase(BaseModel):
    amount: float
    type: str
    date: datetime


class TransactionCreate(TransactionBase):
    account_id: int


class TransactionUpdate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True


class TransactionsListResponse(BaseModel):
    account_id: int
    transactions: List[TransactionResponse]

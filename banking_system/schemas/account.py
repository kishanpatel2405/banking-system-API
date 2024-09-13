from pydantic import BaseModel
from datetime import date
from enum import Enum


class AccountType(str, Enum):
    SAVING = "SAVING"
    CHECKING = "CHECKING"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class AccountCreate(BaseModel):
    firstname: str
    lastname: str
    birthdate: date  # 'YYYY-MM-DD'
    mobile_number: str
    account_type: AccountType
    address: str
    nationality: str
    gender: Gender
    aadhaar_card: str
    balance: float


class AccountUpdate(BaseModel):
    firstname: str
    lastname: str
    mobile_number: str
    address: str
    balance: float


class AccountResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    birthdate: date
    mobile_number: str
    account_type: str
    address: str
    nationality: str
    gender: str
    aadhaar_card: str
    balance: float

    class Config:
        from_attributes = True


class TransactionRequest(BaseModel):
    amount: float


class TransactionResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    amount: float
    type: str  # 'deposit', 'withdrawal', 'transfer', 'payment'
    timestamp: date

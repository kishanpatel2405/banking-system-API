from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class AccountType(enum.Enum):
    SAVINGS = "SAVINGS"
    CHECKING = "CHECKING"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, index=True)
    balance = Column(Float)
    account_type = Column(Enum(AccountType), default=AccountType.SAVINGS)
    fee = Column(Float)
    interest_rate = Column(Float)

    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float)
    timestamp = Column(DateTime)

    account = relationship("Account", back_populates="transactions")


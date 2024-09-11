# models/transaction.py

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from core.database import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    account_id = Column(Integer, ForeignKey('accounts.id'))

    # Optional: Define a relationship if needed
    # account = relationship("Account", back_populates="transactions")

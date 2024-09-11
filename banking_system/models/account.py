# models/account.py

from sqlalchemy import Column, Integer, String, Float, Date

from models.base import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    mobile_number = Column(String, nullable=False)
    account_type = Column(String, nullable=False)
    address = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    aadhaar_card = Column(String, nullable=True)  # Allows NULL
    balance = Column(Float, nullable=False)

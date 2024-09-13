from datetime import datetime

from core.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.account import Account as AccountModel
from schemas.account import AccountCreate, AccountUpdate
from models.transaction import Transaction


def get_account(db: Session, account_id: int):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            return {
                "id": account.id,
                "firstname": account.firstname,
                "lastname": account.lastname,
                "birthdate": account.birthdate,
                "mobile_number": account.mobile_number,
                "account_type": account.account_type,
                "address": account.address,
                "nationality": account.nationality,
                "gender": account.gender,
                "aadhaar_card": account.aadhaar_card,
                "balance": account.balance
            }
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        return {"error": str(e)}


def create_account(db: Session, account_data: AccountCreate):
    try:
        new_account = AccountModel(
            firstname=account_data.firstname,
            lastname=account_data.lastname,
            birthdate=account_data.birthdate,
            mobile_number=account_data.mobile_number,
            account_type=account_data.account_type,
            address=account_data.address,
            nationality=account_data.nationality,
            gender=account_data.gender,
            aadhaar_card=account_data.aadhaar_card,
            balance=account_data.balance,
        )
        db.add(new_account)
        db.commit()

        transaction = Transaction(
            account_id=new_account.id,
            amount=account_data.balance,
            transaction_type='initial deposit',
            timestamp=datetime.utcnow()
        )
        db.add(transaction)
        db.commit()

        return {"status": "Account created successfully", "account_id": new_account.id}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error occurred: {e}")
        return {"error": f"Database error: {str(e)}"}


def update_account(db: Session, account_id: int, account_data: AccountUpdate):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            account.firstname = account_data.firstname
            account.lastname = account_data.lastname
            account.mobile_number = account_data.mobile_number
            account.address = account_data.address
            account.balance = account_data.balance
            db.commit()
            return {"status": "Account updated successfully"}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


def delete_account(db: Session, account_id: int):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            db.delete(account)
            db.commit()
            return {"status": "Account deleted successfully"}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}


def get_statements(db: Session, account_id: int):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            transactions = db.query(Transaction).filter(Transaction.account_id == account_id).all()

            transaction_history = [
                {
                    "id": transaction.id,
                    "amount": transaction.amount,
                    "transaction_type": transaction.transaction_type,
                    "timestamp": transaction.timestamp.isoformat()
                }
                for transaction in transactions
            ]

            return {
                "transaction_history": transaction_history
            }
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        return {"error": str(e)}


def deposit_amount(db: Session, account_id: int, amount: float):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            account.balance += amount

            transaction = Transaction(
                account_id=account_id,
                amount=amount,
                transaction_type='deposit',
                timestamp=datetime.utcnow()
            )
            db.add(transaction)
            db.commit()

            logger.info(f"Deposited {amount} to account_id {account_id} and recorded transaction.")
            return {"status": "Amount deposited successfully",
                    "account": {"id": account.id, "firstname": account.firstname, "balance": account.balance}}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error during deposit: {e}")
        return {"error": str(e)}


def withdraw_amount(db: Session, account_id: int, amount: float):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            if account.balance >= amount:
                account.balance -= amount

                transaction = Transaction(
                    account_id=account_id,
                    amount=amount,
                    transaction_type='withdrawal',
                    timestamp=datetime.utcnow()
                )
                db.add(transaction)
                db.commit()

                logger.info(f"Withdrew {amount} from account_id {account_id} and recorded transaction.")
                return {"status": "Amount withdrawn successfully",
                        "account": {"id": account.id, "firstname": account.firstname, "balance": account.balance}}
            else:
                return {"error": "Insufficient balance"}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error during withdrawal: {e}")
        return {"error": str(e)}

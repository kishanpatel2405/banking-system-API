from core.logger import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.account import Account as AccountModel
from schemas.account import AccountCreate, AccountUpdate

def get_account(db: Session, account_id: int):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            return {
                "account": {
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
        return {"success": "Account created successfully", "account_id": new_account.id}
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
            return {"success": "Account updated successfully"}
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
            return {"success": "Account deleted successfully"}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

def get_statements(db: Session, account_id: int):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            return {"account": {"id": account.id, "firstname": account.firstname, "balance": account.balance}}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        return {"error": str(e)}

def deposit_amount(db: Session, account_id: int, amount: float):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            account.balance += amount
            db.commit()
            return {"success": "Amount deposited successfully",
                    "account": {"id": account.id, "firstname": account.firstname, "balance": account.balance}}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

def withdraw_amount(db: Session, account_id: int, amount: float):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            if account.balance >= amount:
                account.balance -= amount
                db.commit()
                return {"success": "Amount withdrawn successfully",
                        "account": {"id": account.id, "firstname": account.firstname, "balance": account.balance}}
            else:
                return {"error": "Insufficient balance"}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

def transfer_amount(db: Session, from_account_id: int, to_account_id: int, amount: float):
    try:
        from_account = db.query(AccountModel).filter(AccountModel.id == from_account_id).first()
        to_account = db.query(AccountModel).filter(AccountModel.id == to_account_id).first()

        if from_account and to_account:
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                db.commit()
                return {"success": "Amount transferred successfully",
                        "from_account": {"id": from_account.id, "firstname": from_account.firstname,
                                         "balance": from_account.balance},
                        "to_account": {"id": to_account.id, "firstname": to_account.firstname,
                                       "balance": to_account.balance}}
            else:
                return {"error": "Insufficient balance in the source account"}
        else:
            return {"error": "One or both accounts not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

def make_payment(db: Session, payer_account_id: int, payee_account_id: int, amount: float):
    try:
        payer_account = db.query(AccountModel).filter(AccountModel.id == payer_account_id).first()
        payee_account = db.query(AccountModel).filter(AccountModel.id == payee_account_id).first()

        if payer_account and payee_account:
            if payer_account.balance >= amount:
                payer_account.balance -= amount
                payee_account.balance += amount
                db.commit()
                return {"success": "Payment made successfully",
                        "payer_account": {"id": payer_account.id, "firstname": payer_account.firstname,
                                          "balance": payer_account.balance},
                        "payee_account": {"id": payee_account.id, "firstname": payee_account.firstname,
                                          "balance": payee_account.balance}}
            else:
                return {"error": "Insufficient balance in the payer's account"}
        else:
            return {"error": "One or both accounts not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

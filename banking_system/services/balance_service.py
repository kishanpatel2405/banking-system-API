from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.account import Account as AccountModel

def get_balance(db: Session, account_id: int):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            return {"balance": account.balance}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        return {"error": str(e)}

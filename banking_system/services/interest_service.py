from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.account import Account as AccountModel

def compute_interest(db: Session, account_id: int, years: int, interest_rate: float = 0.05):
    try:
        account = db.query(AccountModel).filter(AccountModel.id == account_id).first()
        if account:
            interest = account.balance * interest_rate * years
            total_amount = account.balance + interest
            return {"account_id": account_id, "balance": account.balance, "interest": interest,
                    "total_amount": total_amount}
        else:
            return {"error": "Account not found"}
    except SQLAlchemyError as e:
        return {"error": str(e)}

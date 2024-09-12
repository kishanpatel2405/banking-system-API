from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.account import Account as AccountModel
from models.transaction import Transaction


def transfer_amount(db: Session, from_account_id: int, to_account_id: int, amount: float):
    try:
        from_account = db.query(AccountModel).filter(AccountModel.id == from_account_id).first()
        to_account = db.query(AccountModel).filter(AccountModel.id == to_account_id).first()

        if from_account and to_account:
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount

                transfer_out_transaction = Transaction(
                    account_id=from_account_id,
                    amount=-amount,
                    transaction_type='transfer_out',
                    timestamp=datetime.utcnow()
                )
                transfer_in_transaction = Transaction(
                    account_id=to_account_id,
                    amount=amount,
                    transaction_type='transfer_in',
                    timestamp=datetime.utcnow()
                )
                db.add(transfer_out_transaction)
                db.add(transfer_in_transaction)
                db.commit()

                return {
                    "success": "Amount transferred successfully",
                    "from_account": {"id": from_account.id, "firstname": from_account.firstname, "balance": from_account.balance},
                    "to_account": {"id": to_account.id, "firstname": to_account.firstname, "balance": to_account.balance}
                }
            else:
                return {"error": "Insufficient balance in the source account"}
        else:
            return {"error": "One or both accounts not found"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": str(e)}

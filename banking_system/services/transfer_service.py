from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.account import Account as AccountModel

def transfer_funds(db: Session, sender_account_id: int, receiver_account_id: int, amount: float):
    try:
        # Fetch sender account
        sender_account = db.query(AccountModel).filter(AccountModel.id == sender_account_id).first()
        if not sender_account:
            return {"error": "Sender account not found"}

        # Fetch receiver account
        receiver_account = db.query(AccountModel).filter(AccountModel.id == receiver_account_id).first()
        if not receiver_account:
            return {"error": "Receiver account not found"}

        # Check sufficient funds
        if sender_account.balance < amount:
            return {"error": "Insufficient funds"}

        # Perform the transfer
        sender_account.balance -= amount
        receiver_account.balance += amount
        db.commit()

        return {"success": "Transfer completed successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        # Return a generic error message without details
        return {"error": "An error occurred while processing the request"}

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account, Transaction
import logging

router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("")
def transfer(
        from_account_id: int,
        to_account_id: int,
        amount: float,
        db: Session = Depends(get_db)
):
    from_account = db.query(Account).filter(Account.id == from_account_id).first()
    to_account = db.query(Account).filter(Account.id == to_account_id).first()

    if not from_account or not to_account:
        raise HTTPException(status_code=404, detail="Account not found")

    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid transfer amount")

    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    try:
        from_account.balance -= amount
        to_account.balance += amount

        from_transaction = Transaction(
            account_id=from_account_id,
            amount=-amount,
            timestamp=datetime.utcnow()
        )
        to_transaction = Transaction(
            account_id=to_account_id,
            amount=amount,
            timestamp=datetime.utcnow()
        )

        db.add(from_transaction)
        db.add(to_transaction)
        db.commit()

        return {"detail": "Transfer successful"}
    except Exception as e:
        logger.error(f"An error occurred during the transfer: {e}", exc_info=True)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/{account_id}")
def get_transaction_history(account_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching transactions for account_id: {account_id}")
    try:
        logger.debug(f"Executing query for account_id: {account_id}")

        transactions = db.query(Transaction).filter(Transaction.account_id == account_id).all()

        logger.debug(f"Number of transactions found: {len(transactions)}")

        if not transactions:
            logger.info(f"No transactions found for account_id: {account_id}")
            raise HTTPException(status_code=404, detail="No transactions found for this account.")

        return transactions
    except HTTPException as http_err:
        logger.error(f"HTTP exception occurred: {http_err.detail}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching transactions: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


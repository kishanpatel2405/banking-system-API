from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction
from datetime import datetime
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


@router.get("/{account_id}/from/{start_date}/to/{end_date}", response_model=list)
def get_transaction_history_range(
        account_id: int, start_date: str, end_date: str, db: Session = Depends(get_db)
):
    try:
        logger.info(f"Fetching transactions for account_id: {account_id} from {start_date} to {end_date}")
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        if start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date.")
    except ValueError:
        logger.error(f"Invalid date format provided: {start_date}, {end_date}")
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD HH:MM:SS.")

    try:
        transactions = db.query(Transaction).filter(
            Transaction.account_id == account_id,
            Transaction.timestamp.between(start_date, end_date)
        ).all()

        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found for this period.")

        return transactions
    except HTTPException as http_err:
        logger.error(f"HTTP error occurred: {http_err.detail}")
        raise http_err
    except Exception as e:
        logger.error(f"An unexpected error occurred while fetching transactions for range: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
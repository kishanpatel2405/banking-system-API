from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.transaction import Transaction as TransactionModel
from schemas.transaction import TransactionsListResponse, TransactionResponse

def list_transactions(db: Session, account_id: int) -> TransactionsListResponse:
    try:
        transactions = db.query(TransactionModel).filter(TransactionModel.account_id == account_id).all()
        transaction_list = [
            TransactionResponse(
                id=t.id,
                amount=t.amount,
                type=t.type,
                date=t.date,
                account_id=t.account_id
            ) for t in transactions
        ]
        return TransactionsListResponse(account_id=account_id, transactions=transaction_list)
    except SQLAlchemyError as e:
        return {"error": f"Database error: {str(e)}"}

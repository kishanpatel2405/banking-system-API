from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import JWTBearer, TokenData
from core.database import get_db
from services.transaction_service import list_transactions
from schemas.transaction import TransactionsListResponse

router = APIRouter()

@router.get("", response_model=TransactionsListResponse, tags=["Transactions"])
def your_transactions(account_id: int, db: Session = Depends(get_db),
                               token_data: TokenData = Depends(JWTBearer())):
    result = list_transactions(db, account_id)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import JWTBearer, TokenData
from services.balance_service import get_balance
from schemas.balance import BalanceResponse

router = APIRouter()

@router.get("", response_model=BalanceResponse, tags=["Balance"])
def check_your_balance(account_id: int, db: Session = Depends(get_db),
                         token_data: TokenData = Depends(JWTBearer())):
    result = get_balance(db, account_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

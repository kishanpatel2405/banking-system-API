from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import JWTBearer, TokenData
from services.interest_service import compute_interest

router = APIRouter()


@router.get("", tags=["Interest"], name="Calculate Your Interest")
def check_your_interest(
        account_id: int,
        years: int,
        interest_rate: float = 0.05,
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    result = compute_interest(db, account_id, years, interest_rate)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

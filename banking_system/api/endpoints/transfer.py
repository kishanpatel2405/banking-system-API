from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from services.transfer_service import transfer_amount
from core.database import get_db
from core.security import JWTBearer, TokenData

router = APIRouter()

@router.post("", tags=["Transfers"])
def transfer_your_amount(
        from_account_id: int = Form(...),
        to_account_id: int = Form(...),
        amount: float = Form(...),
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    result = transfer_amount(db, from_account_id, to_account_id, amount)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
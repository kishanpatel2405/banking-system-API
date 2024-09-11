from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.transfer import Transfer
from services.transfer_service import transfer_funds
from core.database import get_db
from core.security import JWTBearer, TokenData

router = APIRouter()

@router.post("/funds", tags=["Transfers"])
def transfer_your_funds(
        transfer: Transfer,
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    result = transfer_funds(db, transfer.from_account_id, transfer.to_account_id, transfer.amount)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import Account, InterestResponse
from app.database import get_db
from pydantic import BaseModel

router = APIRouter()


@router.get("/{account_id}/interest", response_model=InterestResponse)
async def get_interest(account_id: int, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    balance = account.balance
    interest_rate = account.interest_rate
    interest_amount = balance * interest_rate

    return InterestResponse(
        account_id=account.id,
        interest_amount=interest_amount,
        interest_rate=interest_rate,
        balance=balance
    )

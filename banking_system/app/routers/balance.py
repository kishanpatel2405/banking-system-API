from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account
from sqlalchemy import func

router = APIRouter()


@router.get("", response_model=dict)
def get_total_balance(
    db: Session = Depends(get_db)
):
    total_balance = db.query(Account).with_entities(func.sum(Account.balance)).scalar()
    return {"total_balance": total_balance}

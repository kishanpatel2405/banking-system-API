from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account
from app.schemas import AccountCreate, UpdateAccount, AccountResponse

router = APIRouter()


@router.post("", response_model=AccountResponse)
def create_account(
        account: AccountCreate,
        db: Session = Depends(get_db),
):
    fee = 0.0
    if account.account_type == "SAVINGS":
        fee = 5.0
    elif account.account_type == "CHECKING":
        fee = 10.0

    db_account = Account(
        owner=account.owner,
        balance=account.balance,
        account_type=account.account_type,
        fee=fee,
        interest_rate=account.interest_rate
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.patch("/{account_id}/update", response_model=AccountResponse)
def update_account(
        account_id: int,
        update: UpdateAccount,
        db: Session = Depends(get_db)
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account.balance = update.balance
    account.account_type = update.account_type

    if account.account_type == "SAVINGS":
        account.fee = 5.0
    elif account.account_type == "CHECKING":
        account.fee = 10.0

    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}/statement", response_model=dict)
def get_statement(
        account_id: int,
        db: Session = Depends(get_db),
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "owner": account.owner,
        "balance": account.balance
    }


@router.delete("/{account_id}", response_model=dict)
def delete_account(
        account_id: int,
        db: Session = Depends(get_db)
):
    account = db.query(Account).filter(Account.id == account_id).first()
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    db.delete(account)
    db.commit()
    return {"detail": "Account deleted"}

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import JWTBearer, TokenData
from schemas.account import AccountCreate, AccountUpdate, AccountType, Gender
from services.account_service import (
    create_account,
    update_account,
    delete_account,
    get_statements,
    get_account,
    deposit_amount,
    withdraw_amount,
)

router = APIRouter()


@router.get("/{account_id}", tags=["Accounts"])
def read_your_account(
        account_id: int,
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    result = get_account(db, account_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("", tags=["Accounts"])
def create_your_account(
        firstname: str = Form(...),
        lastname: str = Form(...),
        birthdate: str = Form(...),
        mobile_number: str = Form(...),
        account_type: AccountType = Form(...),
        address: str = Form(...),
        nationality: str = Form(...),
        gender: Gender = Form(...),
        aadhaar_card: str = Form(...),
        balance: float = Form(...),
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    account_data = AccountCreate(
        firstname=firstname,
        lastname=lastname,
        birthdate=birthdate,
        mobile_number=mobile_number,
        account_type=account_type,
        address=address,
        nationality=nationality,
        gender=gender,
        aadhaar_card=aadhaar_card,
        balance=balance,
    )
    result = create_account(db, account_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.put("", tags=["Accounts"])
def update_your_account(
        account_id: int,
        firstname: str = Form(...),
        lastname: str = Form(...),
        birthdate: str = Form(...),
        mobile_number: str = Form(...),
        account_type: AccountType = Form(...),
        address: str = Form(...),
        nationality: str = Form(...),
        gender: Gender = Form(...),
        aadhaar_card: str = Form(...),
        balance: float = Form(...),
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    account_data = AccountUpdate(
        firstname=firstname,
        lastname=lastname,
        mobile_number=mobile_number,
        address=address,
        balance=balance,
    )
    result = update_account(db, account_id, account_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.delete("", tags=["Accounts"])
def delete_your_account(
        account_id: int,
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    result = delete_account(db, account_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("", tags=["Accounts"])
def get_your_statements(
        account_id: int,
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    result = get_statements(db, account_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/deposit", tags=["Accounts"])
def deposit_amount_endpoint(
        account_id: int = Form(...),
        amount: float = Form(...),
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    result = deposit_amount(db, account_id, amount)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/withdraw", tags=["Accounts"])
def withdraw_amount_endpoint(
        account_id: int = Form(...),
        amount: float = Form(...),
        db: Session = Depends(get_db),
        token_data: TokenData = Depends(JWTBearer())
):
    result = withdraw_amount(db, account_id, amount)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

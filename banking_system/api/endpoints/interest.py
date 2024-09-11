from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.security import JWTBearer, TokenData
from services.interest_service import compute_interest
from schemas.interest import InterestRequest, InterestResponse

router = APIRouter()

@router.get("/", response_model=InterestResponse, tags=["Interest"])
def check_your_interest(
    request: InterestRequest,
    db: Session = Depends(get_db),
    token_data: TokenData = Depends(JWTBearer())
):
    result = compute_interest(db, request.account_id, request.years)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

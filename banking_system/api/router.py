from fastapi import APIRouter
from api.endpoints import accounts, balance, interest, transfer

api_router = APIRouter()

api_router.include_router(accounts.router, prefix="/account", tags=["Accounts"])
api_router.include_router(transfer.router, prefix="/transfer", tags=["Transfers"])
api_router.include_router(balance.router, prefix="/balance", tags=["Balance"])
api_router.include_router(interest.router, prefix="/interest", tags=["Interest"])


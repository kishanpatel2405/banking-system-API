from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer

from app.routers import accounts_router, transactions_router, transfer_router, balance_router

app = FastAPI()

app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
app.include_router(transfer_router, prefix="/transfer", tags=["transfer"])
app.include_router(balance_router, prefix="/balance", tags=["balance"])

security = HTTPBearer()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FAST API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["security"] = [
        {
            "bearerAuth": []
        }
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi

app = FastAPI()

SECRET_KEY = "1234567890qwertyuiop"
ALGORITHM = "HS256"


security = HTTPBearer()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API",
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

from urllib.request import Request

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={"message": "An unexpected error occurred"}
        )


class ApiException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


async def api_exception_handler(request: Request, exc: ApiException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

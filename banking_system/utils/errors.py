# banking_system/utils/errors.py

from fastapi import HTTPException, status


def handle_errors(message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
    """ Custom error handler function """
    raise HTTPException(status_code=status_code, detail=message)


class ApiException(Exception):
    def __init__(self, detail: str):
        self.detail = detail

from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request
from typing import Optional
import jwt
from pydantic import BaseModel

SECRET_KEY = "asdfghjkl"
ALGORITHM = "HS256"


class TokenData(BaseModel):
    username: str
    email: Optional[str] = None


def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.DecodeError as e:
        raise HTTPException(status_code=401, detail="Invalid token")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            try:
                payload = decode_jwt(credentials.credentials)
                return payload
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token has expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code")

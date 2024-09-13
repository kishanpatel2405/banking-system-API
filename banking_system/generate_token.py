import jwt

SECRET_KEY = "asdfghjkl"
ALGORITHM = "HS256"


def create_jwt_token(data: dict) -> str:
    try:
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


data = {"user_id": 123, "username": "bank_users"}
token = create_jwt_token(data)
print(token)

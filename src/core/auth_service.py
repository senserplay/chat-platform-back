from fastapi import HTTPException, status
from typing import Optional
import jwt
import bcrypt
from datetime import datetime, timedelta
from .config import env_settings
import secrets
import string


class AuthService:
    def create_access_token(self, user_id: int):
        expiration = datetime.utcnow() + timedelta(days=env_settings.JWT_ACCESS_TOKEN_EXPIRE_DAYS)
        payload = {
            "sub": str(user_id),
            "exp": expiration
        }
        token = jwt.encode(payload, env_settings.JWT_SECRET_KEY, algorithm=env_settings.JWT_ALGORITHM)
        return token

    def verify_password(self, plain_password, hashed_password):
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def hash_password(self, password: str):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_token(self, token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, env_settings.JWT_SECRET_KEY, algorithms=[env_settings.JWT_ALGORITHM])
            user_id = payload.get("sub")
            if user_id is None:
                raise jwt.InvalidTokenError("User ID not found in token.")
            return int(user_id)
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired."
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
            )

    def generate_simple_token(self, length=64):
        alphabet = string.ascii_lowercase + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))


auth_service = AuthService()

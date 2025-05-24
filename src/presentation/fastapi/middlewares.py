from fastapi import HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from src.application.schemas.user import UserSchema
from src.infrastructure.postgres.repositories.user import (
    UserNotFoundError,
)
from src.core.auth_service import auth_service
from src.infrastructure.redis.storage.user_storage import users_storage

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


async def get_current_user(
    token: str = Security(oauth2_scheme)
) -> UserSchema:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid",
        )

    try:
        user_id = auth_service.verify_token(token)

        user = users_storage.get_user(user_id)
        if not user:
            raise UserNotFoundError(f"User {user_id} not found")

        return user

    except (HTTPException, UserNotFoundError) as e:
        logger.error(f"Authentication error: {str(e)}")
        raise
    except Exception as e:
        logger.info(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal authentication error",
        )

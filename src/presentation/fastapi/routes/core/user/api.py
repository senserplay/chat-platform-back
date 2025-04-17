from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session as DBSession

from src.application.schemas.user import (
    UserSchema,
    UserLogin,
    UserToken,
    UserCreate, UserUpdate,
)
from src.infrastructure.postgres.client import get_db_session
from src.infrastructure.postgres.repositories.user import (
    users_repository,
    UserNotFoundError,
    IncorrectPasswordError,
    UserAlreadyExistsError,
)
from src.presentation.fastapi.middlewares import get_current_user

ROUTER = APIRouter(prefix="/user")


@ROUTER.post(
    "/login",
    response_model=UserToken,
    summary="Авторизовать пользователя",
)
async def login_user(
        request: UserLogin, db_session: DBSession = Depends(get_db_session)
) -> UserToken:
    try:
        token = users_repository.get_token(db_session, request)
        return UserToken(token=token)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IncorrectPasswordError as e:
        raise HTTPException(status_code=403, detail=str(e))


@ROUTER.post(
    "/registration",
    response_model=UserToken,
    summary="Зарегистрировать пользователя",
)
async def registration_user(
        request: UserCreate, db_session: DBSession = Depends(get_db_session)
) -> UserToken:
    try:
        users_repository.create_user(db_session, request.model_copy())
        token = users_repository.get_token(
            db_session, UserLogin(**request.model_dump())
        )
        return UserToken(token=token)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except IncorrectPasswordError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@ROUTER.get(
    "",
    response_model=UserSchema,
    summary="Получить пользователя",
)
async def get_user(
        user: UserSchema = Depends(get_current_user),
        db_session: DBSession = Depends(get_db_session),
) -> UserSchema:
    return user


@ROUTER.patch(
    "",
    response_model=UserSchema,
    summary="Частично изменить пользователя",
)
async def patch_user(
        request: UserUpdate,
        user: UserSchema = Depends(get_current_user),
        db_session: DBSession = Depends(get_db_session),
) -> UserSchema:
    try:
        return users_repository.update_user(db_session, request, user.id)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@ROUTER.delete(
    "",
    summary="Удалить пользователя",
)
async def delete_user(
        user: UserSchema = Depends(get_current_user),
        db_session: DBSession = Depends(get_db_session),
):
    try:
        users_repository.delete_user(db_session, user.id)
        return {"status": "ok"}
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

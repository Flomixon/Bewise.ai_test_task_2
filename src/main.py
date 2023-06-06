from fastapi import FastAPI
from users.base_config import auth_backend, fastapi_users
from users.shemas import UserCreate, UserRead
from file_convert.router import file_convert_router


app = FastAPI(
    title='waw to mp3'
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    file_convert_router,
    tags=["Convert"]
)

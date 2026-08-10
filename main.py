from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.core.logger import logger
from app.db.database import AsyncSessionLocal
from app.api.categoryAPI import router as categoryRouter
from app.api.productAPI import router as productRouter
from app.api.userAPI import router as userRouter
from app.api.cartAPI import router as cartRouter
from app.api.orderAPI import router as orderRouter
from app.core.exception_handler import (
    already_exists_error_handler,
    cart_access_denied_error_handler,
    empty_cart_error_handler,
    invalid_credentials_error_handler,
    not_found_error_handler,
    value_error_handler,
)
from app.core.exceptions import (
    AlreadyExistsError,
    CartAccessDeniedError,
    EmptyCartError,
    InvalidCredentialsError,
    NotFoundError,
)

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    async with AsyncSessionLocal() as session:
        await session.execute(
            text("TRUNCATE TABLE products, categories RESTART IDENTITY CASCADE")
        )
        logger.info("Connected to PostgreSQL")

    logger.info("Application startup completed")
    yield
    logger.info("Application stopped")


application = FastAPI(lifespan=lifespan)


application.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # для портфолио-проекта ок; в реальном проде указывали бы конкретный домен фронтенда
    allow_credentials=False,  # у тебя Bearer-токен, не cookie — credentials не нужны
    allow_methods=["*"],
    allow_headers=["*"],
)


@application.get("/", summary="Start page")
def starter_page() -> dict[str, str]:
    logger.info("GET /")
    return {"success": "true"}


application.include_router(categoryRouter)
application.include_router(productRouter)
application.include_router(userRouter)
application.include_router(cartRouter)
application.include_router(orderRouter)
application.add_exception_handler(NotFoundError, not_found_error_handler)
application.add_exception_handler(AlreadyExistsError, already_exists_error_handler)
application.add_exception_handler(
    InvalidCredentialsError, invalid_credentials_error_handler
)
application.add_exception_handler(ValueError, value_error_handler)
application.add_exception_handler(
    CartAccessDeniedError, cart_access_denied_error_handler
)
application.add_exception_handler(EmptyCartError, empty_cart_error_handler)


from pathlib import Path
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
application.mount(
    "/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static"
)

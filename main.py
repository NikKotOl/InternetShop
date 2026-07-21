from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.exception_handler import not_found_error_handler
from app.core.exceptions import NotFoundError
from sqlalchemy import text

from app.core.logger import logger
from app.db.database import AsyncSessionLocal
from app.api.categoryAPI import router as categoryRouter
from app.api.productAPI import router as productRouter

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")

    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))
        logger.info("Connected to PostgreSQL")

    logger.info("Application startup completed")
    yield
    logger.info("Application stopped")


app = FastAPI(lifespan=lifespan)


@app.get("/", summary="Start page")
def starter_page() -> dict[str, str]:
    logger.info("GET /")
    return {"success": "true"}


app.include_router(categoryRouter)
app.include_router(productRouter)
app.add_exception_handler(NotFoundError, not_found_error_handler)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

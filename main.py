from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text

from app.db.database import AsyncSessionLocal

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))
        print("Postgres connected!")
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def starter_page() -> str:
    return "Welcome!"


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)

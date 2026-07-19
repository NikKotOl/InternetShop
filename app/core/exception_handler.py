from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import NotFoundError


async def not_found_error_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": exc.message})

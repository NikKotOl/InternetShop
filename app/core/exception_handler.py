from fastapi import Request
from fastapi.responses import JSONResponse


def not_found_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

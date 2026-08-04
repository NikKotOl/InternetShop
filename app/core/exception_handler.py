from fastapi import Request
from fastapi.responses import JSONResponse


def not_found_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


def already_exists_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


def invalid_credentials_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=401, content={"detail": str(exc)})


def value_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(exc)})


def cart_access_denied_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=403, content={"detail": str(exc)})

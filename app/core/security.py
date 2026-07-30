from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import settings


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    }

    return jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> int:
    return int(jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])["sub"])

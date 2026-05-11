from typing import Any

from django.http import HttpRequest
from ninja.security import HttpBearer

from config import settings

import jwt


class JWTAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str) -> Any | None:
        try: 
            payload = jwt.decode(
                token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHIM]
            )

            return payload

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
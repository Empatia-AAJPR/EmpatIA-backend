from datetime import datetime, timedelta
import os
from uuid import UUID, uuid4
from venv import create

from passlib.context import CryptContext

import jwt

from apps.Accounts.domain.entities import TokenEntity, UserEntity
from apps.Accounts.domain.repositories import IHashService, ITokenServices
from apps.Accounts.infrastructure.models import Token
from config import settings

pwd_context = CryptContext(schemes=['bcrypt'])


class TokenService(ITokenServices):
    def generate_access_token(self, user: UserEntity):
        payload = {
            'sub': str(user.id),
            'email': user.email,
            'rule': user.rule,
            'exp': datetime.utcnow()
            + timedelta(minutes=settings.JWT_EXP_MINUTES),
        }

        return jwt.encode(
            payload,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHIM,
        )

    def generate_refresh_token(
        self, user: UserEntity
    ) -> tuple[str, TokenEntity]:
        token = str(uuid4())

        _hash_token = self.hash_token(token)

        model = Token.objects.create(
            id=uuid4(),
            hash_token=_hash_token,
            user_id=user.id,
            expire_at=datetime.utcnow()
            + timedelta(days=settings.JWT_EXP_DAYS),
            created_at=datetime.utcnow(),
            revoked=False
        )

        entity = TokenEntity(
            id=model.id,
            hash_token=model.hash_token,
            user_id=model.user_id, #type: ignore
            expire_at=model.expire_at,
        )

        return _hash_token, entity

    def decode_token(self, hash_token: str) -> dict:
        return jwt.decode(
            hash_token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHIM],
        )

    def hash_token(self, raw_token: str) -> str:
        import hashlib

        return hashlib.sha256(raw_token.encode()).hexdigest()


class HashService(IHashService):
    @staticmethod
    def hash_password(password: str):
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(raw_password: str, hash_password: str):
        return pwd_context.verify(raw_password, hash_password)

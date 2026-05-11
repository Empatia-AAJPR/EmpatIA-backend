from typing import List
from uuid import UUID

from pydantic import EmailStr

from apps.Accounts.domain.entities import TokenEntity, UserEntity
from apps.Accounts.domain.repositories import ITokenRepository, IUserRepository
from apps.Accounts.domain.rules import UserRules
from apps.Accounts.infrastructure.models import Token, User


class UserRepository(IUserRepository):
    def save(self, user: UserEntity) -> UserEntity:
        User.objects.update_or_create(
            id=user.id,
            defaults={
                'name': user.name,
                'email': user.email,
                'password': user.password,
                'rule': user.rule,
                'created_at': user.created_at,
                'deleted_at': user.deleted_at,
                'active': user.active
            },
        )

        return user

    def find_by_id(self, id: UUID) -> UserEntity | None:
        try:
            return self._to_entity(User.objects.get(id=id))

        except User.DoesNotExist:
            return None

    def find_by_email(self, email: str) -> UserEntity | None:
        try:
            return self._to_entity(User.objects.get(email=email))

        except User.DoesNotExist:
            return None

    def exists_email(self, email: EmailStr) -> bool:
        return User.objects.filter(email=email).exists()

    def list_users_by_rule(self, rule: UserRules) -> List[UserEntity]:
        return [
            self._to_entity(model) for model in User.objects.filter(rule=rule)
        ]

    def _to_entity(self, model: User) -> UserEntity:
        return UserEntity(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            rule=model.rule,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
            active=model.active
        )


class TokenRepository(ITokenRepository):
    def save(self, token: TokenEntity) -> TokenEntity:
        Token.objects.update_or_create(
            id=token.id,
            defaults={
                'hash_token': token.hash_token,
                'user_id': token.user_id,
                'created_at': token.created_at,
                'revoked': token.revoked,
            },
        )

        return token

    def find_by_hash(self, hash_token: EmailStr) -> TokenEntity | None:
        try:
            return self._to_entity(Token.objects.get(hash_token=hash_token))

        except Token.DoesNotExist:
            return None

    def find_by_id(self, id: UUID) -> TokenEntity | None:
        try:
            return self._to_entity(Token.objects.get(id=id))

        except Token.DoesNotExist:
            return None

    def _to_entity(self, model: Token) -> TokenEntity:
        return TokenEntity(
            id=model.id,
            hash_token=model.hash_token,
            user_id=model.user_id,
            created_at=model.created_at,
            revoked=model.revoked,
        )

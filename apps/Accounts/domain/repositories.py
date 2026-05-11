from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from pydantic import EmailStr

from apps.Accounts.domain.entities import TokenEntity, UserEntity
from apps.Accounts.domain.rules import UserRules


class IUserRepository(ABC):
    @abstractmethod
    def save(self, user: UserEntity) -> UserEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> UserEntity | None:
        ...

    @abstractmethod
    def find_by_email(self, email: EmailStr) -> UserEntity | None:
        ...

    @abstractmethod
    def exists_email(self, email: EmailStr) -> bool:
        ...

    @abstractmethod
    def list_users_by_rule(self, rule: UserRules) -> List[UserEntity]:
        ...


class ITokenRepository(ABC):
    @abstractmethod
    def save(self, token: TokenEntity) -> TokenEntity:
        ...

    @abstractmethod
    def find_by_hash(self, hash: str) -> TokenEntity | None:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> TokenEntity | None:
        ...


class ITokenServices(ABC):
    @abstractmethod
    def generate_access_token(self, user: UserEntity) -> str:
        ...

    @abstractmethod
    def generate_refresh_token(
        self, user: UserEntity
    ) -> tuple[str, TokenEntity]:
        ...

    @abstractmethod
    def decode_token(self, hash_token: str) -> dict:
        ...

    @abstractmethod
    def hash_token(self, raw_token: str) -> str:
        ...


class IHashService(ABC):
    @abstractmethod
    def hash_password(self, raw_password: str) -> str:
        ...

    @abstractmethod
    def verify_password(self, raw_password: str, hash_password: str) -> str:
        ...

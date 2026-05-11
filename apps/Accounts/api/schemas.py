from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr

from apps.Accounts.application.dto import LoginInDTO, RefreshTokenOutDTO, UserInDTO, UserOutDTO, UserUpdateDTO
from apps.Accounts.domain.rules import UserRules


class UserIn(Schema):
    name: str
    email: str
    password: str

    def to_dto(self) -> UserInDTO:
        return UserInDTO(
            name=self.name,
            email=self.email,
            password=self.password,
            rule=UserRules.PENDING,
        )


class UserOut(Schema):
    id: UUID
    name: str
    email: str
    password: str
    active: bool
    rule: UserRules

    @staticmethod
    def from_domain(dto: UserOutDTO):
        return UserOut(
            id=dto.id,
            name=dto.name,
            email=dto.email,
            password=dto.password,
            active=dto.active,
            rule=dto.rule,
        )


class UserUpdateIn(Schema):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

    def to_dto(self) -> UserUpdateDTO:
        return UserUpdateDTO(
            name=self.name,
            email=self.email,
            password=self.password,
            rule=UserRules.PENDING,
        )
    

class LoginIn(Schema):
    email: EmailStr
    password: str

    def to_dto(self) -> LoginInDTO:
        return LoginInDTO(
            email=self.email,
            password=self.password
        )


class TokenOut(Schema):
    access_token: str
    refresh_token: str

    @staticmethod
    def from_domain(dto: RefreshTokenOutDTO):
        return TokenOut(
            access_token=dto.access_token,
            refresh_token=dto.refresh_token
        )

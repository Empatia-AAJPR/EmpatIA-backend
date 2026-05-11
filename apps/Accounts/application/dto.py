from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from apps.Accounts.domain.rules import UserRules


class UserInDTO(BaseModel):
    name: str
    email: str
    password: str
    rule: UserRules = UserRules.PENDING


class UserOutDTO(BaseModel):
    id: UUID
    name: str
    email: str
    password: str
    active: bool
    rule: UserRules

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
            rule=model.rule,
            active=model.active,
        )


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rule: Optional[UserRules] = None


class RefreshTokenOutDTO(BaseModel):
    access_token: str
    refresh_token: str

    @classmethod
    def from_domain(cls, access, refresh):
        return cls(access_token=access, refresh_token=refresh)


class LoginInDTO(BaseModel):
    email: EmailStr
    password: str

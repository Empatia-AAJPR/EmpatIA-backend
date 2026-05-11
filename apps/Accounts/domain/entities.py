from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import EmailStr

from apps.Accounts.domain.exceptions import (
    ConflictFieldException,
    FieldRequiredException,
)
from apps.Accounts.domain.rules import UserRules


@dataclass
class UserEntity:
    id: UUID = field(default_factory=uuid4)

    name: str = field(default='')
    email: str = field(default='')
    password: str = field(default='')
    rule: str = field(default=UserRules.PENDING)

    active: bool = field(default=True)

    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def is_active(self) -> bool:
        return self.active

    def deactive_user(self):
        if not self.active:
            raise ConflictFieldException('user already deactive')

        self.active = False

    def change_password(self, new_password: str) -> None:
        if not new_password:
            raise FieldRequiredException('field new password is required')

        self.password = new_password

    def change_rule(self, new_rule: str) -> None:
        if not new_rule:
            raise FieldRequiredException('field new rule is required')

        self.rule = new_rule

    def change_email(self, new_email: EmailStr) -> None:
        if not new_email:
            raise FieldRequiredException('field new email is required')

        self.email = new_email

    def change_name(self, new_name):
        if not new_name:
            raise FieldRequiredException('field new name is required')
        
        self.name = new_name


@dataclass
class TokenEntity:
    id: UUID = field(default_factory=uuid4)
    hash_token: str = field(default='')
    user_id: UUID | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    expire_at: datetime | None = field(default=None)
    revoked: bool = field(default=False)

    def deactive_token(self) -> None:
        if self.revoked is True:
            raise ConflictFieldException('token already revoked')

        self.revoked = True

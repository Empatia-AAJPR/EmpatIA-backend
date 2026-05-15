from datetime import date
from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import EmailStr

from apps.Accounts.domain.rules import UserRules
from apps.Users.application.dto import (
    CoordinatorInDTO,
    CoordinatorOutDTO,
    CoordinatorUpdateDTO,
    DirectorInDTO,
    DirectorOutDTO,
    StudentInDTO,
    StudentOutDTO,
    StudentUpdateDTO,
)
from apps.Users.domain.value_objects import UploadFileVO


class StudentIn(Schema):
    name: str
    email: EmailStr
    password: str
    date_birth: date
    classroom: UUID

    def to_dto(self) -> StudentInDTO:
        return StudentInDTO(
            name=self.name,
            email=self.email,
            password=self.password,
            date_birth=self.date_birth,
            classroom=self.classroom,
        )


class StudentOut(Schema):
    id: UUID
    name: str
    email: str
    active: bool
    rule: UserRules
    user: UUID
    classroom: Optional[UUID] = None
    date_birth: date
    photo: str

    @staticmethod
    def from_domain(dto: StudentOutDTO):
        return StudentOutDTO(
            id=dto.id,
            name=dto.name,
            email=dto.email,
            active=dto.active,
            rule=dto.rule,
            user=dto.user,
            classroom=dto.classroom,
            date_birth=dto.date_birth,
            photo=dto.photo,
        )


class UpdateStudentIn(Schema):
    date_birth: Optional[date] = None
    classroom: Optional[UUID] = None

    def to_dto(self) -> StudentUpdateDTO:
        return StudentUpdateDTO(
            date_birth=self.date_birth,
            classroom=self.classroom,
        )


class CoordinatorIn(Schema):
    name: str
    email: EmailStr
    password: str
    date_birth: date
    nucleos_group: UUID

    def to_dto(self) -> CoordinatorInDTO:
        return CoordinatorInDTO(
            name=self.name,
            email=self.email,
            password=self.password,
            date_birth=self.date_birth,
            nucleos_group=self.nucleos_group,
        )


class CoordinatorOut(Schema):
    id: UUID
    name: str
    email: str
    password: str
    rule: UserRules
    active: bool
    user: UUID
    nucleos_group: UUID

    @staticmethod
    def from_domain(dto: CoordinatorOutDTO):
        return CoordinatorOut(
            id=dto.id,
            user=dto.user,
            name=dto.name,
            email=dto.email,
            password=dto.password,
            active=dto.active,
            rule=dto.rule,
            nucleos_group=dto.nucleos_group,
        )


class UpdateCoordinatorIn(Schema):
    nucleos_group: Optional[UUID] = None

    def to_dto(self) -> CoordinatorUpdateDTO:
        return CoordinatorUpdateDTO(
            nucleos_group=self.nucleos_group,
        )


class DirectorIn(Schema):
    name: str
    email: EmailStr
    password: str
    school: UUID

    def to_dto(self) -> DirectorInDTO:
        return DirectorInDTO(
            name=self.name,
            email=self.email,
            password=self.password,
            school=self.school,
        )


class DirectorOut(Schema):
    id: UUID
    user: UUID
    name: str
    email: EmailStr
    password: str
    active: bool
    school: UUID

    @staticmethod
    def from_domain(dto: DirectorOutDTO):
        return DirectorOut(
            id=dto.id,
            user=dto.user,
            name=dto.name,
            email=dto.email,
            password=dto.password,
            active=dto.active,
            school=dto.school,
        )

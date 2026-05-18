from datetime import datetime
from uuid import UUID

from ninja import Schema

from apps.Classroom.application.dto import (
    ClassroomInDTO,
    ClassroomOutDTO,
    UpdateClassroomInDTO,
)


class ClassroomIn(Schema):
    course: str
    school: UUID

    def to_dto(self) -> ClassroomInDTO:
        return ClassroomInDTO(course=self.course, school=self.school)


class ClassroomOut(Schema):
    id: UUID
    course: str
    school: UUID
    deleted_at: datetime | None

    @staticmethod
    def from_domain(dto: ClassroomOutDTO):
        return ClassroomOut(
            id=dto.id,
            course=dto.course,
            school=dto.school,
            deleted_at=dto.deleted_at,
        )


class UpdateClassroomIn(Schema):
    course: str

    def to_dto(self) -> UpdateClassroomInDTO:
        return UpdateClassroomInDTO(course=self.course)

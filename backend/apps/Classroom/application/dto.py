from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ClassroomInDTO(BaseModel):
    course: str
    school: UUID


class ClassroomOutDTO(BaseModel):
    id: UUID
    course: str
    school: UUID
    deleted_at: datetime | None

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            course=model.course,
            school=model.school,
            deleted_at=model.deleted_at,
        )


class UpdateClassroomInDTO(BaseModel):
    course: Optional[str] = None

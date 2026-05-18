from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from apps.Classroom.domain.exceptions import (
    ConflictFieldsExceptions,
    FieldISRequiredException,
)


@dataclass
class ClassroomEntity:
    id: UUID = field(default_factory=uuid4)
    course: str = field(default='')
    school: UUID | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def deactive(self):
        if self.deleted_at:
            raise ConflictFieldsExceptions('classroom already deleted')

        self.deleted_at = datetime.now()

    def change_course(self, new_course):
        if not new_course:
            raise FieldISRequiredException('new course is required')

        self.course = new_course

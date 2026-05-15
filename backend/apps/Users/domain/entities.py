from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

from apps.Users.domain.value_objects import UploadFileVO
from core.exceptions import BaseDomainException


@dataclass
class StudentEntity:
    id: UUID = field(default_factory=uuid4)
    user: UUID | None = field(default=None)
    classroom: UUID | None = field(default=None)
    date_birth: date | None = field(default=None)
    photo: Optional[UploadFileVO] | str = None
    vector_facial: List[float] | None = field(default=None)

    def get_embedding(self):
        return self.vector_facial

    def change_classroom(self, new_classroom: UUID):
        if not new_classroom:
            raise BaseDomainException('field new classroom is required')

        self.classroom = new_classroom

    def change_date_birth(self, new_birth: date):
        if not new_birth:
            raise BaseDomainException('new date birth is field required')

        self.date_birth = new_birth


@dataclass
class CoordinatorEntity:
    id: UUID = field(default_factory=uuid4)
    user: UUID | None = field(default=None)
    nucleos_group: UUID | None = field(default=None)


@dataclass
class DirectorEntity:
    id: UUID = field(default_factory=uuid4)
    user: UUID | None = field(default=None)
    school: UUID | None = field(default=None)

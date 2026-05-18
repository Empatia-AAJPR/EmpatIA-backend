from uuid import UUID

from apps.Classroom.application.dto import (
    ClassroomInDTO,
    ClassroomOutDTO,
    UpdateClassroomInDTO,
)
from apps.Classroom.domain.entities import ClassroomEntity
from apps.Classroom.domain.exceptions import (
    ClassroomNotFound,
    ConflictFieldsExceptions,
)
from apps.Classroom.domain.repositories import IClassroomRepository
from apps.Schools.domain.repositories import ISchoolRepository
from core.exceptions import BaseDomainException


class RegisterClassroomUseCase:
    def __init__(
        self, class_repo: IClassroomRepository, school_repo: ISchoolRepository
    ) -> None:
        self.class_repo = class_repo
        self.school_repo = school_repo

    def execute(self, dto: ClassroomInDTO):
        if self.class_repo.exists_course(dto.course):
            raise ConflictFieldsExceptions(
                f'Course {dto.course} already exists'
            )

        school = self.school_repo.find_by_id(dto.school)
        if not school:
            raise BaseDomainException('school not found')

        if school.deleted_at:
            raise BaseDomainException('school not active')

        classroom = ClassroomEntity(course=dto.course, school=school.id)

        self.class_repo.save(classroom)
        return ClassroomOutDTO.from_domain(classroom)


class ResponseClassroomUseCase:
    def __init__(self, class_repo: IClassroomRepository) -> None:
        self.class_repo = class_repo

    def execute(self, id: UUID):
        classroom = self.class_repo.find_by_id(id)
        if not classroom:
            raise ClassroomNotFound('classroom not found')

        return ClassroomOutDTO.from_domain(classroom)


class ListClassroomUseCase:
    def __init__(self, class_repo: IClassroomRepository) -> None:
        self.class_repo = class_repo

    def execute(self, school: UUID):
        classrooms = self.class_repo.list_classrooms_by_school(school)
        if not classrooms:
            return []

        return [
            ClassroomOutDTO.from_domain(classroom) for classroom in classrooms
        ]


class UpdateClassroomUseCase:
    def __init__(self, class_repo: IClassroomRepository) -> None:
        self.class_repo = class_repo

    def execute(self, id: UUID, dto: UpdateClassroomInDTO):
        classroom = self.class_repo.find_by_id(id)
        if not classroom:
            raise ClassroomNotFound('classroom not found')

        if dto.course:
            classroom.change_course(dto.course)

        self.class_repo.save(classroom)

        return ClassroomOutDTO.from_domain(classroom)


class DeactiveClassroomUseCase:
    def __init__(self, class_repo: IClassroomRepository):
        self.class_repo = class_repo

    def execute(self, id: UUID):
        classroom = self.class_repo.find_by_id(id)
        if not classroom:
            raise ClassroomNotFound('classroom not found')

        classroom.deactive()

        self.class_repo.save(classroom)

        return ClassroomOutDTO.from_domain(classroom)

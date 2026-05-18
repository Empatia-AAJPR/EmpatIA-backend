from typing import List
from uuid import UUID

from apps.Classroom.domain.entities import ClassroomEntity
from apps.Classroom.domain.repositories import IClassroomRepository
from apps.Classroom.infrastructure.models import Classroom


class ClassroomRepository(IClassroomRepository):
    def save(self, classroom: ClassroomEntity) -> ClassroomEntity:
        Classroom.objects.update_or_create(
            id=classroom.id,
            defaults={
                'course': classroom.course,
                'school_id': classroom.school,
                'created_at': classroom.created_at,
                'deleted_at': classroom.deleted_at,
            },
        )

        return classroom

    def find_by_id(self, id: UUID) -> ClassroomEntity | None:
        try:
            return self._to_model(Classroom.objects.get(id=id))

        except Classroom.DoesNotExist:
            return None

    def find_by_course(self, course: str) -> ClassroomEntity | None:
        try:
            return self._to_model(Classroom.objects.get(course=course))

        except Classroom.DoesNotExist:
            return None

    def exists_course(self, course: str) -> bool:
        return Classroom.objects.filter(course=course).exists()

    def list_classrooms_by_school(self, school: UUID) -> List[ClassroomEntity]:
        return [
            self._to_model(model)
            for model in Classroom.objects.filter(school=school)
        ]

    def _to_model(self, model: Classroom) -> ClassroomEntity:
        return ClassroomEntity(
            id=model.id,
            course=model.course,
            school=model.school.id,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
        )

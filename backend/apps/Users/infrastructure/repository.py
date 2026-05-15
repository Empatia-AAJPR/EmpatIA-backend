from uuid import UUID

from apps.Users.domain.entities import (
    CoordinatorEntity,
    DirectorEntity,
    StudentEntity,
)
from apps.Users.domain.repositories import (
    ICoordinatorRepository,
    IDirectorRepository,
    IStudentRepository,
)
from apps.Users.domain.value_objects import UploadFileVO
from apps.Users.infrastructure.models import Coordinator, Director, Student


class StudentRepository(IStudentRepository):
    def save(self, student: StudentEntity) -> StudentEntity:
        Student.objects.update_or_create(
            id=student.id,
            defaults={
                'user_id': student.user,
                'classroom_id': student.classroom,
                'date_birth': student.date_birth,
                'photo': student.photo,
                'vector_facial': student.vector_facial,
            },
        )

        return student

    def find_by_id(self, id: UUID) -> StudentEntity | None:
        try:
            return self._to_entity(Student.objects.get(id=id))

        except Student.DoesNotExist:
            return None

    def _to_entity(self, model: Student) -> StudentEntity:
        return StudentEntity(
            id=model.id,
            user=model.user.id,
            classroom=model.classroom.id if model.classroom else None,
            date_birth=model.date_birth,
            photo=model.photo.url,
        )


class CoordinatorRepository(ICoordinatorRepository):
    def save(self, coordinator: CoordinatorEntity) -> CoordinatorEntity:
        Coordinator.objects.update_or_create(
            id=coordinator.id,
            defaults={
                'user_id': coordinator.user,
                'nucleos_group_id': coordinator.nucleos_group,
            },
        )

        return coordinator

    def find_by_id(self, id: UUID) -> CoordinatorEntity | None:
        try:
            return self._to_entity(Coordinator.objects.get(id=id))

        except Coordinator.DoesNotExist:
            return None

    def _to_entity(self, model: Coordinator) -> CoordinatorEntity:
        return CoordinatorEntity(
            id=model.id, user=model.user.id, nucleos_group=model.nucleos_group
        )


class DirectorRepository(IDirectorRepository):
    def save(self, director: DirectorEntity) -> DirectorEntity:
        Director.objects.update_or_create(
            id=director.id,
            defaults={'user_id': director.user, 'school_id': director.school},
        )

        return director

    def find_by_id(self, id: UUID) -> DirectorEntity | None:
        try:
            return self._to_entity(Director.objects.get(id=id))

        except Director.DoesNotExist:
            return None

    def _to_entity(self, model: Director) -> DirectorEntity:
        return DirectorEntity(
            id=model.id,
            user=model.user.id,
            school=model.school.id if model.school else None,
        )

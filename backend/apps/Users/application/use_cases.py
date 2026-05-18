from uuid import UUID

from apps.Accounts.domain.entities import UserEntity
from apps.Accounts.domain.repositories import IHashService, IUserRepository
from apps.Accounts.domain.rules import UserRules
from apps.Users.application.dto import (
    CoordinatorInDTO,
    DirectorInDTO,
    StudentInDTO,
    StudentUpdateDTO,
)
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
from apps.Users.domain.servicies import (
    ICoordinatorQueryService,
    IDirectorQueryService,
    IStudentQueryService,
)
from apps.Users.infrastructure.adapters.interface_adapter import (
    IImageFileAdapter,
)
from apps.Accounts.domain.exceptions import ConflictFieldException
from apps.Users.infrastructure.exceptions import (
    ConflictEntityException,
    UserNotFoundException,
)
from apps.Classroom.domain.repositories import IClassroomRepository
from apps.Schools.domain.repositories import ISchoolRepository
from core.exceptions import BaseDomainException


class RegisterStudentUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        hash_service: IHashService,
        student_repo: IStudentRepository,
        query_service: IStudentQueryService,
        file_adapter: IImageFileAdapter,
        class_repo: IClassroomRepository,
    ) -> None:
        self.user_repo = user_repo
        self.hash_service = hash_service
        self.student_repo = student_repo
        self.query_service = query_service
        self.file_adapter = file_adapter
        self.class_repo = class_repo

    def execute(self, dto: StudentInDTO):
        if self.user_repo.exists_email(dto.email):
            raise ConflictFieldException('email already register')

        classroom = self.class_repo.find_by_id(dto.classroom)
        if not classroom:
            raise BaseDomainException('classroom not found')

        if classroom.deleted_at:
            raise BaseDomainException('classroom not active')

        password_hash = self.hash_service.hash_password(dto.password)

        file_img = None
        if dto.photo:
            file_img = self.file_adapter.file_upload(dto.photo)

        user = UserEntity(
            name=dto.name,
            email=dto.email,
            password=password_hash,
            rule=UserRules.STUDENT,
        )

        self.user_repo.save(user)

        student = StudentEntity(
            user=user.id,
            classroom=dto.classroom,
            date_birth=dto.date_birth,
            photo=file_img,
        )

        self.student_repo.save(student)

        query_user = self.query_service.get_by_id(student.id)
        if not query_user:
            raise BaseDomainException('error in request user student')

        return query_user


class ResponseStudentByIDUseCase:
    def __init__(self, query_service: IStudentQueryService) -> None:
        self.query_service = query_service

    def execute(self, id: UUID):
        query = self.query_service.get_by_id(id)
        if not query:
            raise UserNotFoundException('student not found')

        return query


class UpdateStudentUseCase:
    def __init__(
        self,
        student_repo: IStudentRepository,
        query_service: IStudentQueryService,
        hash_service: IHashService,
    ) -> None:
        self.student_repo = student_repo
        self.query_service = query_service
        self.hash_service = hash_service

    def execute(self, id: UUID, dto: StudentUpdateDTO):
        student = self.student_repo.find_by_id(id)
        if not student:
            raise UserNotFoundException('student not found')

        if dto.classroom:
            student.change_classroom(dto.classroom)

        if dto.date_birth:
            student.change_date_birth(dto.date_birth)

        self.student_repo.save(student)

        query = self.query_service.get_by_id(student.id)
        if not query:
            raise BaseDomainException('user account student not found')

        return query


class DeactiveStudentUseCase:
    def __init__(
        self,
        student_repo: IStudentRepository,
        user_repo: IUserRepository,
        query_service: IStudentQueryService,
    ) -> None:
        self.student_repo = student_repo
        self.user_repo = user_repo
        self.query_service = query_service

    def execute(self, id: UUID):
        student = self.student_repo.find_by_id(id)
        if not student:
            raise UserNotFoundException('student not found')

        if not student.user:
            raise BaseDomainException('student has no user vinculate')

        user = self.user_repo.find_by_id(student.user)

        if not user:
            raise BaseDomainException('user not found')

        user.deactive_user()

        self.user_repo.save(user)

        query_user = self.query_service.get_by_id(student.id)

        if not query_user:
            raise UserNotFoundException('user account student not found')

        return query_user


class RegisterCoordinatorUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        coordinator_repo: ICoordinatorRepository,
        hash_service: IHashService,
        query_service: ICoordinatorQueryService,
        school_repo: ISchoolRepository,
    ) -> None:
        self.user_repo = user_repo
        self.coordinator_repo = coordinator_repo
        self.hash_service = hash_service
        self.query_service = query_service
        self.school_repo = school_repo

    def execute(self, dto: CoordinatorInDTO):
        if self.user_repo.exists_email(dto.email):
            raise ConflictEntityException('email already exists')

        school = self.school_repo.find_by_id(dto.school)
        if not school:
            raise BaseDomainException('school not found')

        if school.deleted_at:
            raise BaseDomainException('school not active')

        password_hash = self.hash_service.hash_password(dto.password)

        user = UserEntity(
            name=dto.name,
            email=dto.email,
            password=password_hash,
            rule=UserRules.COORDINATOR,
        )
        self.user_repo.save(user)

        coordinator = CoordinatorEntity(user=user.id, school=dto.school)
        self.coordinator_repo.save(coordinator)

        query = self.query_service.get_by_id(coordinator.id)
        if not query:
            raise BaseDomainException('student not found')

        return query


class ResponseCoordinatorByIDUseCase:
    def __init__(self, query_service: ICoordinatorQueryService) -> None:
        self.query_service = query_service

    def execute(self, id: UUID):
        query = self.query_service.get_by_id(id)
        if not query:
            raise UserNotFoundException(
                'coordinator or association on coordinator and user has no atribute'
            )

        return query


class DeactiveCoordinatorUseCase:
    def __init__(
        self,
        coordinator_repo: ICoordinatorRepository,
        user_repo: IUserRepository,
        query_service: ICoordinatorQueryService,
    ) -> None:
        self.coordinator_repo = coordinator_repo
        self.user_repo = user_repo
        self.query_service = query_service

    def execute(self, id: UUID):
        coordinator = self.coordinator_repo.find_by_id(id)
        if not coordinator:
            raise UserNotFoundException('coordinator not found')

        if not coordinator.user:
            raise BaseDomainException('coordinator has no user')

        user = self.user_repo.find_by_id(coordinator.user)

        if not user:
            raise UserNotFoundException('user not found')

        user.deactive_user()
        self.user_repo.save(user)

        query_user = self.query_service.get_by_id(coordinator.id)

        if not query_user:
            raise UserNotFoundException('user account coordinator not found')

        return query_user


class RegisterDirectorUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        director_repo: IDirectorRepository,
        hash_service: IHashService,
        query_service: IDirectorQueryService,
        school_repo: ISchoolRepository,
    ) -> None:
        self.user_repo = user_repo
        self.director_repo = director_repo
        self.hash_service = hash_service
        self.query_service = query_service
        self.school_repo = school_repo

    def execute(self, dto: DirectorInDTO):
        if self.user_repo.exists_email(dto.email):
            raise ConflictFieldException('email already register')

        school = self.school_repo.find_by_id(dto.school)

        if not school:
            raise BaseDomainException('school not found')

        if school.deleted_at:
            raise BaseDomainException('school not active')

        password_hash = self.hash_service.hash_password(dto.password)

        user = UserEntity(
            name=dto.name,
            email=dto.email,
            password=password_hash,
            rule=UserRules.DIRECTOR,
        )

        self.user_repo.save(user)

        director = DirectorEntity(user=user.id, school=dto.school)
        self.director_repo.save(director)

        query_user = self.query_service.get_by_id(director.id)
        if not query_user:
            raise UserNotFoundException('user account director not found')

        return query_user


class ResponseDirectorUseCase:
    def __init__(self, query_service: IDirectorQueryService) -> None:
        self.query_service = query_service

    def execute(self, id: UUID):
        director = self.query_service.get_by_id(id)
        if not director:
            raise UserNotFoundException('director not found')

        return director


class DeactiveDirectorUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        director_repo: IDirectorRepository,
        query_service: IDirectorQueryService,
    ) -> None:
        self.user_repo = user_repo
        self.director_repo = director_repo
        self.query_service = query_service

    def execute(self, id: UUID):
        director = self.director_repo.find_by_id(id)
        if not director:
            raise UserNotFoundException('director not found')

        if not director.user:
            raise BaseDomainException('director has no user atribute')

        user = self.user_repo.find_by_id(director.user)
        if not user:
            raise UserNotFoundException('user not found')

        user.deactive_user()
        self.user_repo.save(user)

        query_user = self.query_service.get_by_id(director.id)
        if not query_user:
            raise BaseDomainException('user account director not found')

        return query_user

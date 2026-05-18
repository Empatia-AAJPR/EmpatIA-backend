from dependency_injector import containers, providers

from apps.Accounts.domain.services import HashService
from apps.Accounts.infrastructure.repository import UserRepository
from apps.Users.application.use_cases import (
    DeactiveCoordinatorUseCase,
    DeactiveDirectorUseCase,
    DeactiveStudentUseCase,
    RegisterCoordinatorUseCase,
    RegisterDirectorUseCase,
    RegisterStudentUseCase,
    ResponseCoordinatorByIDUseCase,
    ResponseDirectorUseCase,
    ResponseStudentByIDUseCase,
    UpdateStudentUseCase,
)
from apps.Users.infrastructure.adapters.file_adapter import ImageFileAdapter
from apps.Users.infrastructure.repository import (
    CoordinatorRepository,
    DirectorRepository,
    StudentRepository,
)
from apps.Users.infrastructure.services import (
    CoordinatorQueryService,
    DirectorQueryService,
    StudentQueryService,
)
from apps.Classroom.infrastructure.repository import ClassroomRepository
from apps.Schools.infrastructure.repository import SchoolRepository


class UsersContainer(containers.DeclarativeContainer):
    user_repo = providers.Factory(UserRepository)

    student_repo = providers.Factory(StudentRepository)

    coordinator_repo = providers.Factory(CoordinatorRepository)

    director_repo = providers.Factory(DirectorRepository)

    hash_service = providers.Factory(HashService)

    query_student = providers.Factory(StudentQueryService)

    query_coordinator = providers.Factory(CoordinatorQueryService)

    query_director = providers.Factory(DirectorQueryService)

    file_adapter = providers.Factory(ImageFileAdapter)

    class_repo = providers.Factory(ClassroomRepository)

    school_repo = providers.Factory(SchoolRepository)

    register_student_use_case = providers.Factory(
        RegisterStudentUseCase,
        user_repo=user_repo,
        hash_service=hash_service,
        student_repo=student_repo,
        query_service=query_student,
        file_adapter=file_adapter,
        class_repo=class_repo,
    )

    response_student_use_case = providers.Factory(
        ResponseStudentByIDUseCase, query_service=query_student
    )

    update_student_use_case = providers.Factory(
        UpdateStudentUseCase,
        student_repo=student_repo,
        query_service=query_student,
        hash_service=hash_service,
    )

    deactive_student_use_case = providers.Factory(
        DeactiveStudentUseCase,
        student_repo=student_repo,
        user_repo=user_repo,
        query_service=query_student,
    )

    register_coordinator_use_case = providers.Factory(
        RegisterCoordinatorUseCase,
        user_repo=user_repo,
        coordinator_repo=coordinator_repo,
        hash_service=hash_service,
        query_service=query_coordinator,
        school_repo=school_repo,
    )

    response_coordinator_use_case = providers.Factory(
        ResponseCoordinatorByIDUseCase, query_service=query_coordinator
    )

    deactive_coordinator_use_case = providers.Factory(
        DeactiveCoordinatorUseCase,
        coordinator_repo=coordinator_repo,
        user_repo=user_repo,
        query_service=query_coordinator,
    )

    register_director_use_case = providers.Factory(
        RegisterDirectorUseCase,
        user_repo=user_repo,
        director_repo=director_repo,
        hash_service=hash_service,
        query_service=query_director,
        school_repo=school_repo,
    )

    response_director_use_case = providers.Factory(
        ResponseDirectorUseCase, query_service=query_director
    )

    deactive_director_use_case = providers.Factory(
        DeactiveDirectorUseCase,
        user_repo=user_repo,
        director_repo=director_repo,
        query_service=query_director,
    )

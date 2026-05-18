from dependency_injector import containers, providers

from apps.Classroom.application.use_cases import (
    DeactiveClassroomUseCase,
    ListClassroomUseCase,
    RegisterClassroomUseCase,
    ResponseClassroomUseCase,
    UpdateClassroomUseCase,
)
from apps.Classroom.infrastructure.repository import ClassroomRepository
from apps.Schools.infrastructure.repository import SchoolRepository


class ClassroomContainer(containers.DeclarativeContainer):
    class_repo = providers.Factory(ClassroomRepository)

    school_repo = providers.Factory(SchoolRepository)

    register_classroom_use_case = providers.Factory(
        RegisterClassroomUseCase,
        class_repo=class_repo,
        school_repo=school_repo,
    )

    response_classroom_by_id_use_case = providers.Factory(
        ResponseClassroomUseCase, class_repo=class_repo
    )

    list_classroom_by_school = providers.Factory(
        ListClassroomUseCase, class_repo=class_repo
    )

    update_classroom_use_case = providers.Factory(
        UpdateClassroomUseCase, class_repo=class_repo
    )

    deactive_classroom_use_case = providers.Factory(
        DeactiveClassroomUseCase, class_repo=class_repo
    )

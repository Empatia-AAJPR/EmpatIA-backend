from dependency_injector import containers, providers

from apps.Schools.application.use_cases import (
    DeactiveNucleosGroupUseCase,
    DeactiveSchoolUseCase,
    RegisterNucleosGroupUseCase,
    RegisterSchoolUseCase,
    ResponseNucleosGroupUseCase,
    ResponseSchoolByCNPJUseCase,
    ResponseSchoolByIDUseCase,
    UpdateNucleosGroupUseCase,
    UpdateSchoolUseCase,
)
from apps.Schools.infrastructure.adapters.file_adapters import ImageFileAdapter
from apps.Schools.infrastructure.repository import (
    NucleosGroupRepository,
    SchoolRepository,
)


class SchoolsContainer(containers.DeclarativeContainer):
    school_repo = providers.Factory(SchoolRepository)

    file_adapter = providers.Factory(ImageFileAdapter)

    ng_repo = providers.Factory(NucleosGroupRepository)

    register_school_use_case = providers.Factory(
        RegisterSchoolUseCase,
        school_repo=school_repo,
        file_adapter=file_adapter,
    )

    response_school_by_id_use_case = providers.Factory(
        ResponseSchoolByIDUseCase, school_repo=school_repo
    )

    response_school_by_cnpj_use_case = providers.Factory(
        ResponseSchoolByCNPJUseCase, school_repo=school_repo
    )

    update_school_use_case = providers.Factory(
        UpdateSchoolUseCase, school_repo=school_repo
    )

    dective_school_use_case = providers.Factory(
        DeactiveSchoolUseCase, school_repo=school_repo
    )

    register_nucleos_group_use_case = providers.Factory(
        RegisterNucleosGroupUseCase, ng_repo=ng_repo, school_repo=school_repo
    )

    response_nucleos_group_use_case = providers.Factory(
        ResponseNucleosGroupUseCase, ng_repo=ng_repo
    )

    update_nucleos_group_use_case = providers.Factory(
        UpdateNucleosGroupUseCase, ng_repo=ng_repo
    )

    deative_nucleos_group_use_case = providers.Factory(
        DeactiveNucleosGroupUseCase, ng_repo=ng_repo
    )

from typing import Annotated, Optional
from uuid import UUID

from ninja import File, Form, Router, UploadedFile

from apps.Schools.api.dependencies import SchoolsContainer
from apps.Schools.api.schemas import NucleosGroupIn, NucleosGroupOut, SchoolIn, SchoolOut, UpdateNucleosGroupIn, UpdateSchoolIn

from django.db import transaction

from apps.Schools.application.dto import SchoolInDTO, UpdateSchoolInDTO
from apps.Schools.domain.value_objects import CNPJ
from apps.Users.domain.value_objects import UploadFileVO


router_schools = Router()

router_nucleos_group = Router()

container = SchoolsContainer()


@router_schools.post('/', response={201: SchoolOut})
@transaction.atomic
def register_schools(request, data: Form[SchoolIn], file: File[UploadedFile]):

    logo = UploadFileVO(
        name=file.name,
        content=file.read(),
        content_type=file.content_type,
        size=file.size,
    )

    dto = SchoolInDTO(
        name=data.name, cnpj=CNPJ(data.cnpj), gre=data.gre, logo=logo
    )

    use_case = container.register_school_use_case()

    school = use_case.execute(dto)

    return 201, SchoolOut.from_domain(school)


@router_schools.get('/{id}', response={200: SchoolOut})
def response_schools_by_id(request, id: UUID):
    use_case = container.response_school_by_id_use_case()

    school = use_case.execute(id)

    return 200, SchoolOut.from_domain(school)


@router_schools.patch('/{id}', response={200: SchoolOut})
@transaction.atomic
def update_school(
    request,
    id: UUID,
    data: UpdateSchoolIn,
):
    dto = data.to_dto()

    use_case = container.update_school_use_case()

    school = use_case.execute(id, dto)

    return 200, SchoolOut.from_domain(school)


@router_schools.delete('/{id}', response={200: SchoolOut})
@transaction.atomic
def deactive_school(request, id: UUID):
    use_case = container.dective_school_use_case()

    school = use_case.execute(id)

    return 200, SchoolOut.from_domain(school)


@router_nucleos_group.post('/', response={201: NucleosGroupOut})
@transaction.atomic
def register_nucleos_group(request, data: NucleosGroupIn):
    dto = data.to_dto()

    use_case = container.register_nucleos_group_use_case()

    nucleos_group = use_case.execute(dto)

    return 201, NucleosGroupOut.from_domain(nucleos_group)

@router_nucleos_group.get('/{id}', response={200: NucleosGroupOut})
def response_nucleos_group(request, id: UUID):
    use_case = container.response_nucleos_group_use_case()

    nucleos_group = use_case.execute(id)

    return 200, NucleosGroupOut.from_domain(nucleos_group)

@router_nucleos_group.patch('/{id}', response={200: NucleosGroupOut})
@transaction.atomic
def update_nucleos_group(request, id: UUID, data: UpdateNucleosGroupIn):
    dto = data.to_dto()

    use_case = container.update_nucleos_group_use_case()

    nucleos_group = use_case.execute(id, dto)

    return 200, NucleosGroupOut.from_domain(nucleos_group)

@router_nucleos_group.delete('/{id}', response={200: NucleosGroupOut})
@transaction.atomic
def deactive_nucleos_group(request, id: UUID):
    use_case = container.deative_nucleos_group_use_case()

    nucleos_group = use_case.execute(id)

    return 200, NucleosGroupOut.from_domain(nucleos_group)

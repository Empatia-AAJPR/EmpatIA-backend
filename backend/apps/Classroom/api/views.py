from typing import List
from uuid import UUID

from ninja import Router

from django.db import transaction

from apps.Classroom.api.dependencies import ClassroomContainer
from apps.Classroom.api.schemas import (
    ClassroomIn,
    ClassroomOut,
    UpdateClassroomIn,
)
from apps.Accounts.api.permissions import is_authorized
from apps.Accounts.api.auth import JWTAuth


router_classroom = Router(auth=JWTAuth())

container = ClassroomContainer()


@router_classroom.post('/', response={201: ClassroomOut})
@transaction.atomic
def register_classroom(request, data: ClassroomIn):

    is_authorized(request)

    dto = data.to_dto()

    use_case = container.register_classroom_use_case()

    classroom = use_case.execute(dto)

    return 201, ClassroomOut.from_domain(classroom)


@router_classroom.get('/school/{id}', response={200: List[ClassroomOut]})
def list_classroom_by_school(request, id: UUID):

    is_authorized(request)

    use_case = container.list_classroom_by_school()

    classrooms = use_case.execute(id)

    return 200, [ClassroomOut.from_domain(dtos) for dtos in classrooms]


@router_classroom.get('/{id}', response={200: ClassroomOut})
def response_classroom_by_id(request, id: UUID):

    is_authorized(request)

    use_case = container.response_classroom_by_id_use_case()

    classroom = use_case.execute(id)

    return 200, ClassroomOut.from_domain(classroom)


@router_classroom.patch('/{id}', response={200: ClassroomOut})
@transaction.atomic
def update_classroom(request, id: UUID, data: UpdateClassroomIn):

    is_authorized(request)

    dto = data.to_dto()

    use_case = container.update_classroom_use_case()

    classroom = use_case.execute(id, dto)

    return 200, ClassroomOut.from_domain(classroom)


@router_classroom.delete('/{id}', response={200: ClassroomOut})
@transaction.atomic
def deactive_classroom(request, id: UUID):

    is_authorized(request)

    use_case = container.deactive_classroom_use_case()

    classroom = use_case.execute(id)

    return 200, ClassroomOut.from_domain(classroom)

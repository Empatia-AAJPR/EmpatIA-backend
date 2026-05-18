from uuid import UUID

from ninja import File, Form, Router, UploadedFile

from django.db import transaction

from apps.Users.api.dependencies import UsersContainer
from apps.Users.api.schemas import (
    CoordinatorIn,
    CoordinatorOut,
    DirectorIn,
    DirectorOut,
    StudentIn,
    StudentOut,
    UpdateStudentIn,
)
from apps.Users.application.dto import StudentInDTO
from apps.Users.domain.value_objects import UploadFileVO
from apps.Accounts.api.permissions import is_authorized
from apps.Accounts.api.auth import JWTAuth


router_student = Router(auth=JWTAuth())

router_coordinator = Router()

router_director = Router()

container = UsersContainer()


@router_student.post('/', response={201: StudentOut})
@transaction.atomic
def register_student(request, data: Form[StudentIn], img: File[UploadedFile]):

    is_authorized(request)

    photo = UploadFileVO(
        name=img.name,
        content=img.read(),
        content_type=img.content_type,
        size=img.size,
    )

    dto = StudentInDTO(
        name=data.name,
        email=data.email,
        password=data.password,
        classroom=data.classroom,
        date_birth=data.date_birth,
        photo=photo,
    )

    use_case = container.register_student_use_case()

    student = use_case.execute(dto)

    return 201, StudentOut.from_domain(student)


@router_student.get('/{id}', response={200: StudentOut})
def response_student(request, id: UUID):

    is_authorized(request)

    use_case = container.response_student_use_case()

    student = use_case.execute(id)

    return 200, student


@router_student.patch('/{id}', response={200: StudentOut})
@transaction.atomic
def update_student(request, id: UUID, data: UpdateStudentIn):

    is_authorized(request)

    dto = data.to_dto()

    use_case = container.update_student_use_case()

    student = use_case.execute(id, dto)

    return 200, StudentOut.from_domain(student)


@router_student.delete('/{id}', response={200: StudentOut})
@transaction.atomic
def deactive_student(request, id: UUID):

    is_authorized(request)

    use_case = container.deactive_student_use_case()

    student = use_case.execute(id)

    return 200, student


@router_coordinator.post('/', response={201: CoordinatorOut})
@transaction.atomic
def register_coordinator(request, data: CoordinatorIn):
    dto = data.to_dto()

    use_case = container.register_coordinator_use_case()

    coordinator = use_case.execute(dto)

    return 201, CoordinatorOut.from_domain(coordinator)


@router_coordinator.get('/{id}', response={200: CoordinatorOut})
def response_coordinator(request, id: UUID):
    use_case = container.response_coordinator_use_case()

    coordinator = use_case.execute(id)

    return 200, CoordinatorOut.from_domain(coordinator)


@router_coordinator.delete('/{id}', response={200: CoordinatorOut})
@transaction.atomic
def deactive_coordinator(request, id: UUID):
    use_case = container.deactive_coordinator_use_case()

    coordinator = use_case.execute(id)

    return 200, CoordinatorOut.from_domain(coordinator)


@router_director.post('/', response={201: DirectorOut})
@transaction.atomic
def register_director(request, data: DirectorIn):
    dto = data.to_dto()

    use_case = container.register_director_use_case()

    director = use_case.execute(dto)

    return 201, DirectorOut.from_domain(director)


@router_director.get('/{id}', response={200: DirectorOut})
def response_director(request, id: UUID):
    use_case = container.response_director_use_case()

    director = use_case.execute(id)

    return 200, DirectorOut.from_domain(director)


@router_director.delete('/{id}', response={200: DirectorOut})
@transaction.atomic
def deactive_director(request, id: UUID):
    use_case = container.deactive_director_use_case()

    director = use_case.execute(id)

    return 200, DirectorOut.from_domain(director)

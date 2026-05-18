from uuid import UUID

from ninja import Router

from django.db import transaction
from pydantic import EmailStr

from apps.Accounts.api.auth import JWTAuth
from apps.Accounts.api.dependencies import AccountsContainer
from apps.Accounts.api.permissions import is_authorized
from apps.Accounts.api.schemas import (
    LoginIn,
    TokenOut,
    UserIn,
    UserOut,
    UserUpdateIn,
)

router = Router(auth=JWTAuth())

auth_router = Router()

container = AccountsContainer()


@router.post('/', response={201: UserOut})
@transaction.atomic
def register_user(request, data: UserIn):

    is_authorized(request)

    dto = data.to_dto()

    use_case = container.register_user_use_case()

    user = use_case.execute(dto)

    return 201, UserOut.from_domain(user)


@router.get('/{id}', response={200: UserOut})
def response_user_by_id(request, id: UUID):

    is_authorized(request)

    use_case = container.response_user_by_id_use_case()

    user = use_case.execute(id)

    return 200, UserOut.from_domain(user)


@router.get('/', response={200: UserOut})
def response_user_by_email(request, email: EmailStr):

    is_authorized(request)

    use_case = container.response_user_by_email_use_case()

    user = use_case.execute(email)

    return 200, UserOut.from_domain(user)


@router.patch('/{id}', response={200: UserOut})
@transaction.atomic
def update_user(request, id: UUID, data: UserUpdateIn):

    is_authorized(request)

    dto = data.to_dto()

    use_case = container.update_user_use_case()

    user = use_case.execute(id=id, dto=dto)

    return 200, UserOut.from_domain(user)


@router.delete('/{id}', response={200: UserOut}, auth=JWTAuth())
@transaction.atomic
def deactive_user(request, id: UUID):

    is_authorized(request)

    use_case = container.deactive_user_use_case()

    user = use_case.execute(id)

    return 200, UserOut.from_domain(user)


@auth_router.post('/login', response={201: TokenOut})
@transaction.atomic
def login_user(request, data: LoginIn):
    dto = data.to_dto()

    use_case = container.login_user_use_case()

    tokens = use_case.execute(dto)

    return 201, TokenOut.from_domain(tokens)


@auth_router.get('/me', response={200: UserOut}, auth=JWTAuth())
def return_me(request):
    user_id = request.auth['sub']

    use_case = container.response_user_by_id_use_case()

    user = use_case.execute(user_id)

    return 200, UserOut.from_domain(user)

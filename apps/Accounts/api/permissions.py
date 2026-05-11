from uuid import UUID

from ninja.errors import HttpError

from apps.Accounts.domain.rules import UserRules


def is_same_user(request, id: UUID):
    current_user = request.auth['sub']

    if current_user != id:
        raise HttpError(403, "Forbidden")


def is_admin_user(request):
    current_rule = request.auth['rule']

    if current_rule != UserRules.ADMIN:
        raise HttpError(403, "Forbidden")


def is_same_user_and_admin(request, id: UUID):
    current_rule = request.auth['rule']
    current_id = request.auth['sub']

    if current_rule != UserRules.ADMIN or current_id != id:
        raise HttpError(403, "Forbidden")


def is_authorized(request):
    current_rule = request.auth['rule']

    if current_rule not in [UserRules.COORDINATOR, UserRules.DIRECTOR, UserRules.ADMIN]:
        raise HttpError(403, "Forbidden")

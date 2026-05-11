from dependency_injector import containers, providers

from apps.Accounts.application.use_cases import (
    DeactiveUserUseCase,
    ListUsersByRuleUseCase,
    LoginUserUseCase,
    RegisterUserUseCase,
    ResponseUserByEmailUseCase,
    ResponseUserByIDUseCase,
    UpdateUserUseCase,
)
from apps.Accounts.domain.services import HashService, TokenService
from apps.Accounts.infrastructure.repository import (
    TokenRepository,
    UserRepository,
)


class AccountsContainer(containers.DeclarativeContainer):
    user_repo = providers.Factory(UserRepository)

    hash_service = providers.Factory(HashService)

    token_service = providers.Factory(TokenService)

    token_repo = providers.Factory(TokenRepository)

    register_user_use_case = providers.Factory(
        RegisterUserUseCase, user_repo=user_repo, hash_service=hash_service
    )

    response_user_by_id_use_case = providers.Factory(
        ResponseUserByIDUseCase, user_repo=user_repo
    )

    response_user_by_email_use_case = providers.Factory(
        ResponseUserByEmailUseCase, user_repo=user_repo
    )

    list_users_by_rule_use_case = providers.Factory(
        ListUsersByRuleUseCase, user_repo=user_repo
    )

    update_user_use_case = providers.Factory(
        UpdateUserUseCase, user_repo=user_repo, hash_service=hash_service
    )

    deactive_user_use_case = providers.Factory(
        DeactiveUserUseCase, user_repo=user_repo
    )

    login_user_use_case = providers.Factory(
        LoginUserUseCase,
        user_repo=user_repo,
        token_service=token_service,
        hash_service=hash_service,
        token_repo=token_repo,
    )

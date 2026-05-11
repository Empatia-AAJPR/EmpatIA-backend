from uuid import UUID

from apps.Accounts.application.dto import (
    LoginInDTO,
    RefreshTokenOutDTO,
    UserInDTO,
    UserOutDTO,
    UserUpdateDTO,
)
from apps.Accounts.domain.entities import UserEntity
from apps.Accounts.domain.exceptions import (
    ConflictFieldException,
    NotFoundException,
    UserNotActiveException,
)
from apps.Accounts.domain.repositories import (
    IHashService,
    ITokenRepository,
    ITokenServices,
    IUserRepository,
)
from apps.Accounts.domain.rules import UserRules


class RegisterUserUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        hash_service: IHashService,
    ) -> None:
        self.user_repo = user_repo
        self.hash_service = hash_service

    def execute(self, dto: UserInDTO):
        if self.user_repo.exists_email(dto.email):
            raise ConflictFieldException('email already exists')

        password_hash = self.hash_service.hash_password(dto.password)

        user = UserEntity(
            name=dto.name,
            email=dto.email,
            password=password_hash,
            rule=dto.rule,
        )
        self.user_repo.save(user)

        return UserOutDTO.from_domain(user)


class ResponseUserByIDUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, id: UUID):
        user = self.user_repo.find_by_id(id)

        if not user:
            raise NotFoundException('not found user')

        return UserOutDTO.from_domain(user)


class ResponseUserByEmailUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, email: str):
        user = self.user_repo.find_by_email(email)
        if not user:
            raise NotFoundException('not found user')

        return UserOutDTO.from_domain(user)


class ListUsersByRuleUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, rule: UserRules):
        return self.user_repo.list_users_by_rule(rule)


class UpdateUserUseCase:
    def __init__(
        self, user_repo: IUserRepository, hash_service: IHashService
    ) -> None:
        self.user_repo = user_repo
        self.hash_service = hash_service

    def execute(self, id: UUID, dto: UserUpdateDTO):
        user = self.user_repo.find_by_id(id)
        if not user:
            raise NotFoundException('not found user')
        
        if dto.name:
            user.change_name(dto.name)

        if dto.email:
            user.change_email(dto.email)

        if dto.password:
            password = self.hash_service.hash_password(dto.password)
            user.change_password(password)

        if dto.rule:
            user.change_rule(dto.rule)

        self.user_repo.save(user)

        return UserOutDTO.from_domain(user)


class DeactiveUserUseCase:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def execute(self, id: UUID):
        user = self.user_repo.find_by_id(id)
        if not user:
            raise NotFoundException('not found user')

        user.deactive_user()

        self.user_repo.save(user)

        return UserOutDTO.from_domain(user)


class LoginUserUseCase:
    def __init__(
        self,
        user_repo: IUserRepository,
        token_service: ITokenServices,
        hash_service: IHashService,
        token_repo: ITokenRepository,
    ) -> None:
        self.user_repo = user_repo
        self.token_service = token_service
        self.hash_service = hash_service
        self.token_repo = token_repo

    def execute(self, dto: LoginInDTO):
        user = self.user_repo.find_by_email(dto.email)
        if not user:
            raise NotFoundException('not found user')

        if not user.is_active:
            raise UserNotActiveException('user not is active')

        if not self.hash_service.verify_password(
            raw_password=dto.password, hash_password=user.password
        ):
            raise ConflictFieldException('email or password incorrect')

        access_token = self.token_service.generate_access_token(user)

        (raw_token, token_entity) = self.token_service.generate_refresh_token(
            user
        )

        self.token_repo.save(token_entity)

        return RefreshTokenOutDTO.from_domain(access_token, raw_token)

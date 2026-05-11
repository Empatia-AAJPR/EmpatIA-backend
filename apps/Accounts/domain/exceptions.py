from core.exceptions import BaseDomainException


class FieldRequiredException(BaseDomainException):
    pass


class ConflictFieldException(BaseDomainException):
    pass


class TokenUserException(BaseDomainException):
    pass


class NotFoundException(BaseDomainException):
    pass


class UserNotActiveException(BaseDomainException):
    pass

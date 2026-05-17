from core.exceptions import BaseDomainException


class SchoolNotFoundException(BaseDomainException):
    pass


class NucleosGroupNotFoundException(BaseDomainException):
    pass


class ConflictFieldsException(BaseDomainException):
    pass

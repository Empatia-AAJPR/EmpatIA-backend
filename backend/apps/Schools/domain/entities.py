from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

from apps.Schools.domain.value_objects import CNPJ
from core.exceptions import BaseDomainException


@dataclass
class SchoolEntity:
    id: UUID = field(default_factory=uuid4)
    name: str = field(default='')
    cnpj: CNPJ = field(default_factory=lambda: CNPJ(''))
    logo: str | None = field(default=None)
    gre: str = field(default='')
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def deactive(self):
        if self.deleted_at:
            raise BaseDomainException('school already deleted')

        self.deleted_at = datetime.now()

    def change_name(self, new_name: str):
        if not new_name:
            raise BaseDomainException('new name is required')

        self.name = new_name

    def change_cnpj(self, new_cnpj: CNPJ):
        if not new_cnpj:
            raise BaseDomainException('new cnpj is required')

        self.cnpj = new_cnpj

    def change_gre(self, new_gre: str):
        if not new_gre:
            raise BaseDomainException('new gre is required')

        self.gre = new_gre

    def change_logo(self, new_logo: str):
        if not new_logo:
            raise BaseDomainException('new logo is required')

        self.logo = new_logo


@dataclass
class NucleosGroupEntity:
    id: UUID = field(default_factory=uuid4)
    name: str = field(default='')
    school: UUID | None = field(default=None)
    created_at: datetime = field(default_factory=datetime.now)
    deleted_at: datetime | None = field(default=None)

    def deactive(self):
        if self.deleted_at:
            raise BaseDomainException('school already deleted')

        self.deleted_at = datetime.now()

    def change_name(self, new_name: str):
        if not new_name:
            raise BaseDomainException('new name is required')

        self.name = new_name

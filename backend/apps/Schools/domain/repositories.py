from abc import ABC, abstractmethod
from uuid import UUID

from apps.Schools.domain.entities import NucleosGroupEntity, SchoolEntity
from apps.Schools.domain.value_objects import CNPJ


class ISchoolRepository(ABC):
    @abstractmethod
    def save(self, school: SchoolEntity) -> SchoolEntity | None:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> SchoolEntity | None:
        ...

    @abstractmethod
    def find_by_cnpj(self, cnpj: CNPJ) -> SchoolEntity | None:
        ...

    @abstractmethod
    def existis_cnpj(self, cnpj: CNPJ) -> bool:
        ...


class INucleosGroupRepository(ABC):
    @abstractmethod
    def save(self, n_group: NucleosGroupEntity) -> NucleosGroupEntity:
        ...

    @abstractmethod
    def find_by_id(self, id: UUID) -> NucleosGroupEntity | None:
        ...

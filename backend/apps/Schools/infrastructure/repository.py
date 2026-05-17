from uuid import UUID

from apps.Schools.domain.entities import NucleosGroupEntity, SchoolEntity
from apps.Schools.domain.repositories import (
    INucleosGroupRepository,
    ISchoolRepository,
)
from apps.Schools.domain.value_objects import CNPJ
from apps.Schools.infrastructure.models import NucleosGroup, School


class SchoolRepository(ISchoolRepository):
    def save(self, school: SchoolEntity) -> SchoolEntity | None:
        School.objects.update_or_create(
            id=school.id,
            defaults={
                'name': school.name,
                'cnpj': school.cnpj.value,
                'logo': school.logo,
                'gre': school.gre,
                'created_at': school.created_at,
                'deleted_at': school.deleted_at,
            },
        )

        return school

    def find_by_id(self, id: UUID) -> SchoolEntity | None:
        try:
            return self._to_model(School.objects.get(id=id))

        except School.DoesNotExist:
            return None

    def find_by_cnpj(self, cnpj: CNPJ) -> SchoolEntity | None:
        try:
            return self._to_model(School.objects.get(id=cnpj.value))

        except School.DoesNotExist:
            return None

    def existis_cnpj(self, cnpj: CNPJ) -> bool:
        return School.objects.filter(cnpj=cnpj.value).exists()

    def _to_model(self, model: School) -> SchoolEntity:
        return SchoolEntity(
            id=model.id,
            name=model.name,
            cnpj=CNPJ(value=model.cnpj),
            logo=model.logo.name if model.logo else None,
            gre=model.gre,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
        )


class NucleosGroupRepository(INucleosGroupRepository):
    def save(self, n_group: NucleosGroupEntity) -> NucleosGroupEntity:
        NucleosGroup.objects.update_or_create(
            id=n_group.id,
            defaults={
                'name': n_group.name,
                'school_id': n_group.school,
                'created_at': n_group.created_at,
                'deleted_at': n_group.deleted_at,
            },
        )

        return n_group

    def find_by_id(self, id: UUID) -> NucleosGroupEntity | None:
        try:
            return self._to_model(NucleosGroup.objects.get(id=id))

        except NucleosGroup.DoesNotExist:
            return None

    def _to_model(self, model: NucleosGroup) -> NucleosGroupEntity:
        return NucleosGroupEntity(
            id=model.id,
            name=model.name,
            school=model.school.id,
            created_at=model.created_at,
            deleted_at=model.deleted_at,
        )

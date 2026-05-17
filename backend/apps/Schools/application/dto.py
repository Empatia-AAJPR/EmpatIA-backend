from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from apps.Schools.domain.value_objects import CNPJ
from apps.Users.domain.value_objects import UploadFileVO


class SchoolInDTO(BaseModel):
    name: str
    cnpj: CNPJ
    logo: Optional[UploadFileVO] = None
    gre: str


class SchoolOutDTO(BaseModel):
    id: UUID
    name: str
    cnpj: str
    logo: str
    gre: str
    deleted_at: datetime | None

    @classmethod
    def from_domain(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            cnpj=model.cnpj.value,
            logo=model.logo,
            gre=model.gre,
            deleted_at=model.deleted_at,
        )


class UpdateSchoolInDTO(BaseModel):
    name: Optional[str] = None
    cnpj: Optional[CNPJ] = None
    gre: Optional[str] = None


class NucleosGroupInDTO(BaseModel):
    name: str
    school: UUID


class NucleosGroupOutDTO(BaseModel):
    id: UUID
    name: str
    school: UUID
    deleted_at: datetime | None

    @classmethod
    def from_domain(cls, model):
        return cls(id=model.id, name=model.name, school=model.school, deleted_at=model.deleted_at)


class UpdateNucleosGroupInDTO(BaseModel):
    name: Optional[str] = None

import base64
from uuid import UUID

import cv2
import numpy as np

from apps.Users.application.dto import StudentOutDTO
from apps.Users.domain.servicies import (
    ICompacterService,
    ICoordinatorQueryService,
    IDirectorQueryService,
    IStudentQueryService,
)
from apps.Users.infrastructure.models import Coordinator, Director, Student
from apps.Users.application.dto import (
    CoordinatorOutDTO,
    DirectorOutDTO,
)

from apps.Users.infrastructure.adapters.encoded_image import encode


class StudentQueryService(IStudentQueryService):
    def get_by_id(self, id: UUID) -> StudentOutDTO | None:
        student = Student.objects.select_related('user').get(id=id)
        if not student:
            return None

        return StudentOutDTO.from_domain(student)


class CoordinatorQueryService(ICoordinatorQueryService):
    def get_by_id(self, id: UUID) -> CoordinatorOutDTO | None:
        coordinator = Coordinator.objects.select_related('user').get(id=id)
        if not coordinator:
            return None
# media/photo/WhatsApp Image 2026-05-11 at 14.46.23.jpeg
        return CoordinatorOutDTO.from_domain(coordinator)


class DirectorQueryService(IDirectorQueryService):
    def get_by_id(self, id: UUID) -> DirectorOutDTO | None:
        director = Director.objects.select_related('user').get(id=id)
        if not director:
            return None

        return DirectorOutDTO.from_domain(director)


class CompacterService(ICompacterService):
    @staticmethod
    def encodedb64_image(img):
        img_encoded = encode(img)
        if img_encoded is None:
            return None

        return base64.b64encode(img_encoded).decode('utf-8')

    @staticmethod
    def decoded_img(img_base64):  # ← faltava esse
        if img_base64 is None:
            return None
        img_bytes = base64.b64decode(img_base64)
        np_array = np.frombuffer(img_bytes, dtype=np.uint8)
        return cv2.imdecode(np_array, cv2.IMREAD_COLOR)

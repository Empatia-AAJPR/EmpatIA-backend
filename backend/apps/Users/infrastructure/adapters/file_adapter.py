from apps.Users.domain.value_objects import UploadFileVO
from apps.Users.infrastructure.adapters.interface_adapter import (
    IImageFileAdapter,
)

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class ImageFileAdapter(IImageFileAdapter):
    def file_upload(self, img: UploadFileVO) -> str:
        file = default_storage.save(
            f'photo/{img.name}',
            ContentFile(content=img.content, name=img.name),
        )

        return default_storage.path(file)

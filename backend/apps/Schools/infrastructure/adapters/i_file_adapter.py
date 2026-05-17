from abc import ABC, abstractmethod

from apps.Users.domain.value_objects import UploadFileVO


class IImageFileAdapter(ABC):
    @abstractmethod
    def file_upload(self, img: UploadFileVO) -> str | None:
        ...

    @abstractmethod
    def delete(self, path: str) -> None:
        ...

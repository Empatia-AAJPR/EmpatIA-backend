from abc import ABC, abstractmethod
from typing import Any


class IRedisRepository(ABC):
    @abstractmethod
    def h_insert(self, key: str, field: str, value: Any):
        ...

    @abstractmethod
    def h_insert_ex(self, key: str, field: str, value: Any, ex: int):
        ...

    @abstractmethod
    def h_get(self, key: str, field: str):
        ...

    @abstractmethod
    def h_get_all(self, key: str):
        ...

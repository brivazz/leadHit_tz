"""Описание интерфейса для работы с БД."""

import abc
from typing import Any


class AbstractDB(abc.ABC):
    """Абстрактный класс для работы с БД."""

    @abc.abstractmethod
    async def get_collection(self, collection_name: str) -> Any:
        """Получить коллекцию по названию."""

    @abc.abstractmethod
    async def find_all(
        self,
        collection_name: str,
        query: dict[str, str],
        page_size: int | None = None,
        page_number: int | None = None,
    ) -> list[dict[str, str]] | None:
        """Поиск всех записей в коллекции по запросу."""


db: AbstractDB | None = None


def get_db() -> AbstractDB | None:
    """DI для FastAPI. Получаем DB."""
    return db

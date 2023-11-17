"""Реализация AbstractDB для MongoDB."""

from core.config import settings
from db.abstract import AbstractDB
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCursor
from pymongo.collection import Collection
from pymongo.errors import OperationFailure


class MongoDB(AbstractDB):  # type: ignore
    """Реализация AbstractDB для взаимодействия с коллекциями MongoDB."""

    def __init__(self, db_client: AsyncIOMotorClient) -> None:
        """Конструктор класса."""
        self._mongo_client: AsyncIOMotorClient = db_client
        self.database = self._mongo_client[settings.mongo_db]

    async def get_collection(self, collection_name: str) -> Collection:
        """Получить коллекцию по названию."""
        return self.database[collection_name]

    async def find_all(
        self,
        collection_name: str,
        query: dict[str, str],
        page_size: int | None = None,
        page_number: int | None = None,
    ) -> list[dict[str, str]] | None:
        """Поиск всех записей в коллекции по запросу."""
        try:
            collection = await self.get_collection(collection_name)

            if page_size and page_number:
                skip_count = (page_number - 1) * page_size
                result: AsyncIOMotorCursor = collection.find(query).skip(skip_count).limit(page_size)
            else:
                result = collection.find(query)
            entries = await result.to_list(length=None)
        except OperationFailure:
            return None
        if entries:
            logger.info(
                f'Entries in the collection: {collection_name} found {len(entries)}',
            )
            return entries  # type: ignore[no-any-return]
        logger.info(f'Entries in the collection: {collection_name} not found')
        return None

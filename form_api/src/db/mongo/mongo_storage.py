"""Модуль создания подключения/отключения к MongoDB и создание коллекций."""


from core.config import settings
from db import abstract
from db.mongo import mongo_rep
from db.mongo.templates_data import TEMPLATES
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError

mongo_client: AsyncIOMotorClient | None = None


async def on_startup(mongo_uri: str) -> None:
    """Выполняет необходимые операции при запуске приложения."""
    global mongo_client
    try:
        mongo_client = AsyncIOMotorClient(
            mongo_uri,
            uuidRepresentation='standard',
        )
        db: Database = mongo_client[settings.mongo_db]

        if 'form_templates' not in await db.list_collection_names():
            collection: Collection = db['form_templates']
            collection.create_index([('name', 1)], unique=True)

            await collection.insert_many(TEMPLATES, ordered=False)

        abstract.db = mongo_rep.MongoDB(mongo_client)
        logger.info('Connected to MongoDB successfully.')
    except ServerSelectionTimeoutError as er:
        logger.exception(f'Error connecting to MongoDB: {er}')
    except Exception as er:
        logger.exception(f'Error connecting to MongoDB: {er}')


async def on_shutdown() -> None:
    """
    Выполняет необходимые операции при завершении работы приложения.

    Закрывает соединение с MongoDB, если оно было установлено.
    """
    if mongo_client:
        mongo_client.close()
        logger.info('Disconnected from MongoDB.')

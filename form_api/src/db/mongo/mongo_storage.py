"""Модуль создания подключения/отключения к MongoDB и создание коллекций."""

from core.config import settings
from db import abstract
from db.mongo import mongo_rep
from db.mongo.templates_data import TEMPLATES
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors
from pymongo.collection import Collection
from pymongo.database import Database

mongo_client: AsyncIOMotorClient | None = None


def validate_values(template: dict[str, str]) -> None:
    """Валидатор типов значений полей."""
    allowed_types = ['date', 'phone', 'email', 'text']

    for key, value in template.items():
        if key == 'name':
            continue
        if isinstance(value, str):
            if value not in allowed_types:
                raise ValueError(f'Invalid value type for key {key}: {value}')
        else:
            raise ValueError(f'Invalid value type for key {key}: {value})')


async def on_startup(mongo_uri: str) -> None:
    """Выполняет необходимые операции при запуске приложения."""
    global mongo_client
    try:
        mongo_client = AsyncIOMotorClient(
            mongo_uri,
        )
        db: Database = mongo_client[settings.mongo_db]

        if 'form_templates' not in await db.list_collection_names():
            collection: Collection = db['form_templates']
            collection.create_index([('name', 1)])
            for template in TEMPLATES:
                try:
                    validate_values(template)
                    await collection.insert_one(template)
                except (ValueError, errors.OperationFailure) as er:
                    logger.error(er)

        abstract.db = mongo_rep.MongoDB(mongo_client)
        logger.info('Connected to MongoDB successfully.')
    except errors.ServerSelectionTimeoutError as er:
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

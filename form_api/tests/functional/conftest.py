import asyncio
import contextlib
import os
import sys

import aiohttp
import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors
from pymongo.collection import Collection

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from functional.settings import test_settings

COLLECTION_NAMES = ['form_templates']


@pytest.fixture(scope='session')
def event_loop():
    """Фикстура для создания нового событийного цикла asyncio."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(name='mongo_client', scope='session')
async def mongo_client():
    client = AsyncIOMotorClient(test_settings.mongo_uri)
    yield client
    await client.close()


@pytest.fixture(scope='session', autouse=True)
async def delete_all_mongo_data(mongo_client: AsyncIOMotorClient):
    async def delete_data(client):
        db = client[test_settings.mongo_db]

        for collection_name in COLLECTION_NAMES:
            with contextlib.suppress(errors.OperationFailure):
                collection: Collection = db[collection_name]
                await collection.delete_many({})

    await delete_data(mongo_client)
    yield
    await delete_data(mongo_client)


@pytest_asyncio.fixture(scope='session')
async def session_client():
    """Фикстура для создания сессии клиента aiohttp."""
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope='session')
def make_get_request(session_client: aiohttp.ClientSession):
    """Выполняет http запросы."""

    async def inner(
        url: str,
        method: str = 'GET',
        params: dict | None = None,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> tuple[dict, int]:
        if method == 'GET':
            async with session_client.get(url, params=params, headers=headers) as response:
                message = await response.json()
                status = response.status
                return message, status

        if method == 'POST':
            async with session_client.post(url, json=data, headers=headers) as response:
                message = await response.json()
                status = response.status
                return message, status

    return inner

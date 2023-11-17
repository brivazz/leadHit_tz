"""Модуль конфигурации тестов для сервиса event_api."""

from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    """Класс, представляющий настройки приложения."""

    service_url: str = Field('http://127.0.0.1:8000')
    mongo_uri: str = Field('mongodb://127.0.0.1:27017/')


test_settings = TestSettings()

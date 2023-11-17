"""Модуль с настройками приложения."""


from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):  # type: ignore
    """Настройки приложения."""

    project_name: str = Field('form_api')
    debug: str = Field('False')

    mongo_uri: str = Field('mongodb://127.0.0.1:27017/')
    mongo_db: str = Field('forms_db')


settings = Settings()

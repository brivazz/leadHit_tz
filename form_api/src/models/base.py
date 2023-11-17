"""Файл базовой модели."""

import typing

import orjson
from pydantic import BaseModel


def orjson_dumps(value: dict[typing.Any, str], *, default: typing.Callable[[int, str], str]) -> typing.Any | str:
    """Сериализует объект 'value' в JSON с использованием библиотеки orjson.

    Args:
        value: Основной объект, который нужно сериализовать в JSON.
        default: Функция-обратный вызов (callback), которая будет использоваться для сериализации.

    Returns:
        Строка, представляющая основной объект 'value' в формате JSON.

    """
    return orjson.dumps(value, default=default).decode()


class BaseOrjsonModel(BaseModel):  # type: ignore
    """Базовая модель."""

    class Config:
        model_load = orjson.loads
        model_dump = orjson_dumps

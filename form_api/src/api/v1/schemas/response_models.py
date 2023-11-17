"""Модуль с моделями ответа по http."""

from models.base import BaseOrjsonModel


class ResponseForm(BaseOrjsonModel):  # type: ignore
    """Модель ответа для формы."""

    name: str

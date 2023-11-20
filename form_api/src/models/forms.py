"""Модели шаблонов."""

import enum

from fastapi import HTTPException, status
from models.base import BaseOrjsonModel
from pydantic import root_validator


class FormFieldEnum(str, enum.Enum):
    """Модель типа данных полей."""

    date = 'date'
    phone = 'phone'
    email = 'email'
    text = 'text'


class DynamicFormData(BaseOrjsonModel):  # type: ignore
    """Модель формы."""

    class Config:
        extra = 'allow'

    @root_validator(skip_on_failure=True)
    def validate_model(cls, values):  # type: ignore
        """Модель валидатор входящих данных."""
        for key, value in values.items():
            if value not in FormFieldEnum.__members__:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid: '{value}' for key: '{key}'. Acceptable value: 'date', 'phone', 'email', 'text'.",
                )
        return values


class TemplateError(Exception):
    """Базовый класс для ошибок сервиса."""

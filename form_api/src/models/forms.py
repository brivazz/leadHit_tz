"""Модели шаблонов."""

import enum
import re
from datetime import datetime

from fastapi import HTTPException, status
from models.base import BaseOrjsonModel
from pydantic import root_validator


class DateValidator:
    """Модель валидатора даты."""

    @classmethod
    def validate_date(cls, date: str) -> str:
        """Валидирует дату по шаблонам."""
        date_formats = ['%d.%m.%Y', '%Y-%m-%d']
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date, date_format)
                return parsed_date.strftime(date_format)
            except ValueError:
                pass
        raise ValueError


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
        for field, value in values.items():
            if field not in FormFieldEnum.__members__:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid field '{field}'. Acceptable fields: 'date', 'phone', 'email', 'text'.",
                )

            field_type = FormFieldEnum[field].value
            if field_type == 'date':
                try:
                    DateValidator.validate_date(value)
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid date format, should be 'DD.MM.YYYY' or 'YYYY-MM-DD'",
                    )
            pattern = r'^(\+)[7][0-9]{10}$'
            if field_type == 'phone' and not re.search(pattern, value, re.I):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Phone number must be in format '+7 XXX XXX XX XX' without spaces",
                )
            email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if field_type == 'email' and not re.match(email_pattern, value):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid email address. Example: example@example.com',
                )
            values[field] = value

        return values


class TemplateError(Exception):
    """Базовый класс для ошибок сервиса."""

"""Модели шаблонов."""

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


class FormField(BaseOrjsonModel):  # type: ignore
    """Модель типа данных полей."""

    date: str | None = None
    phone: str | None = None
    email: str | None = None
    text: str | None = None

    @root_validator(skip_on_failure=True)
    def validate_fields(cls, values):  # type: ignore
        """Валидатор полей шаблона."""
        date = values.get('date')
        phone = values.get('phone')
        email = values.get('email')
        if date:
            try:
                DateValidator.validate_date(date)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid date format, should be 'DD.MM.YYYY' or 'YYYY-MM-DD'",
                )
        pattern = r'^(\+)[7][0-9]{10}$'
        if phone and not re.search(pattern, phone, re.I):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number must be in format '+7 XXX XXX XX XX' without spaces",
            )
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if email:
            if not re.match(email_pattern, email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Invalid email address. Example: example@example.com',
                )
        return values


class TemplateError(Exception):
    """Базовый класс для ошибок сервиса."""

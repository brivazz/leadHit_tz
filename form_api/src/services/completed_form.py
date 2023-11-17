"""Модуль сервиса для поиска шаблонов с указанными и совпадающими полями."""

from collections import defaultdict
from functools import lru_cache
from typing import Any, DefaultDict

from api.v1.schemas.response_models import ResponseForm
from db.abstract import AbstractDB, get_db
from fastapi import Depends
from models.form_templates import FormField


class CompletedForm:
    """Сервис для поиска шаблонов форм."""

    def __init__(self, db: AbstractDB) -> None:
        """Инициализация объекта."""
        self.db = db

    async def get_form(self, field_names: FormField) -> ResponseForm:
        """Ищет в бд запись у которой поля совпали с полями в присланной форме."""
        field_queries = []
        key_list = []
        for field, value in field_names.model_dump().items():
            if value:
                field_queries.append({f'fields.{field}': field})
                key_list.append(field)

        query = {'$or': field_queries}
        if matched_templates := await self.db.find_all('form_templates', query):
            name = await self.max_match_document(matched_templates, key_list)
            return ResponseForm(name=name)

    async def max_match_document(self, matched_templates: list[dict[Any, Any]], key_list: list[str]) -> str:
        """Выбирает наиболее подходящее имя документа."""
        count_dict: DefaultDict[str, int] = defaultdict(int)

        for template in matched_templates:
            template_fields = template['fields']

            for k, v in template_fields.items():
                if k == v and k in key_list:
                    count_dict[template['name']] += 1

        return max(count_dict, key=lambda k: count_dict[k])

    async def fields_type(self, fields: FormField) -> dict[str, str]:
        """Если подходящей формы не нашлось возвращаются поля на основе правил валидации."""
        return {field: field for field in fields.model_dump().keys()}


@lru_cache
def get_completed_form_service(
    db: AbstractDB = Depends(get_db),
) -> CompletedForm:
    """DI получения сервиса для FastAPI."""
    return CompletedForm(db)

"""Модуль сервиса для поиска шаблонов с указанными и совпадающими полями."""

from collections import defaultdict
from functools import lru_cache
from typing import Any, DefaultDict

from api.v1.schemas.response_models import ResponseForm
from db.abstract import AbstractDB, get_db
from fastapi import Depends
from models.forms import FormFieldEnum


class FormService:
    """Сервис для поиска шаблонов форм."""

    def __init__(self, db: AbstractDB) -> None:
        """Инициализация объекта."""
        self.db = db

    async def find_matching_template(self, form_data: dict[str, str]) -> ResponseForm:
        """Ищет в бд запись у которой поля совпали с полями в присланной форме."""
        field_queries = []
        key_list = []
        for field, value in form_data.items():
            if value:
                field_queries.append({f'{field}': field})
                key_list.append(field)

        query = {'$or': field_queries}
        if matched_templates := await self.db.find_all('form_templates', query):
            name = await self.max_match_document(matched_templates, key_list)
            return ResponseForm(name=name)

    async def max_match_document(self, matched_templates: list[dict[Any, Any]], key_list: list[str]) -> str:
        """Выбирает имя наиболее подходящего документа."""
        count_dict: DefaultDict[str, int] = defaultdict(int)

        for template in matched_templates:
            for key, value in template.items():
                if key == value and key in key_list:
                    count_dict[template['name']] += 1

        return max(count_dict, key=lambda k: count_dict[k])

    async def fields_type(self, form_data: dict[str, str]) -> dict[str, str]:
        """Если подходящей формы не нашлось возвращаются поля на основе правил валидации."""
        len_form_data = len(form_data.keys())
        return {key: value.value for key, value in list(FormFieldEnum.__members__.items())[:len_form_data]}


@lru_cache
def get_form_service(
    db: AbstractDB = Depends(get_db),
) -> FormService:
    """DI получения сервиса для FastAPI."""
    return FormService(db)

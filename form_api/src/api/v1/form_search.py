"""API для получения подходящего шаблона."""

from api.v1.schemas.response_models import ResponseForm
from fastapi import APIRouter, Depends, HTTPException, status
from models.forms import DynamicFormData, TemplateError
from services.form_service import FormService, get_form_service

form_router = APIRouter()


@form_router.post(
    '/get_form',
    summary='Поиск формы',
    description='Поиск шаблона формы, у которого совпали имя и тип значения с присланной формой',
    response_description='Имя шаблона формы или список полей с их типами',
    tags=['Поиск подходящего шаблона формы'],
    status_code=status.HTTP_200_OK,
)
async def search_form(
    form_data: DynamicFormData,
    service: FormService = Depends(get_form_service),
) -> ResponseForm | dict[str, str]:
    """Получить форму."""
    try:
        if template_name := await service.find_matching_template(form_data.model_dump()):
            return ResponseForm.model_validate(template_name)
        return await service.fields_type(form_data.model_dump())
    except TemplateError as err:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

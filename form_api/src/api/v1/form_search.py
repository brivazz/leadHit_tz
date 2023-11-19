"""API для получения подходящего шаблона."""

from api.v1.schemas.response_models import ResponseForm
from fastapi import APIRouter, Body, Depends, HTTPException, status
from models.form_templates import FormField, TemplateError
from services.form import FormService, get_form_service

form_router = APIRouter()


@form_router.post(
    '/get_form',
    summary='Получить форму',
    description='Запрашивает форму подходящую по переданным полям',
    status_code=status.HTTP_200_OK,
)
async def get_form(
    form_data: FormField = Body(),
    service: FormService = Depends(get_form_service),
) -> ResponseForm | dict[str, str]:
    """Получить форму."""
    try:
        if template_name := await service.get_form(form_data):
            return ResponseForm.model_validate(template_name)
        return await service.fields_type(form_data)
    except TemplateError as err:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

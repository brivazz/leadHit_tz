"""API получения форм."""

import contextlib
from collections.abc import AsyncIterator

import fastapi
from api.v1 import form_search
from core.config import settings
from db.mongo import mongo_storage


@contextlib.asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    """Выполняет необходимые действия при запуске/остановке приложения."""
    await mongo_storage.on_startup(settings.mongo_uri)
    yield
    await mongo_storage.on_shutdown()


def init_app() -> fastapi.FastAPI:
    """Инициализирует экземпляр FastAPI."""
    return fastapi.FastAPI(
        title=settings.project_name,
        docs_url='/api/openapi',
        openapi_url='/api/openapi.json',
        default_response_class=fastapi.responses.ORJSONResponse,
        debug=settings.debug,
        lifespan=lifespan,
    )


app = init_app()

app.include_router(form_search.form_router, prefix='/api/v1', tags=['get_form'])

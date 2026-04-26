from datetime import datetime

from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep
from src.services.analytics import AnalyticsService
from src.tasks.analytics_tasks import compute_devise_analytics
from src.utils.exceptions import DeviceNotFoundException

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/users/{user_id}",
    summary="Аналитика по пользователю",
    description="Возвращает агрегированную статистику по всем устройствам пользователя, "
    "а также отдельную статистику для каждого устройства.",
)
async def get_analytics_by_usr(user_id: int, db: DBDep):
    try:
        analytics = await AnalyticsService(db).get_analytics_by_user(user_id)
        return analytics
    except DeviceNotFoundException:
        raise HTTPException(
            status_code=404, detail="Устройства пользователя не найдены"
        )


@router.get(
    "/tasks/{task_id}",
    summary="Результат асинхронной задачи",
    description="Возвращает статус и результат задачи Celery по её идентификатору. "
    "Возможные статусы: PENDING, SUCCESS, FAILURE.",
)
async def get_task_result(task_id: str):
    result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
    }


@router.get(
    "/{device_id}/async",
    summary="Запуск асинхронного расчёта аналитики",
    description="Ставит задачу расчёта аналитики в очередь Celery и сразу возвращает task_id. "
    "Результат можно получить через GET /analytics/tasks/{task_id}.",
)
async def get_analytics_async(
    device_id: int, date_from: datetime | None = None, date_to: datetime | None = None
):
    task = compute_devise_analytics.delay(
        device_id,
        date_from.isoformat() if date_from else None,
        date_to.isoformat() if date_to else None,
    )
    return {"task_id": task.id}


@router.get(
    "/{device_id}",
    summary="Аналитика по устройству",
    description="Возвращает статистику (min, max, count, sum, медиана) по осям x, y, z "
    "для указанного устройства. Поддерживает фильтрацию по периоду через date_from и date_to.",
)
async def get_analytics(
    device_id: int,
    db: DBDep,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):

    analutics = await AnalyticsService(db).get_analytics(device_id, date_from, date_to)
    return analutics

import asyncio
import logging
from datetime import datetime


from src.config import settings
from src.database import get_async_session_maker
from src.services.analytics import AnalyticsService
from src.tasks.celery_app import celery_instance
from src.utils.database import DBManager


async def _compute_devise_analytics(
    device_id: int, date_from: datetime | None, date_to: datetime | None
):
    session_maker = get_async_session_maker(settings.DB_URL)
    async with DBManager(session_maker) as db:
        result = await AnalyticsService(db).get_analytics(device_id, date_from, date_to)
        if not result:
            return None
        return result.model_dump()


@celery_instance.task(bind=True, max_retries=3, default_retry_delay=5)
def compute_devise_analytics(
    self, device_id: int, date_from: str | None = None, date_to: str | None = None
):
    try:
        date_from_datetime = datetime.fromisoformat(date_from) if date_from else None
        date_to_datetime = datetime.fromisoformat(date_to) if date_to else None

        analytics = asyncio.run(
            _compute_devise_analytics(device_id, date_from_datetime, date_to_datetime)
        )
        return analytics

    except Exception as e:
        logging.error(f"Ошибка при вычислении аналитики для device_id={device_id}: {e}")
        raise self.retry(exc=e)

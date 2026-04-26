import logging
from datetime import datetime

from sqlalchemy import select, func

from src.models.measurements import MeasurementsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import MeasurementDataMapper
from src.utils.exceptions import ObjectNotFoundException


class MeasurementRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, MeasurementsOrm)

    mapper = MeasurementDataMapper

    def _axis_columns(self, axis):
        col = getattr(MeasurementsOrm, axis)
        return [
            func.min(col).label(f"{axis}_min"),
            func.max(col).label(f"{axis}_max"),
            func.count(col).label(f"{axis}_count"),
            func.sum(col).label(f"{axis}_sum"),
            func.percentile_cont(0.5).within_group(col).label(f"{axis}_median"),
        ]

    def _analytics_columns(self, with_device_id: bool = False):
        columns = []
        if with_device_id:
            columns.append(MeasurementsOrm.device_id)
        for axis in ("x", "y", "z"):
            columns.extend(self._axis_columns(axis))
        return columns

    async def get_analytics(
        self,
        device_id: int,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ):

        query = select(*self._analytics_columns()).where(
            MeasurementsOrm.device_id == device_id
        )

        if date_from:
            query = query.where(MeasurementsOrm.timestamp >= date_from)
        if date_to:
            query = query.where(MeasurementsOrm.timestamp <= date_to)

        result = await self._session.execute(query)
        row = result.one_or_none()

        if row is None:
            logging.warning(f"Измерения для device_id={device_id} не найдены")
            raise ObjectNotFoundException

        return row

    async def get_analytics_by_devices_ids(
        self,
        device_ids: list[int],
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ):

        query = (
            select(*self._analytics_columns(with_device_id=True))
            .where(MeasurementsOrm.device_id.in_(device_ids))
            .group_by(MeasurementsOrm.device_id)
        )

        if date_from:
            query = query.where(MeasurementsOrm.timestamp >= date_from)
        if date_to:
            query = query.where(MeasurementsOrm.timestamp <= date_to)

        result = await self._session.execute(query)
        rows = result.all()

        if not rows:
            logging.warning(f"Измерения для devices {device_ids} не найдены")
            return []

        return rows

    async def get_analytics_aggregated(self, device_ids: list[int]):
        query = select(*self._analytics_columns()).where(
            MeasurementsOrm.device_id.in_(device_ids)
        )

        result = await self._session.execute(query)
        row = result.one_or_none()

        if row is None:
            logging.warning(
                f"Агрегированные данные для devices {device_ids} не найдены"
            )
            raise ObjectNotFoundException

        return row

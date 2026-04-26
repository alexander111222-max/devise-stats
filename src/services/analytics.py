import logging
from datetime import datetime

from src.schemas.analytics import (
    AnalyticsSchema,
    AxisMetricsSchema,
    AggregatedAnalyticsSchema,
    UserAnalyticsSchema,
)
from src.services.base import BaseService
from src.utils.exceptions import DeviceNotFoundException


class AnalyticsService(BaseService):
    def __init__(self, db):
        super().__init__(db)

    async def get_analytics(
        self,
        device_id: int,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> AnalyticsSchema:

        row = await self._db.measurements.get_analytics(device_id, date_from, date_to)

        return AnalyticsSchema(
            device_id=device_id,
            x=AxisMetricsSchema(
                min_value=row.x_min or 0,
                max_value=row.x_max or 0,
                count=row.x_count or 0,
                total=row.x_sum or 0,
                median=row.x_median or 0,
            ),
            y=AxisMetricsSchema(
                min_value=row.y_min or 0,
                max_value=row.y_max or 0,
                count=row.y_count or 0,
                total=row.y_sum or 0,
                median=row.y_median or 0,
            ),
            z=AxisMetricsSchema(
                min_value=row.z_min or 0,
                max_value=row.z_max or 0,
                count=row.z_count or 0,
                total=row.z_sum or 0,
                median=row.z_median or 0,
            ),
        )

    async def get_analytics_by_user(self, user_id: int):
        devices = await self._db.devices.get_by_user(user_id)

        if not devices:
            logging.warning(f"Устройства для user_id={user_id} не найдены")
            raise DeviceNotFoundException

        devices_ids = [device.id for device in devices]

        rows = await self._db.measurements.get_analytics_by_devices_ids(devices_ids)
        aggregated_row = await self._db.measurements.get_analytics_aggregated(
            devices_ids
        )

        device_analytics = [
            AnalyticsSchema(
                device_id=row.device_id,
                x=AxisMetricsSchema(
                    min_value=row.x_min or 0,
                    max_value=row.x_max or 0,
                    count=row.x_count or 0,
                    total=row.x_sum or 0,
                    median=row.x_median or 0,
                ),
                y=AxisMetricsSchema(
                    min_value=row.y_min or 0,
                    max_value=row.y_max or 0,
                    count=row.y_count or 0,
                    total=row.y_sum or 0,
                    median=row.y_median or 0,
                ),
                z=AxisMetricsSchema(
                    min_value=row.z_min or 0,
                    max_value=row.z_max or 0,
                    count=row.z_count or 0,
                    total=row.z_sum or 0,
                    median=row.z_median or 0,
                ),
            )
            for row in rows
        ]

        return UserAnalyticsSchema(
            aggregated=AggregatedAnalyticsSchema(
                x=AxisMetricsSchema(
                    min_value=aggregated_row.x_min or 0,
                    max_value=aggregated_row.x_max or 0,
                    count=aggregated_row.x_count or 0,
                    total=aggregated_row.x_sum or 0,
                    median=aggregated_row.x_median or 0,
                ),
                y=AxisMetricsSchema(
                    min_value=aggregated_row.y_min or 0,
                    max_value=aggregated_row.y_max or 0,
                    count=aggregated_row.y_count or 0,
                    total=aggregated_row.y_sum or 0,
                    median=aggregated_row.y_median or 0,
                ),
                z=AxisMetricsSchema(
                    min_value=aggregated_row.z_min or 0,
                    max_value=aggregated_row.z_max or 0,
                    count=aggregated_row.z_count or 0,
                    total=aggregated_row.z_sum or 0,
                    median=aggregated_row.z_median or 0,
                ),
            ),
            device_analytics=device_analytics,
        )

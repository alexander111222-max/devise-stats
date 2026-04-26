from pydantic import BaseModel


class AxisMetricsSchema(BaseModel):
    min_value: float
    max_value: float
    count: int
    total: float
    median: float


class AnalyticsSchema(BaseModel):
    device_id: int
    x: AxisMetricsSchema
    y: AxisMetricsSchema
    z: AxisMetricsSchema


class AggregatedAnalyticsSchema(BaseModel):
    x: AxisMetricsSchema
    y: AxisMetricsSchema
    z: AxisMetricsSchema


class UserAnalyticsSchema(BaseModel):
    aggregated: AggregatedAnalyticsSchema
    device_analytics: list[AnalyticsSchema]

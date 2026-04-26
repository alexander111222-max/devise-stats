from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class MeasurementsOrm(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(primary_key=True)

    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)
    z: Mapped[float] = mapped_column(Float)

    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id", ondelete="CASCADE"))
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    device: Mapped["DevicesOrm"] = relationship(back_populates="measurements")
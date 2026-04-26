from datetime import datetime

from sqlalchemy import ForeignKey, func, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class DeviceOrm(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    user: Mapped["UsersOrm"] = relationship(back_populates="devices")
    measurements: Mapped[list["MeasurementsOrm"]] = relationship(back_populates="device")


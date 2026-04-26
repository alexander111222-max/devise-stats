# src/models/users
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int]  = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    devices: Mapped[list["DevicesOrm"]] = relationship(back_populates="users")
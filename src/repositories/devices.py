import logging

from sqlalchemy import select

from src.models.devices import DeviceOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import DeviceDataMapper


class DeviceRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session, DeviceOrm)

    mapper = DeviceDataMapper

    async def get_by_user(self, user_id: int):
        query = select(self._model).where(user_id == self._model.user_id)
        result = await self._session.execute(query)
        models = result.scalars().all()

        if not models:
            logging.warning(f"Девайся для user_id={user_id} не найдены")
            return []

        return [self.mapper.map_to_domain_entity(model) for model in models]

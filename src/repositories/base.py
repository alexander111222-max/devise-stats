from typing import Type

from pydantic import BaseModel
from sqlalchemy import insert

from src.repositories.mappers.base import DataMapper


class BaseRepository:

    mapper: Type[DataMapper]

    def __init__(self, session, model):
        self._session = session
        self._model = model

    async def add_one(self, data: BaseModel):

        stmt = (insert(self._model).values(**data.model_dump())
                .returning(self._model))

        row = await self._session.execute(stmt)

        model = row.scalar_one_or_none()

        return self.mapper.map_to_domain_entity(model)







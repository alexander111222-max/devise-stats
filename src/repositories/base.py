import logging
from typing import Type

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from src.repositories.mappers.base import DataMapper
from src.utils.exceptions import (
    ObjectCreationException,
    ObjectNotFoundException,
    UniqueConstraintException,
)


class BaseRepository:
    mapper: Type[DataMapper]

    def __init__(self, session, model):
        self._session = session
        self._model = model

    async def add_one(self, data: BaseModel):
        try:
            stmt = (
                insert(self._model).values(**data.model_dump()).returning(self._model)
            )

            row = await self._session.execute(stmt)
            model = row.scalar_one_or_none()

            if model is None:
                raise ObjectCreationException
            logging.info(f"Создан обьект {self._model.__tablename__}: id-{model.id}")
            return self.mapper.map_to_domain_entity(model)

        except IntegrityError as e:
            logging.warning(f"Конфликт уникальности в {self._model.__tablename__}: {e}")
            raise UniqueConstraintException

        except Exception as ex:
            logging.error(
                f"Ошибка при создании обьекта {self._model.__tablename__}: {ex}"
            )
            raise ObjectCreationException

    async def get_one_or_none(self, id: int):
        query = select(self._model).where(id == self._model.id)
        result = await self._session.execute(query)
        model = result.scalar_one_or_none()

        if model is None:
            logging.warning(f"Обьект {self._model.__tablename__} id={id} не найден")
            raise ObjectNotFoundException

        return self.mapper.map_to_domain_entity(model)

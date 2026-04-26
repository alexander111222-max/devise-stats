#src/repositories/mappers/base
from typing import Type

from pydantic import BaseModel
from typing_extensions import TypeVar

from src.database import Base

SchemaType = TypeVar("SchemaType", bound=BaseModel)

class DataMapper:
    model: Type[Base]
    schema: Type[SchemaType]


    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.model(**data.model_dump())


    


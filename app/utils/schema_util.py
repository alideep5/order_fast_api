from typing import Type, TypeVar, List
from pydantic import BaseModel, TypeAdapter

T = TypeVar("T", bound=BaseModel)
D = TypeVar("D")


class SchemaUtil:
    @staticmethod
    def convert_to_schema(domain_model: D, pydantic_model: Type[T]) -> T:
        adapter = TypeAdapter(pydantic_model)
        return adapter.validate_python(domain_model)

    @staticmethod
    def convert_list_to_schema(
        domain_models: List[D], pydantic_model: Type[T]
    ) -> List[T]:
        adapter = TypeAdapter(pydantic_model)
        return [adapter.validate_python(model) for model in domain_models]

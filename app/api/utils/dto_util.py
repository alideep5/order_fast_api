from typing import Type, TypeVar, List, Any
from dataclasses import asdict, is_dataclass
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class DTOUtil:
    @staticmethod
    def convert_to_dto(source: Any, target_cls: Type[T]) -> T:
        if is_dataclass(source) and not isinstance(source, type):
            source_data = asdict(source)
        elif isinstance(source, dict):
            source_data = source
        else:
            raise ValueError("Source must be a dataclass instance or a dictionary.")

        return target_cls(**source_data)

    @staticmethod
    def convert_to_dto_list(source_list: List[Any], target_cls: Type[T]) -> List[T]:
        if not all(
            (is_dataclass(obj) and not isinstance(obj, type)) or isinstance(obj, dict)
            for obj in source_list
        ):
            raise ValueError(
                "All elements in source_list must be dataclass instances or dictionaries."
            )

        return [DTOUtil.convert_to_dto(source, target_cls) for source in source_list]

from abc import ABC, abstractmethod
from functools import total_ordering


@total_ordering
class Entity(ABC):


    _counter: int = 0

    def __init__(self, entity_id: int | None = None) -> None:
        if entity_id is None:
            Entity._counter += 1
            entity_id = Entity._counter
        else:
            Entity._counter = max(Entity._counter, entity_id)
        self._id = entity_id

    @property
    def id(self) -> int:
        return self._id

    # --- абстрактный интерфейс ---
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Человекочитаемое имя сущности."""

    @abstractmethod
    def sort_key(self) -> tuple:
        """Ключ для естественной сортировки (используется в __lt__)."""

    @abstractmethod
    def to_row(self) -> tuple:
        """Представление сущности строкой таблицы."""

    @staticmethod
    @abstractmethod
    def headers() -> tuple:
        """Заголовки столбцов таблицы."""

    # --- специальные методы ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return type(self) is type(other) and self._id == other._id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.sort_key() < other.sort_key()

    def __hash__(self) -> int:
        return hash((type(self).__name__, self._id))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(id={self._id}, name={self.display_name!r})"

    def __str__(self) -> str:
        return self.display_name

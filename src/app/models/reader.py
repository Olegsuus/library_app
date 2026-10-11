"""Сущность «Читатель»."""
import re
from typing import Iterator

from .entity import Entity


class Reader(Entity):
    PHONE_PATTERN = re.compile(r"^\+?[\d\-\s()]{5,20}$")

    def __init__(self, name: str, phone: str, entity_id: int | None = None) -> None:
        super().__init__(entity_id)
        self._name = ""
        self._phone = ""
        self._book_ids: list[int] = []
        self.name = name
        self.phone = phone

    # --- геттеры и сеттеры ---
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = str(value).strip()
        if len(value) < 2:
            raise ValueError("Имя читателя должно содержать хотя бы 2 символа")
        self._name = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        value = str(value).strip()
        if not Reader.PHONE_PATTERN.match(value):
            raise ValueError("Некорректный номер телефона")
        self._phone = value

    @property
    def book_ids(self) -> tuple:
        return tuple(self._book_ids)

    # --- бизнес-логика ---
    def take(self, book_id: int) -> None:
        if book_id in self._book_ids:
            raise ValueError("Эта книга уже у читателя")
        self._book_ids.append(book_id)

    def release(self, book_id: int) -> None:
        if book_id not in self._book_ids:
            raise ValueError("Этой книги нет у читателя")
        self._book_ids.remove(book_id)

    # --- реализация абстрактного интерфейса ---
    @property
    def display_name(self) -> str:
        return self._name

    def sort_key(self) -> tuple:
        return (self._name.lower(),)

    def to_row(self) -> tuple:
        return str(self.id), self._name, self._phone, str(len(self))

    @staticmethod
    def headers() -> tuple:
        return "ID", "Имя", "Телефон", "Книг на руках"

    # --- дополнительные специальные методы ---
    def __len__(self) -> int:
        return len(self._book_ids)

    def __iter__(self) -> Iterator[int]:
        return iter(tuple(self._book_ids))

    def __contains__(self, book_id: int) -> bool:
        return book_id in self._book_ids

    def __str__(self) -> str:
        return f"{self._name} ({self._phone})"

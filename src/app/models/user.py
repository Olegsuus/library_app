import re

from .entity import Entity


class User(Entity):
    LOGIN_PATTERN = re.compile(r"^[A-Za-zА-Яа-яЁё0-9_.\-]{3,20}$")

    def __init__(self, login: str, entity_id: int | None = None) -> None:
        super().__init__(entity_id)
        self._login = ""
        self.login = login

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, value: str) -> None:
        value = str(value).strip()
        if not User.LOGIN_PATTERN.match(value):
            raise ValueError("Логин: 3–20 символов, буквы, цифры, _ . -")
        self._login = value

    @property
    def display_name(self) -> str:
        return self._login

    def sort_key(self) -> tuple:
        return (self._login.lower(),)

    def to_row(self) -> tuple:
        return str(self.id), self._login

    @staticmethod
    def headers() -> tuple:
        return "ID", "Логин"

    def __len__(self) -> int:
        return len(self._login)

    def __bool__(self) -> bool:
        return bool(self._login)

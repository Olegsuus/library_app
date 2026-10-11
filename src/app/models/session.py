from datetime import datetime

from .entity import Entity


class Session(Entity):
    TIME_FORMAT = "%d.%m.%Y %H:%M:%S"

    def __init__(self, login: str, time_in: datetime,
                 time_out: datetime | None = None, entity_id: int | None = None) -> None:
        super().__init__(entity_id)
        self._login = str(login)
        self._time_in = time_in
        self._time_out = time_out

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, value: str) -> None:
        if not str(value).strip():
            raise ValueError("Логин сессии не может быть пустым")
        self._login = str(value).strip()

    @property
    def time_in(self) -> datetime:
        return self._time_in

    @time_in.setter
    def time_in(self, value: datetime) -> None:
        self._time_in = value

    @property
    def time_out(self) -> datetime | None:
        return self._time_out

    @time_out.setter
    def time_out(self, value: datetime) -> None:
        if value < self._time_in:
            raise ValueError("Время выхода раньше времени входа")
        self._time_out = value

    @property
    def is_closed(self) -> bool:
        return self._time_out is not None

    @staticmethod
    def fmt(value: datetime | None) -> str:
        return value.strftime(Session.TIME_FORMAT) if value else "-"

    @staticmethod
    def parse(value: str) -> datetime | None:
        return None if value == "-" else datetime.strptime(value, Session.TIME_FORMAT)

    @property
    def display_name(self) -> str:
        return f"{self._login} @ {Session.fmt(self._time_in)}"

    def sort_key(self) -> tuple:
        return self._time_in, self._login

    def to_row(self) -> tuple:
        return self._login, Session.fmt(self._time_in), Session.fmt(self._time_out)

    @staticmethod
    def headers() -> tuple:
        return "login", "time_in", "time_out"

    def __len__(self) -> int:
        end = self._time_out or datetime.now()
        return int((end - self._time_in).total_seconds())

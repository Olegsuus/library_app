import csv
from datetime import datetime
from pathlib import Path

from app.models import Session, User


class SessionReport:
    HISTORY_FILE = "sessions.csv"
    REPORT_FILE = "report.txt"

    def __init__(self, directory: str | Path) -> None:
        self._directory = Path(directory)
        self._directory.mkdir(parents=True, exist_ok=True)
        self._current: Session | None = None

    @property
    def directory(self) -> Path:
        return self._directory

    @property
    def report_path(self) -> Path:
        return self._directory / SessionReport.REPORT_FILE

    @property
    def history_path(self) -> Path:
        return self._directory / SessionReport.HISTORY_FILE

    @property
    def current(self) -> Session | None:
        return self._current

    def start(self, user: User) -> Session:
        self._current = Session(user.login, datetime.now().replace(microsecond=0))
        return self._current

    def finish(self) -> Path:
        if self._current is None:
            raise RuntimeError("Сессия не была начата")
        if not self._current.is_closed:
            self._current.time_out = datetime.now().replace(microsecond=0)
        sessions = self.load_history()
        sessions.append(self._current)
        self._save_history(sessions)
        self.report_path.write_text(SessionReport.render(sessions), encoding="utf-8")
        return self.report_path

    def load_history(self) -> list[Session]:
        if not self.history_path.exists():
            return []
        with self.history_path.open(encoding="utf-8", newline="") as file:
            return [
                Session(row[0], Session.parse(row[1]), Session.parse(row[2]))
                for row in csv.reader(file, delimiter=";") if len(row) == 3
            ]

    def _save_history(self, sessions: list[Session]) -> None:
        with self.history_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            for session in sessions:
                writer.writerow(session.to_row())

    @staticmethod
    def render(sessions: list[Session]) -> str:
        headers = Session.headers()
        rows = [session.to_row() for session in sessions]
        widths = [
            max(len(headers[i]), *(len(row[i]) for row in rows)) + 2 if rows
            else len(headers[i]) + 2
            for i in range(len(headers))
        ]
        inner = sum(widths) + len(widths) - 1
        border = "+" + "-" * inner + "+"
        separator = "|" + "|".join("-" * w for w in widths) + "|"

        def line(cells: tuple) -> str:
            return "|" + "|".join(cell.center(w) for cell, w in zip(cells, widths)) + "|"

        parts = [border, line(headers), separator, *(line(row) for row in rows), border]
        return "\n".join(parts) + "\n"

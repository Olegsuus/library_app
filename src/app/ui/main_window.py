from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

from app.models import User
from app.services.library import Library
from app.services.report import SessionReport
from app.ui.books_tab import BooksTab
from app.ui.readers_tab import ReadersTab
from app.ui.widgets import AppLabel, AppStatusBar, AppTabWidget


class MainWindow(QMainWindow):
    def __init__(self, user: User, library: Library, report: SessionReport) -> None:
        super().__init__()
        self._user = user
        self._library = library
        self._report = report
        self.setWindowTitle(f"Библиотека — {user.login}")
        self.resize(1200, 720)
        self.setMinimumSize(1000, 600)
        self._build()
        self.update_status()

    @property
    def user(self) -> User:
        return self._user

    def _build(self) -> None:
        header = QHBoxLayout()
        header.addWidget(AppLabel("Учёт книг и читателей", role="title"))
        header.addStretch()
        header.addWidget(AppLabel(
            f"Пользователь: <b>{self._user.login}</b>", role="hint",
            align=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
        ))

        self.status = AppStatusBar()
        self.setStatusBar(self.status)

        self.tabs = AppTabWidget()
        self.books_tab = BooksTab(self._library, self.notify)
        self.readers_tab = ReadersTab(self._library, self.notify)
        self.tabs.addTab(self.books_tab, "Книги")
        self.tabs.addTab(self.readers_tab, "Читатели")

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 12, 16, 8)
        layout.addLayout(header)
        layout.addWidget(self.tabs)
        self.setCentralWidget(central)

    def notify(self, text: str, is_error: bool) -> None:
        if is_error:
            self.status.error(text)
        else:
            self.status.info(text)
        self.update_status()

    def update_status(self) -> None:
        self.status.set_permanent(str(self._library))

    def closeEvent(self, event: QCloseEvent) -> None:
        try:
            path = self._report.finish()
            print(f"Отчёт сохранён: {path}\n{path.read_text(encoding='utf-8')}", flush=True)
        except (OSError, RuntimeError) as error:
            print(f"Не удалось сохранить отчёт: {error}", flush=True)
        event.accept()

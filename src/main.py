import os
import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from app.services.library import Library
from app.services.report import SessionReport
from app.services.seed import Seeder
from app.ui.login_dialog import LoginDialog
from app.ui.main_window import MainWindow
from app.ui.styles import Theme


class Application:
    DEFAULT_REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"

    def __init__(self, argv: list[str]) -> None:
        self._qt = QApplication(argv)
        self._qt.setApplicationName("Библиотека")
        self._qt.setStyleSheet(Theme.STYLESHEET)
        self._report = SessionReport(Application.report_dir())
        self._library = Seeder.fill(Library())
        self._window: MainWindow | None = None

    @staticmethod
    def report_dir() -> Path:
        return Path(os.environ.get("REPORT_DIR", Application.DEFAULT_REPORT_DIR))

    def run(self) -> int:
        login = LoginDialog()
        login.exec()
        if login.user is None:
            return 0
        self._report.start(login.user)
        self._window = MainWindow(login.user, self._library, self._report)
        self._window.show()
        return self._qt.exec()


if __name__ == "__main__":
    sys.exit(Application(sys.argv).run())

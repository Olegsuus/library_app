from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QWidget

from app.models import User
from app.ui.widgets import AppButton, AppLabel, AppLineEdit


class LoginDialog(QDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._user: User | None = None
        self.setWindowTitle("Вход — Библиотека")
        self.setFixedSize(380, 230)
        self._build()

    @property
    def user(self) -> User | None:
        return self._user

    def _build(self) -> None:
        center = Qt.AlignmentFlag.AlignCenter
        self._title = AppLabel("Библиотека", role="title", align=center)
        self._hint = AppLabel("Введите логин, чтобы начать работу", role="hint", align=center)
        self._login = AppLineEdit("Логин, например librarian")
        self._error = AppLabel("", align=center, wrap=True)
        self._error.setStyleSheet("color: #ff8b84;")
        self._ok = AppButton("Войти", role="primary")
        self._cancel = AppButton("Отмена")
        self._ok.clicked.connect(self.try_login)
        self._cancel.clicked.connect(self.reject)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._cancel)
        buttons.addWidget(self._ok)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)
        layout.addWidget(self._title)
        layout.addWidget(self._hint)
        layout.addWidget(self._login)
        layout.addWidget(self._error)
        layout.addLayout(buttons)

    def try_login(self) -> None:
        try:
            self._user = User(self._login.text())
        except ValueError as error:
            self._error.setText(str(error))
            self._login.setFocus()
            return
        self.accept()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.try_login()
        else:
            super().keyPressEvent(event)

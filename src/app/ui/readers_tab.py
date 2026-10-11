"""Вкладка «Читатели»: список, регистрация, книги на руках."""
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout

from app.models import Reader
from app.services.library import Library
from app.ui.widgets import (
    AppButton, AppGroupBox, AppLabel, AppLineEdit, AppListWidget, AppTable, Dialogs,
)


class ReadersTab(QWidget):
    def __init__(self, library: Library, notify: Callable[[str, bool], None],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._library = library
        self._notify = notify
        self._build()
        self.refresh()

    def _build(self) -> None:
        self.table = AppTable(Reader.headers())
        self.table.itemSelectionChanged.connect(self._on_select)
        self.table.deleteRequested.connect(self.remove_reader)

        books_box = AppGroupBox("Книги на руках")
        self.books_list = AppListWidget()
        books_layout = QVBoxLayout(books_box)
        books_layout.addWidget(self.books_list)

        left = QVBoxLayout()
        left.addWidget(self.table, 3)
        left.addWidget(books_box, 2)

        form_box = AppGroupBox("Новый читатель")
        self.name_edit = AppLineEdit("Имя и фамилия")
        self.phone_edit = AppLineEdit("+7 900 000-00-00")
        self.btn_add = AppButton("Зарегистрировать", role="primary")
        self.btn_remove = AppButton("Удалить выбранного", role="danger")
        self.btn_add.clicked.connect(self.add_reader)
        self.btn_remove.clicked.connect(self.remove_reader)
        form = QFormLayout(form_box)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form.addRow("Имя:", self.name_edit)
        form.addRow("Телефон:", self.phone_edit)
        form.addRow(self.btn_add)

        self.info = AppLabel("", role="hint", wrap=True)
        self.info.setMinimumHeight(48)

        right = QVBoxLayout()
        right.addWidget(form_box)
        right.addWidget(self.btn_remove)
        right.addWidget(self.info)
        right.addStretch()
        right_panel = QWidget()
        right_panel.setLayout(right)
        right_panel.setFixedWidth(340)

        root = QHBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)
        root.addLayout(left, 1)
        root.addWidget(right_panel)

    def refresh(self) -> None:
        self.table.show_entities(list(self._library.readers))
        self._on_select()

    def _selected_reader(self) -> Reader | None:
        reader_id = self.table.selected_id()
        return self._library.get_reader(reader_id) if reader_id is not None else None

    def _on_select(self) -> None:
        reader = self._selected_reader()
        self.btn_remove.setEnabled(reader is not None)
        if reader is None:
            self.books_list.show_entities([], "Выберите читателя")
            self.info.setText(str(self._library))
            return
        self.books_list.show_entities(self._library.books_of(reader), "Книг на руках нет")
        self.info.setText(f"{reader}\nКниг на руках: {len(reader)}")

    def add_reader(self) -> None:
        try:
            reader = self._library.add_reader(Reader(self.name_edit.text(), self.phone_edit.text()))
        except ValueError as error:
            Dialogs.error(self, str(error))
            return
        self.name_edit.clear()
        self.phone_edit.clear()
        self.refresh()
        self._notify(f"Зарегистрирован читатель {reader}", False)

    def remove_reader(self) -> None:
        reader = self._selected_reader()
        if reader is None or not Dialogs.confirm(self, f"Удалить читателя {reader.name}?"):
            return
        try:
            self._library.remove_reader(reader.id)
        except ValueError as error:
            Dialogs.error(self, str(error))
            return
        self.refresh()
        self._notify(f"Удалён читатель {reader.name}", False)

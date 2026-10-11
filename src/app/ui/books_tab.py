from datetime import date
from typing import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QGridLayout

from app.models import Book
from app.services.library import Library
from app.ui.widgets import (
    AppButton, AppCheckBox, AppComboBox, AppGroupBox, AppLabel, AppLineEdit,
    AppSpinBox, AppTable, Dialogs,
)


class BookForm(AppGroupBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__("Карточка книги", parent)
        self.title_edit = AppLineEdit("Название")
        self.author_edit = AppLineEdit("Автор")
        self.year_spin = AppSpinBox(Book.MIN_YEAR, date.today().year, 2000)
        self.genre_combo = AppComboBox()
        self.genre_combo.setEditable(True)
        self.genre_combo.lineEdit().setPlaceholderText("Жанр (можно ввести новый)")

        form = QFormLayout(self)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        form.setFormAlignment(Qt.AlignmentFlag.AlignTop)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.addRow("Название:", self.title_edit)
        form.addRow("Автор:", self.author_edit)
        form.addRow("Год:", self.year_spin)
        form.addRow("Жанр:", self.genre_combo)

    def fill(self, book: Book | None) -> None:
        self.title_edit.setText(book.title if book else "")
        self.author_edit.setText(book.author if book else "")
        self.year_spin.setValue(book.year if book else 2000)
        self.genre_combo.setCurrentText(book.genre if book else "")

    def values(self) -> tuple:
        return (self.title_edit.text(), self.author_edit.text(),
                self.year_spin.value(), self.genre_combo.currentText())


class BooksTab(QWidget):
    def __init__(self, library: Library, notify: Callable[[str, bool], None],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._library = library
        self._notify = notify
        self._build()
        self.refresh()

    def _build(self) -> None:
        # фильтры
        self.search = AppLineEdit("Поиск по названию или автору…")
        self.genre_filter = AppComboBox()
        self.sort_combo = AppComboBox(tuple(label for label, _ in Library.SORT_MODES))
        self.only_available = AppCheckBox("Только в наличии")
        self.search.textChanged.connect(self.refresh)
        self.genre_filter.currentTextChanged.connect(self.refresh)
        self.sort_combo.currentIndexChanged.connect(self.refresh)
        self.only_available.toggled.connect(self.refresh)

        filters = QHBoxLayout()
        filters.addWidget(self.search, 3)
        filters.addWidget(self.genre_filter, 1)
        filters.addWidget(self.sort_combo, 1)
        filters.addWidget(self.only_available)

        # таблица
        self.table = AppTable(Book.headers())
        self.table.itemSelectionChanged.connect(self._on_select)
        self.table.deleteRequested.connect(self.delete_book)
        self.counter = AppLabel("", role="hint",
                                align=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        left = QVBoxLayout()
        left.addLayout(filters)
        left.addWidget(self.table)
        left.addWidget(self.counter)

        # правая панель: форма + действия + выдача
        self.form = BookForm()
        self.btn_add = AppButton("Добавить", role="primary")
        self.btn_save = AppButton("Сохранить")
        self.btn_clear = AppButton("Очистить")
        self.btn_delete = AppButton("Удалить", role="danger")
        self.btn_add.clicked.connect(self.add_book)
        self.btn_save.clicked.connect(self.save_book)
        self.btn_clear.clicked.connect(self.clear_selection)
        self.btn_delete.clicked.connect(self.delete_book)

        actions = QGridLayout()
        actions.addWidget(self.btn_add, 0, 0)
        actions.addWidget(self.btn_save, 0, 1)
        actions.addWidget(self.btn_clear, 1, 0)
        actions.addWidget(self.btn_delete, 1, 1)

        issue_box = AppGroupBox("Выдача и возврат")
        self.reader_combo = AppComboBox()
        self.btn_issue = AppButton("Выдать", role="primary")
        self.btn_return = AppButton("Вернуть")
        self.holder = AppLabel("Выберите книгу в таблице", role="hint", wrap=True)
        self.btn_issue.clicked.connect(self.issue_book)
        self.btn_return.clicked.connect(self.return_book)
        issue_layout = QGridLayout(issue_box)
        issue_layout.addWidget(AppLabel("Читатель:"), 0, 0)
        issue_layout.addWidget(self.reader_combo, 0, 1)
        issue_layout.addWidget(self.btn_issue, 1, 0)
        issue_layout.addWidget(self.btn_return, 1, 1)
        issue_layout.addWidget(self.holder, 2, 0, 1, 2)

        right = QVBoxLayout()
        right.addWidget(self.form)
        right.addLayout(actions)
        right.addWidget(issue_box)
        right.addStretch()

        right_panel = QWidget()
        right_panel.setLayout(right)
        right_panel.setFixedWidth(340)

        root = QHBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(12)
        root.addLayout(left, 1)
        root.addWidget(right_panel)

    # --- обновление представления ---
    def refresh(self) -> None:
        self.genre_filter.reset_items((Library.ALL_GENRES,) + self._library.genres)
        self.form.genre_combo.reset_items(self._library.genres)
        self.reader_combo.reset_items(tuple(r.name for r in self._library.readers))
        books = self._library.filter_books(
            self.search.text(), self.genre_filter.currentText(),
            self.only_available.isChecked(), self.sort_combo.currentIndex(),
        )
        self.table.show_entities(books)
        self.counter.setText(f"Показано {len(books)} из {len(self._library)}")
        self._on_select()

    def _selected_book(self) -> Book | None:
        book_id = self.table.selected_id()
        return self._library.get_book(book_id) if book_id is not None else None

    def _on_select(self) -> None:
        book = self._selected_book()
        has_book = book is not None
        for button in (self.btn_save, self.btn_delete):
            button.setEnabled(has_book)
        self.btn_issue.setEnabled(has_book and book.is_available)
        self.btn_return.setEnabled(has_book and not book.is_available)
        if not has_book:
            self.holder.setText("Выберите книгу в таблице")
            return
        self.form.fill(book)
        if book.is_available:
            self.holder.setText("Книга в наличии")
        else:
            self.holder.setText(f"На руках у: {self._library.get_reader(book.reader_id)}")

    def _reader_id_by_name(self, name: str) -> int:
        for reader in self._library.readers:
            if reader.name == name:
                return reader.id
        raise ValueError("Сначала выберите читателя")

    # --- действия ---
    def add_book(self) -> None:
        try:
            book = self._library.add_book(Book(*self.form.values()))
        except ValueError as error:
            Dialogs.error(self, str(error))
            return
        self.search.clear()
        self.refresh()
        self._notify(f"Добавлена книга {book}", False)

    def save_book(self) -> None:
        book = self._selected_book()
        if book is None:
            return
        try:
            self._library.update_book(book.id, *self.form.values())
        except ValueError as error:
            Dialogs.error(self, str(error))
            return
        self.refresh()
        self._notify(f"Сохранены изменения: {book}", False)

    def delete_book(self) -> None:
        book = self._selected_book()
        if book is None or not Dialogs.confirm(self, f"Удалить книгу {book}?"):
            return
        try:
            self._library.remove_book(book.id)
        except ValueError as error:
            Dialogs.error(self, str(error))
            return
        self.clear_selection()
        self._notify(f"Удалена книга {book}", False)

    def clear_selection(self) -> None:
        self.table.clearSelection()
        self.form.fill(None)
        self.refresh()

    def issue_book(self) -> None:
        book = self._selected_book()
        if book is None:
            return
        try:
            reader_id = self._reader_id_by_name(self.reader_combo.currentText())
            self._library.issue(book.id, reader_id)
        except ValueError as error:
            self._notify(str(error), True)
            return
        self.refresh()
        self._notify(f"Книга {book.display_name} выдана: {self._library.get_reader(reader_id).name}", False)

    def return_book(self) -> None:
        book = self._selected_book()
        if book is None:
            return
        try:
            reader = self._library.give_back(book.id)
        except ValueError as error:
            self._notify(str(error), True)
            return
        self.refresh()
        self._notify(f"{reader.name} вернул(а) книгу {book.display_name}", False)

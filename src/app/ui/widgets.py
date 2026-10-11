from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QCursor, QKeyEvent, QFocusEvent, QWheelEvent, QEnterEvent
from PyQt6.QtWidgets import (
    QPushButton, QLineEdit, QLabel, QComboBox, QSpinBox, QTableWidget,
    QTableWidgetItem, QListWidget, QListWidgetItem, QGroupBox, QCheckBox,
    QStatusBar, QTabWidget, QAbstractItemView, QHeaderView, QMessageBox, QWidget,
)


class AppButton(QPushButton):
    def __init__(self, text: str, role: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        if role:
            self.setProperty("role", role)
        self.setMinimumWidth(110)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        self.unsetCursor()
        super().leaveEvent(event)


class AppLineEdit(QLineEdit):
    def __init__(self, placeholder: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setClearButtonEnabled(True)

    def focusInEvent(self, event: QFocusEvent) -> None:
        super().focusInEvent(event)
        QTimer.singleShot(0, self.selectAll)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Escape:
            self.clear()
        else:
            super().keyPressEvent(event)


class AppLabel(QLabel):

    def __init__(self, text: str = "", role: str = "",
                 align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                 wrap: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        if role:
            self.setProperty("role", role)
        self.setAlignment(align)
        self.setWordWrap(wrap)


class AppComboBox(QComboBox):

    def __init__(self, items: tuple = (), parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.reset_items(items)

    def reset_items(self, items: tuple, keep_current: bool = True) -> None:
        current = self.currentText()
        self.blockSignals(True)
        self.clear()
        self.addItems(list(items))
        if keep_current and current in items:
            self.setCurrentText(current)
        self.blockSignals(False)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class AppSpinBox(QSpinBox):

    def __init__(self, minimum: int, maximum: int, value: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class AppTable(QTableWidget):
    deleteRequested = pyqtSignal()

    def __init__(self, headers: tuple, parent: QWidget | None = None) -> None:
        super().__init__(0, len(headers), parent)
        self.setHorizontalHeaderLabels(list(headers))
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_entities(self, entities: list) -> None:
        selected = self.selected_id()
        self.setRowCount(0)
        for entity in entities:
            row = self.rowCount()
            self.insertRow(row)
            for column, value in enumerate(entity.to_row()):
                item = QTableWidgetItem(value)
                if column != 1 and column != 2:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, column, item)
            if entity.id == selected:
                self.selectRow(row)

    def selected_id(self) -> int | None:
        rows = self.selectionModel().selectedRows() if self.selectionModel() else []
        if not rows:
            return None
        item = self.item(rows[0].row(), 0)
        return int(item.text()) if item else None

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.deleteRequested.emit()
        else:
            super().keyPressEvent(event)


class AppListWidget(QListWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAlternatingRowColors(True)

    def show_entities(self, entities: list, empty_text: str = "") -> None:
        selected = self.selected_id()
        self.clear()
        for entity in entities:
            item = QListWidgetItem(str(entity))
            item.setData(Qt.ItemDataRole.UserRole, entity.id)
            self.addItem(item)
            if entity.id == selected:
                self.setCurrentItem(item)
        if not entities and empty_text:
            placeholder = QListWidgetItem(empty_text)
            placeholder.setFlags(Qt.ItemFlag.NoItemFlags)
            self.addItem(placeholder)

    def selected_id(self) -> int | None:
        item = self.currentItem()
        return item.data(Qt.ItemDataRole.UserRole) if item else None


class AppGroupBox(QGroupBox):

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(title, parent)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def changeEvent(self, event) -> None:
        super().changeEvent(event)
        self.setWindowOpacity(1.0 if self.isEnabled() else 0.6)


class AppCheckBox(QCheckBox):

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.toggle()
        else:
            super().keyPressEvent(event)


class AppStatusBar(QStatusBar):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._permanent = AppLabel("", align=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.addPermanentWidget(self._permanent)

    def set_permanent(self, text: str) -> None:
        self._permanent.setText(text)

    def info(self, text: str) -> None:
        self.setStyleSheet("color: #a9adb8;")
        self.showMessage(text, 5000)

    def error(self, text: str) -> None:
        self.setStyleSheet("color: #ff8b84;")
        self.showMessage(text, 7000)


class AppTabWidget(QTabWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setDocumentMode(False)
        self.currentChanged.connect(self._on_changed)

    def _on_changed(self, index: int) -> None:
        widget = self.widget(index)
        refresh = getattr(widget, "refresh", None)
        if callable(refresh):
            refresh()


class Dialogs:
    @staticmethod
    def error(parent: QWidget, text: str) -> None:
        QMessageBox.critical(parent, "Ошибка", text)

    @staticmethod
    def confirm(parent: QWidget, text: str) -> bool:
        answer = QMessageBox.question(parent, "Подтверждение", text)
        return answer == QMessageBox.StandardButton.Yes

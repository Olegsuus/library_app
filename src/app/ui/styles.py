class Theme:
    ACCENT = "#4f8cff"
    DANGER = "#e5534b"
    SUCCESS = "#3fb950"

    STYLESHEET = """
    QWidget { background: #1e1f24; color: #e6e6e6; font-family: "DejaVu Sans"; font-size: 13px; }
    QMainWindow, QDialog { background: #1e1f24; }
    QGroupBox { border: 1px solid #3a3d46; border-radius: 8px; margin-top: 14px; padding: 12px 10px 10px 10px; font-weight: bold; }
    QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; color: #9fb8ff; }
    QLineEdit, QSpinBox, QComboBox { background: #2a2c33; border: 1px solid #3a3d46; border-radius: 6px; padding: 5px 8px; min-height: 22px; }
    QLineEdit:focus, QSpinBox:focus, QComboBox:focus { border: 1px solid #4f8cff; }
    QComboBox QAbstractItemView { background: #2a2c33; selection-background-color: #4f8cff; }
    QPushButton { background: #2f3340; border: 1px solid #454a59; border-radius: 6px; padding: 6px 14px; min-height: 22px; }
    QPushButton:hover { background: #3a4052; }
    QPushButton:disabled { color: #6b6f7a; background: #26282e; }
    QPushButton[role="primary"] { background: #4f8cff; border-color: #4f8cff; color: white; }
    QPushButton[role="primary"]:hover { background: #6a9dff; }
    QPushButton[role="danger"] { background: #4a2326; border-color: #e5534b; color: #ffb4ae; }
    QPushButton[role="danger"]:hover { background: #5c2a2e; }
    QTableWidget, QListWidget { background: #24262c; alternate-background-color: #282a31; border: 1px solid #3a3d46; border-radius: 6px; gridline-color: #33363e; }
    QTableWidget::item:selected, QListWidget::item:selected { background: #4f8cff; color: white; }
    QHeaderView::section { background: #2f3340; color: #c9d4ff; padding: 6px; border: none; border-right: 1px solid #3a3d46; font-weight: bold; }
    QTabWidget::pane { border: 1px solid #3a3d46; border-radius: 8px; top: -1px; }
    QTabBar::tab { background: #2a2c33; padding: 8px 20px; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; }
    QTabBar::tab:selected { background: #4f8cff; color: white; }
    QStatusBar { background: #17181c; color: #a9adb8; }
    QLabel[role="title"] { font-size: 20px; font-weight: bold; color: #ffffff; }
    QLabel[role="hint"] { color: #8b909c; }
    QCheckBox { spacing: 8px; }
    """

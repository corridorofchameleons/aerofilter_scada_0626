from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from core.settings import Settings


class ErrorWidget(QWidget):
    close_error = Signal()

    def __init__(
            self,
    ):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setContentsMargins(3,3,3,3)
        self.layout.setContentsMargins(0,0,0,0)
        self.setStyleSheet(f'''
            background-color: transparent;
            border: none;
        ''')
        self.label.setStyleSheet(f"""
            border-radius: 3px;
            color: {Settings.TEXT_COLOR};
            background-color: {Settings.ERROR_WIDGET_BACKGROUND_COLOR};
            font-size: {Settings.VALUE_BOX_TITLE_FONT_SIZE}px;
            font-weight: bold;
        """)
        self.setWindowOpacity(0.9)
        self.layout.addWidget(self.label)
        self.setFixedSize(Settings.ERROR_WIDGET_WIDTH, Settings.ERROR_WIDGET_HEIGHT)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setLayout(self.layout)
        self.label.setWordWrap(True)
        self.hide()

    def mousePressEvent(self, event, /):
        self.close_error.emit()
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from core.settings import Settings
from core.widgets.ui_widgets.clock_widget import ClockWidget
from app.ui.layouts.containers.menu_buttons import MenuButtons


class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('header')
        self.layout.setContentsMargins(20, 0, 20, 5)

        self.left_container = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_container.setLayout(self.left_layout)

        self.middle_container = QWidget()
        self.middle_layout = QVBoxLayout()
        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle_layout.setContentsMargins(0, 0, 0, 0)
        self.middle_container.setLayout(self.middle_layout)

        self.right_container = QWidget()
        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_container.setLayout(self.right_layout)

        self.company_name = QLabel('ООО Аэрофильтр')
        self.company_name.setStyleSheet(f'''
            color: #202020;
            font-size: {Settings.HEADER_FONT_SIZE * 1.2}px;
            font-weight: bold;
        ''')
        self.phone = QLabel('+74843979612')
        self.phone.setStyleSheet(f'''
            color: #202020;
            font-size: {Settings.HEADER_FONT_SIZE}px;
        ''')
        self.left_layout.addWidget(self.company_name)
        self.left_layout.addWidget(self.phone)

        self.title = QLabel('Установка для проверки топливных\nи масляных фильтров УТМ-АФ-25')
        self.title.setStyleSheet(f'''
            color: #202020;
            font-size: {Settings.HEADER_FONT_SIZE * 1.4}px;
            font-style: italic;
        ''')
        self.middle_layout.addWidget(self.title)

        self.menu_buttons = MenuButtons()
        self.clock_widget = ClockWidget()
        self.clock_widget.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.right_layout.addWidget(self.menu_buttons)
        self.right_layout.addWidget(self.clock_widget)

        self.layout.addWidget(self.left_container, stretch=1)
        self.layout.addWidget(self.middle_container, stretch=3)
        self.layout.addWidget(self.right_container, stretch=1)

        self.setLayout(self.layout)

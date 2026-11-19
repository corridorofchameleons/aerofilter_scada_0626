from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel

from core.settings import Settings
from core.widgets.ui_widgets.clock_widget import ClockWidget
from app.ui.layouts.containers.menu_buttons import MenuButtons

# LOGO_PATH = '../../../assets/logo.png'
LOGO_PATH = Path(__file__).resolve().parent.parent.parent.parent / 'assets' / 'logo.jpg'

class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('header')
        self.layout.setContentsMargins(0, 0, 20, 5)

        self.left_container = QWidget()
        self.left_layout = QHBoxLayout()
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

        self.logo_container = QWidget()
        self.logo_container.setFixedSize(100, 70)
        self.logo_layout = QVBoxLayout()
        self.logo_layout.setContentsMargins(0,0,0,0)
        self.logo_container.setLayout(self.logo_layout)
        logo = QLabel()
        pixmap = QPixmap(LOGO_PATH)
        logo.setPixmap(pixmap)
        logo.setScaledContents(True)
        self.logo_layout.addWidget(logo)
        # logo.setObjectName('logo')
        #
        # phone = QLabel('ООО Аэрофильтр\nтелефон:\n +7(484)397-96-42')
        # phone.setObjectName('phone')
        #
        # self.layout.addWidget(logo)
        # self.layout.addWidget(phone)

        self.info_container = QWidget()
        self.info_layout = QVBoxLayout()
        self.info_layout.setContentsMargins(10,0,0,0)
        self.info_container.setLayout(self.info_layout)
        self.company_name = QLabel('ООО АэроФильтр')
        self.company_name.setStyleSheet(f'''
            color: #202020;
            font-size: {Settings.HEADER_FONT_SIZE * 1.2}px;
            font-style: italic;
        ''')
        self.mail = QLabel('info@aerofiltr.ru')
        self.mail.setStyleSheet(f'''
            color: #202020;
            font-size: {Settings.HEADER_FONT_SIZE * 1.1}px;
            font-style: italic;
        '''
        )
        self.phone = QLabel('+7(484)397-96-12')
        self.phone.setStyleSheet(f'''
            color: #202020;
            font-size: {Settings.HEADER_FONT_SIZE * 1.1}px;
            font-style: italic;
        ''')
        self.info_layout.addWidget(self.company_name)
        self.info_layout.addWidget(self.mail)
        self.info_layout.addWidget(self.phone)

        self.left_layout.addWidget(self.logo_container)
        self.left_layout.addWidget(self.info_container)

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

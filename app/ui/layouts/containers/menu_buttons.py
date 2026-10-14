from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QApplication
from loguru import logger

from core.widgets.ui_widgets.button import BaseButton, Button


class MenuButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('menuButtons')
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.alarm_button = Button('Аварии', slot_function=self.open_alarms, size=3, custom=True)
        self.graph_button = Button('Графики', size=3, custom=True)
        self.report_button = Button('Отчеты', slot_function=self.open_reports, size=3, custom=True)
        self.settings_button = Button('Настройки', slot_function=self.open_settings, size=3, custom=True)
        self.exit_button = Button('Выход', slot_function=self.close_app, size=3, custom=True)

        self.layout.addWidget(self.alarm_button)
        self.layout.addWidget(self.graph_button)
        self.layout.addWidget(self.report_button)
        self.layout.addWidget(self.settings_button)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    @Slot()
    def open_alarms(self):
        logger.info('Opening alarms...')

    @Slot()
    def open_reports(self):
        logger.info('Opening reports...')

    @Slot()
    def open_settings(self):
        logger.info('Opening settings...')

    @Slot()
    def close_app(self):
        window = self.window()
        window.close()

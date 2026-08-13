from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QApplication

from widgets.ui_widgets.button import SCADAButton


class MenuButtons(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('menuButtons')
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.alarm_button = SCADAButton('Аварии', self.open_alarms, size=3)
        self.graph_button = SCADAButton('Графики', self.open_graphs, size=3)
        self.report_button = SCADAButton('Отчеты', self.open_reports, size=3)
        self.settings_button = SCADAButton('Настройки', self.open_settings, size=3)
        self.exit_button = SCADAButton('Выход', self.close_app, size=3)

        self.layout.addWidget(self.alarm_button)
        self.layout.addWidget(self.graph_button)
        self.layout.addWidget(self.report_button)
        self.layout.addWidget(self.settings_button)
        self.layout.addWidget(self.exit_button)

        self.setLayout(self.layout)

    @Slot()
    def open_alarms(self):
        print('opening alarms...')

    @Slot()
    def open_graphs(self):
        print('opening graphs...')

    @Slot()
    def open_reports(self):
        print('opening reports...')

    @Slot()
    def open_settings(self):
        print('opening settings...')

    @Slot()
    def close_app(self):
        print('closing app...')
        QApplication.instance().quit()

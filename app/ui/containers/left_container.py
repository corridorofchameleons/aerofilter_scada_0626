from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from app.instances.particles import Particles, OilTable, FuelTable
from app.instances.stands import MetaStand, OilStand
from app.ui.elements.particle_table import ParticleTable
from app.ui.elements.select_button import SideButton
from core.widgets.ui_widgets.button import SCADAButton, MenuButton
from core.widgets.ui_widgets.value_input import ValueInput


class LeftContainer(QWidget):
    choose_button_pressed = Signal()

    def __init__(
            self,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.button_container = QWidget()
        self.button_container_layout = QVBoxLayout()
        self.button_container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.button_container.setLayout(self.button_container_layout)

        self.oil_value_input = ValueInput(OilTable.oil_test_num, 'Количество\nизмерений масл')
        self.fuel_value_input = ValueInput(FuelTable.fuel_test_num, 'Количество\nизмерений топл')

        self.title_label = QLabel()
        self.title_label.setStyleSheet('''
            color: black;
            font-weight: bold;
        ''')
        self.title_label.setMinimumHeight(20)

        self.choose_button = MenuButton('Выбрать\nстенд', size=2)
        self.choose_button.pressed.connect(self.choose_stand)
        # self.choose_button.pressed.connect()
        self.button_container_layout.addWidget(self.choose_button)

        self.layout.addWidget(self.oil_value_input)
        self.layout.addWidget(self.fuel_value_input)
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.button_container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)

    @Slot()
    def choose_stand(self):
        self.choose_button.setDisabled(True)
        self.choose_button_pressed.emit()


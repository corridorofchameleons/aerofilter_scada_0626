from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

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
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.button_container = QWidget()
        self.button_container_layout = QVBoxLayout()
        self.button_container.setLayout(self.button_container_layout)

        self.oil_value_input = ValueInput(OilTable.oil_test_num, 'Количество\nизмерений', width=100, min_value=1, max_value=11, error_indicator=False)
        self.oil_value_input.hide()
        self.fuel_value_input = ValueInput(FuelTable.fuel_test_num, 'Количество\nизмерений', width=100, min_value=1, max_value=11, error_indicator=False)
        self.fuel_value_input.hide()

        self.title_box = QWidget()
        self.title_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.title_box_layout = QVBoxLayout()
        self.title_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = QLabel()
        self.title_label.setStyleSheet('''
            color: black;
            font-weight: bold;
        ''')
        self.title_label.setMinimumHeight(20)
        self.title_box_layout.addWidget(self.title_label)
        self.title_box.setLayout(self.title_box_layout)

        self.button_box = QWidget()
        self.button_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.button_box_layout = QVBoxLayout()
        self.button_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.button_box.setLayout(self.button_box_layout)

        self.button_box_layout.addWidget(self.oil_value_input)
        self.button_box_layout.addWidget(self.fuel_value_input)

        self.choose_button = MenuButton('Выбор\nстенда', width=100)
        self.test_before_button = MenuButton('Измерение\nдо', width=100)
        self.test_after_button = MenuButton('Измерение\nпосле', width=100)

        self.choose_button.pressed.connect(self.choose_stand)

        self.button_box_layout.addWidget(self.choose_button)
        self.button_box_layout.addWidget(self.test_before_button)
        self.button_box_layout.addWidget(self.test_after_button)

        self.layout.addWidget(self.title_box)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    @Slot()
    def choose_stand(self):
        self.choose_button.setDisabled(True)
        self.choose_button_pressed.emit()

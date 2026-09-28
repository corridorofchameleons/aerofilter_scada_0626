from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from app.instances.particles import Particles, OilTable, FuelTable
from app.ui.elements.particle_table import ParticleTable
from app.ui.elements.select_button import SideButton
from core.widgets.ui_widgets.button import MenuButton
from core.widgets.ui_widgets.value_box import ValueBox


class RightContainer(QWidget):

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

        self.oil_effectiveness_box = ValueBox(OilTable.oil_effectiveness, 'Эффективность\nфильтра', width=100, error_indicator=False)
        self.oil_effectiveness_box.hide()
        self.fuel_effectiveness_box = ValueBox(FuelTable.fuel_effectiveness, 'Эффективность\nфильтра', width=100, error_indicator=False)
        self.fuel_effectiveness_box.hide()

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

        self.button_box_layout.addWidget(self.oil_effectiveness_box)
        self.button_box_layout.addWidget(self.fuel_effectiveness_box)

        self.calculate_button = MenuButton('Рассчитать', width=100)
        self.new_test_button = MenuButton('Новое\nиспытание', width=100)
        self.report_button = MenuButton('Сформировать\nотчет', width=100)

        self.button_box_layout.addWidget(self.calculate_button)
        self.button_box_layout.addWidget(self.new_test_button)
        self.button_box_layout.addWidget(self.report_button)

        self.layout.addWidget(self.title_box)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)
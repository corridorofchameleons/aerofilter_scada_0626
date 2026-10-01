from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QStackedWidget

from app.instances.particles import OilTable, FuelTable, fuel_particles_dict, fuel_effectiveness_dict, \
    oil_particles_dict, oil_effectiveness_dict, oil_table_data_dict, fuel_table_data_dict
from core.signals.mqtt import bus
from core.widgets.ui_widgets.button import MenuButton, SwitchButton
from core.widgets.ui_widgets.value_box import ValueBox


class RightContainer(QWidget):

    def __init__(
            self,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,20,0)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        self.stacked_button_box = QStackedWidget()

        self.oil_button_box = QWidget()
        self.oil_button_box_layout = QVBoxLayout()
        self.oil_button_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.oil_effectiveness_box = ValueBox(OilTable.oil_effectiveness, 'Эффективность\nфильтра', width=100, error_indicator=False)
        self.oil_calculate_button = MenuButton('Рассчитать', width=100)
        self.oil_new_test_button = MenuButton('Новое\nиспытание', width=100)
        self.oil_new_test_button.pressed.connect(
            lambda: self.clear_table(oil_particles_dict | oil_effectiveness_dict | oil_table_data_dict))
        self.oil_report_button = MenuButton('Сформировать\nотчет', width=100)

        self.oil_button_box_layout.addWidget(self.oil_effectiveness_box)
        self.oil_button_box_layout.addWidget(self.oil_calculate_button)
        self.oil_button_box_layout.addWidget(self.oil_new_test_button)
        self.oil_button_box_layout.addWidget(self.oil_report_button)
        self.oil_button_box.setLayout(self.oil_button_box_layout)

        self.fuel_button_box = QWidget()
        self.fuel_button_box_layout = QVBoxLayout()
        self.fuel_button_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fuel_effectiveness_box = ValueBox(FuelTable.fuel_effectiveness, 'Эффективность\nфильтра', width=100,
                                          error_indicator=False)
        self.fuel_calculate_button = MenuButton('Рассчитать', width=100)
        self.fuel_new_test_button = MenuButton('Новое\nиспытание', width=100)
        self.fuel_new_test_button.pressed.connect(lambda: self.clear_table(fuel_particles_dict | fuel_effectiveness_dict | fuel_table_data_dict))
        self.fuel_report_button = MenuButton('Сформировать\nотчет', width=100)

        self.fuel_button_box_layout.addWidget(self.fuel_effectiveness_box)
        self.fuel_button_box_layout.addWidget(self.fuel_calculate_button)
        self.fuel_button_box_layout.addWidget(self.fuel_new_test_button)
        self.fuel_button_box_layout.addWidget(self.fuel_report_button)
        self.fuel_button_box.setLayout(self.fuel_button_box_layout)

        self.stacked_button_box.addWidget(self.oil_button_box)
        self.stacked_button_box.addWidget(self.fuel_button_box)
        self.stacked_button_box.addWidget(QLabel())

        self.layout.addWidget(self.stacked_button_box)

        self.setLayout(self.layout)

    @Slot()
    def clear_table(self, tags_to_clear):
        data = [{'name': name, 'value': None} for name in tags_to_clear]
        bus.mqtt_publish_multiple_signal.emit(data)

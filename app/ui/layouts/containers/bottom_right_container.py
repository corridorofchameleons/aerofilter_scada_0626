from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QStackedWidget

from app.instances.particles import OilTable, FuelTable, fuel_particles_dict, fuel_effectiveness_dict, \
    oil_particles_dict, oil_effectiveness_dict, oil_table_data_dict, fuel_table_data_dict
from core.models.tag import Tag
from core.signals.mqtt import bus
from core.widgets.ui_widgets.button import MenuButton, SwitchButton
from core.widgets.ui_widgets.value_box import ValueBox
from mock.mock import SET_TOPIC


class RightBottomContainer(QWidget):
    def __init__(
            self,
            effectiveness_tag: Tag,
            clear_data: dict,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 20, 20, 0)
        self.setMinimumHeight(self.height())

        self.effectiveness_tag = effectiveness_tag
        self.clear_data = clear_data

        self.button_box = QWidget()
        self.button_box_layout = QVBoxLayout()
        self.button_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.effectiveness_box = ValueBox(self.effectiveness_tag, 'Эффективность\nфильтра', width=100, error_indicator=False)
        self.calculate_button = MenuButton('Рассчитать', width=100)
        self.new_test_button = MenuButton('Новое\nиспытание', width=100)
        self.new_test_button.pressed.connect(
            lambda: self.clear_table(self.clear_data))
        self.report_button = MenuButton('Сформировать\nотчет', width=100)

        self.button_box_layout.addWidget(self.effectiveness_box)
        self.button_box_layout.addWidget(self.calculate_button)
        self.button_box_layout.addWidget(self.new_test_button)
        self.button_box_layout.addWidget(self.report_button)
        self.button_box.setLayout(self.button_box_layout)

        self.setLayout(self.layout)
        self.layout.addWidget(self.button_box)

    @Slot()
    def clear_table(self, tags_to_clear):
        tags = [tag for tag in tags_to_clear.values() if isinstance(tag, Tag)]

        data = [{'name': tag.name, 'value': tag.initial_value} for tag in tags]
        bus.mqtt_publish_multiple_signal.emit(data, SET_TOPIC)

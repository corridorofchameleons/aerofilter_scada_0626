from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsProxyWidget

from app.instances.stands import FuelStand, OilStand
from app.ui.layouts.scheme.scheme_layout import HEADER_OIL_X, HEADER_OIL_Y, HEADER_WIDTH, HEADER_HEIGHT, HEADER_FUEL_X, \
    HEADER_FUEL_Y
from app.ui.layouts.scheme.systems.scheme_header import SchemeHeader
from core.widgets.ui_widgets.button import SwitchButton


class SchemeHeaders(QWidget):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_header = SchemeHeader(title='Масляный стенд')
        self.oil_heater_button = SwitchButton('Нагрев\nСТОП', 'Нагрев\nСТАРТ', tag=OilStand.oil_tank_heater, size=1, error_widget=True)
        self.oil_pollutant_button = SwitchButton('Загрязнитель\nСТОП', 'Загрязнитель\nСТАРТ', tag=OilStand.oil_pollutant, size=1, error_widget=True)
        self.oil_cleaning_button = SwitchButton('Очистка\nСТОП', 'Очистка\nСТАРТ', tag=OilStand.oil_cleaning, size=1, error_widget=True)
        self.oil_pump_button = SwitchButton('Насос\nСТОП', 'Насос\nСТАРТ', tag=OilStand.oil_main_pump_start, size=1, error_widget=True)
        self.oil_light_button = SwitchButton('Освещение\nВЫКЛ', 'Освещение\nВКЛ', tag=OilStand.oil_light, size=1, error_widget=True)
        self.oil_header.button_box_layout.addWidget(self.oil_heater_button)
        self.oil_header.button_box_layout.addWidget(self.oil_pollutant_button)
        self.oil_header.button_box_layout.addWidget(self.oil_cleaning_button)
        self.oil_header.button_box_layout.addWidget(self.oil_pump_button)
        self.oil_header.button_box_layout.addWidget(self.oil_light_button)

        self.oil_header_proxy = QGraphicsProxyWidget()
        self.oil_header_proxy.setWidget(self.oil_header)
        self.oil_header_proxy.setPos(HEADER_OIL_X - 2, HEADER_OIL_Y)

        self.scene.addItem(self.oil_header_proxy)

        self.fuel_header = SchemeHeader(title='Топливный стенд')
        self.fuel_heater_button = SwitchButton('Нагрев\nСТОП', 'Нагрев\nСТАРТ', tag=FuelStand.fuel_tank_heater, size=1, error_widget=True)
        self.fuel_pollutant_button = SwitchButton('Загрязнитель\nСТОП', 'Загрязнитель\nСТАРТ', tag=FuelStand.fuel_pollutant, size=1, error_widget=True)
        self.fuel_cleaning_button = SwitchButton('Очистка\nСТОП', 'Очистка\nСТАРТ', tag=FuelStand.fuel_cleaning, size=1, error_widget=True)
        self.fuel_pump_button = SwitchButton('Насос\nСТОП', 'Насос\nСТАРТ', tag=FuelStand.fuel_main_pump_start, size=1, error_widget=True)
        self.fuel_light_button = SwitchButton('Освещение\nВЫКЛ', 'Освещение\nВКЛ', tag=FuelStand.fuel_light, size=1, error_widget=True)
        self.fuel_header.button_box_layout.addWidget(self.fuel_heater_button)
        self.fuel_header.button_box_layout.addWidget(self.fuel_pollutant_button)
        self.fuel_header.button_box_layout.addWidget(self.fuel_cleaning_button)
        self.fuel_header.button_box_layout.addWidget(self.fuel_pump_button)
        self.fuel_header.button_box_layout.addWidget(self.fuel_light_button)

        self.fuel_header_proxy = QGraphicsProxyWidget()
        self.fuel_header_proxy.setWidget(self.fuel_header)
        self.fuel_header_proxy.setPos(HEADER_FUEL_X - 2, HEADER_FUEL_Y)
        self.scene.addItem(self.fuel_header_proxy)

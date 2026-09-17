from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsProxyWidget

from app.instances.fuel_stand import FuelStand
from app.instances.oil_stand import OilStand
from app.ui.layouts.scheme_layout import HEADER_OIL_X, HEADER_OIL_Y, HEADER_WIDTH, HEADER_HEIGHT, HEADER_FUEL_X, \
    HEADER_FUEL_Y
from core.widgets.graphics.components.scheme_header import SchemeHeader
from core.widgets.ui_widgets.button import SCADAButton


class SchemeHeaders(QWidget):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_header = SchemeHeader(title='Масляный стенд', width=HEADER_WIDTH, height=HEADER_HEIGHT)
        self.oil_light_button = SCADAButton(OilStand.oil_light, 'Освещение\nВЫКЛ', 'Освещение\nВКЛ', size=2)
        self.oil_header.button_box_layout.addWidget(self.oil_light_button)

        self.oil_header_proxy = QGraphicsProxyWidget()
        self.oil_header_proxy.setWidget(self.oil_header)
        self.oil_header_proxy.setPos(HEADER_OIL_X, HEADER_OIL_Y)

        self.scene.addItem(self.oil_header_proxy)

        self.fuel_header = SchemeHeader(title='Топливный стенд', width=HEADER_WIDTH, height=HEADER_HEIGHT)
        self.fuel_light_button = SCADAButton(FuelStand.fuel_light, 'Освещение\nВЫКЛ', 'Освещение\nВКЛ')
        self.fuel_header.button_box_layout.addWidget(self.fuel_light_button)

        self.fuel_header_proxy = QGraphicsProxyWidget()
        self.fuel_header_proxy.setWidget(self.fuel_header)
        self.fuel_header_proxy.setPos(HEADER_FUEL_X, HEADER_FUEL_Y)
        self.scene.addItem(self.fuel_header_proxy)

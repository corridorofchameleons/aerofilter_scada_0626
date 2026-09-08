from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsProxyWidget

from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from app.data.tags.binary_tags import BinaryTags
from app.ui.layouts.scheme_layout import HEADER_OIL_X, HEADER_OIL_Y, HEADER_FUEL_X, HEADER_FUEL_Y
from core.widgets.graphics.components.scheme_header import SchemeHeader
from core.widgets.ui_widgets.button import SCADAButton


class SchemeHeaders(QWidget):
    def __init__(
            self,
            scene: QGraphicsScene
    ):
        super().__init__()
        self.scene = scene

        self.oil_header = SchemeHeader(title='Масляный стенд')
        self.oil_light_button = SCADAButton(BinaryTags.units.get(OilStand.light), 'Освещение\nВЫКЛ', 'Освещение\nВКЛ')
        self.oil_header.button_box_layout.addWidget(self.oil_light_button)

        self.oil_header_proxy = QGraphicsProxyWidget()
        self.oil_header_proxy.setWidget(self.oil_header)
        self.oil_header_proxy.setPos(HEADER_OIL_X, HEADER_OIL_Y)
        self.scene.addItem(self.oil_header_proxy)

        self.fuel_header = SchemeHeader(title='Топливный стенд')
        self.fuel_light_button = SCADAButton(BinaryTags.units.get(FuelStand.light), 'Освещение\nВЫКЛ', 'Освещение\nВКЛ')
        self.fuel_header.button_box_layout.addWidget(self.fuel_light_button)

        self.fuel_header_proxy = QGraphicsProxyWidget()
        self.fuel_header_proxy.setWidget(self.fuel_header)
        self.fuel_header_proxy.setPos(HEADER_FUEL_X, HEADER_FUEL_Y)
        self.scene.addItem(self.fuel_header_proxy)

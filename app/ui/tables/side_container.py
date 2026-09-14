from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from app.data.tags.binary_tags import BinaryTags
from core.connectors.topics import COMMAND_TOPIC
from core.widgets.ui_widgets.button import SCADAButton, BaseButton, MenuButton
from app.data.signals.mqtt import bus


class SideContainer(QWidget):
    def __init__(
            self,
            stand,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.stand = stand
        self.tag = BinaryTags.units.get(self.stand.name)
        if self.tag:
            self.tag.signal_fn.connect(self.set_is_active)

        self.text_active = 'Выбран'
        self.text_inactive = 'Выбрать'

        self.is_active = False
        self.button_text = self.text_inactive

        self.set_active_button = MenuButton(self.button_text, self.set_active_device, size=2)

        self.table_left = QLabel('table')

        self.layout.addWidget(self.set_active_button)
        self.layout.addWidget(self.table_left)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.setLayout(self.layout)

    @Slot(bool)
    def set_is_active(self, val: bool):

        if val:
            self.is_active = True
            self.set_active_button.setText(self.text_active)
            self.set_active_button.setDisabled(True)
        else:
            self.is_active = False
            self.set_active_button.setText(self.text_inactive)
            self.set_active_button.setDisabled(False)

    def set_active_device(self):
        bus.mqtt_publish_signal.emit(
            COMMAND_TOPIC,
            {
                'name': self.stand.name,
                'value': self.stand.num
            }
        )

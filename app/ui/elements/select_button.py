from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout

from core.widgets.ui_widgets.button import MenuButton


class SideButton(QWidget):
    def __init__(
            self,
            stand,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.stand = stand
        self.tag = self.stand.__dict__.get(self.stand.name)
        self.tag.update_ui.connect(self.update_ui)
        self.tag.timeout_error_signal.connect(self.handle_error)

        self.text_active = 'Выбран'
        self.text_inactive = 'Выбрать'

        self.is_active = False
        self.button_text = self.text_inactive

        self.set_active_button = MenuButton(self.button_text, self.set_active_device, size=2)
        self.layout.addWidget(self.set_active_button)

    @Slot()
    def update_ui(self):
        if self.tag.value:
            self.set_active_button.setText(self.text_active)
            self.set_active_button.setDisabled(True)
        else:
            self.set_active_button.setText(self.text_inactive)
            self.set_active_button.setDisabled(False)

    @Slot()
    def handle_error(self):
        if self.tag.value:
            self.set_active_button.setText(self.text_active)
            self.set_active_button.setDisabled(True)
        else:
            self.set_active_button.setText(self.text_inactive)
            self.set_active_button.setDisabled(False)

    def set_active_device(self):
        self.set_active_button.setDisabled(True)
        self.tag.set_value(self.stand.num)
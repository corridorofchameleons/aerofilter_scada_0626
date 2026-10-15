from PySide6.QtCore import Signal, Slot, Qt

from app.data.topics import SQL_TOPIC
from core.models.tag import Tag
from core.settings import Settings
from core.signals.mqtt import bus
from app.ui.components.tables.cells.table_cell import Cell


class ButtonCell(Cell):
    cleared_col = Signal(int)
    revalidate = Signal()

    def __init__(
            self,
            tag: Tag,
            enum_data: dict,
            col: int,
            calculate_index,
            victims=None,
            disconnect_signal=None
    ):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.enum_data = enum_data
        self.tag = tag
        self.tag.update_ui.connect(self.update_ui)
        self.fn = lambda: None
        self.mousePressEvent = self.handle_click
        self.col = col
        self.victims = victims
        self.bus = bus

        self.calculate_index = calculate_index

        self.disconnect_signal = disconnect_signal
        if self.disconnect_signal is not None:
            self.disconnect_signal.connect(self.disconnect)

    @Slot()
    def update_ui(self):
        self.calculate_index()
        d = self.enum_data.get(self.tag.value)
        if self.tag.value > 0:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            # if self.tag.value == 1:
            #     pass
            # elif self.tag.value == 2:
            #     for item in self.victims.values():
            #         item.value = None
            #         item.update_ui.emit()
        else:
            self.unsetCursor()

        if d is not None:
            title = d.get('title')
            color = d.get('color')

            self.setText(title)
            self.set_style(font_size=Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8, bg_color=color)

        self.revalidate.emit()

    def handle_click(self, event):
        if self.tag.value == 1:
            self.tag.set_value(2)
        elif self.tag.value == 2:
            col_names = [tag.name for tag in self.victims.values()]
            self.bus.mqtt_publish_multiple_signal.emit(col_names, SQL_TOPIC)
            self.tag.set_value(1)

    @Slot()
    def disconnect(self):
        self.tag.update_ui.disconnect(self.update_ui)
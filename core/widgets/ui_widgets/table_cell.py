from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel

from core.models.tag import Tag
from core.settings import Settings
from core.signals.mqtt import bus


class Cell(QLabel):
    def __init__(
            self,
            tag: Tag | None = None,
            text: str | None = None
    ):
        super().__init__()
        self.text = text

        if self.text is not None:
            self.setText(self.text)

        self.tag = tag
        if self.tag is not None:
            self.tag.update_ui.connect(self.update_ui)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        font = QFont()
        font.setBold(True)
        self.setFont(font)
        self.__highlight_cell(False)

        # if self.text is None:
        #     self.update_ui()

    @Slot()
    def update_ui(self):
        if self.tag and self.tag.value is not None:
            self.setText(str(self.tag.value))
        else:
            self.setText('')

        # if self.highlight_tag is not None:
        #     if self.highlight_tag.value == self.index:
        #         self.__highlight_cell(True)
        #     else:
        #         self.__highlight_cell(False)

    def __highlight_cell(self, val: bool = False, bg_color: str = None):
        if val:
            bgc = 'white'
        else:
            bgc = '#E9E9E9'
        font = Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.9
        bbc = 'silver'
        if bg_color is not None:
            bgc = bg_color
            bbc = 'dimgray'
            font = Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8
        self.setStyleSheet(f'''
            font-size: {font}px;
            border: none;
            border-left: 1px solid dimgray;
            border-bottom: 1px solid {bbc};
            background-color: {bgc};
        ''')

    # @Slot(int)
    # def highlight(self):
    #     if self.highlight_tag.value == self.index:
    #         self.__highlight_cell(True)
    #     else:
    #         self.__highlight_cell(False)

    def set_style(self, bgc: str):
        self.__highlight_cell(val=False, bg_color=bgc)


class EnumCell(Cell):
    cleared_col = Signal(int)
    revalidate = Signal()

    def __init__(
            self,
            tag: Tag,
            enum_data: dict,
            col: int,
            tests: dict,
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
        self.tests = tests
        self.victims = victims
        self.bus = bus

        self.disconnect_signal = disconnect_signal
        if self.disconnect_signal is not None:
            self.disconnect_signal.connect(self.disconnect)

        # self.update_ui()

    @Slot()
    def update_ui(self):
        d = self.enum_data.get(self.tag.value)
        if self.tag.value > 0:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            if self.tag.value == 1:
                self.tests[self.col] = True
            if self.tag.value == 2:
                for item in self.victims.values():
                    item.value = None
                    item.update_ui.emit()
                    self.tests[self.col] = False
            if self.tag.value > 2:
                print('you did the impossible')
                # self.bus.mqtt_publish_multiple_signal()

        else:
            self.unsetCursor()

        if d is not None:
            title = d.get('title')
            color = d.get('color')

            self.setText(title)
            self.set_style(color)

        self.revalidate.emit()

    def handle_click(self, event):
        if self.tag.value == 0:
            print('seems like you broke the system...')
        elif self.tag.value == 1:
            self.tag.set_value(2)
        elif self.tag.value == 2:
            for tag in self.victims.values():
                print(tag, tag.name, tag.value)
            col_names = [tag for tag in self.victims.values()]
            print(col_names)
            self.tag.set_value(1)

    @Slot()
    def disconnect(self):
        self.tag.update_ui.disconnect(self.update_ui)

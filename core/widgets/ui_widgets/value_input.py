from PySide6.QtCore import Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

from core.connectors.topics import COMMAND_TOPIC
from app.data.signals.mqtt import bus
from core.models.tag import Tag
from core.settings import Settings


class ValueInput(QWidget):
    class Size:
        _width = Settings.VALUE_BOX_WIDTH
        _height = Settings.VALUE_BOX_HEIGHT
        SMALL = (_width * 0.75, _height)
        NORMAL = (_width, _height)
        BIG = (_width * 1.5, _height)

    def __init__(
            self,
            tag: Tag,
            title: str,
            min_value: int | None = None,
            max_value: int | None = None,
            size: int = 2,
    ):
        super().__init__()

        self.tag = tag
        if self.tag:
            self.tag.signal_fn.connect(self.update_value)

        self.title = title
        self.value = '0'
        self.min_value = min_value
        self.max_value = max_value
        if self.min_value is not None:
            self.min_value = float(self.min_value)
        if self.max_value is not None:
            self.max_value = float(self.max_value)

        self._is_active = True

        self.error = ''

        match size:
            case 1:
                self.width, self.height = ValueInput.Size.SMALL
            case 2:
                self.width, self.height = ValueInput.Size.NORMAL
            case 3:
                self.width, self.height = ValueInput.Size.BIG
            case _:
                self.width, self.height = ValueInput.Size.NORMAL

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.title_label = QLabel(self.title)
        self._set_label_stylesheet(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_input = QLineEdit(self.value)
        self.value_input.setReadOnly(False)
        # self.value_input.setStyleSheet(f"""
        #     border: 3px solid {Settings.VALUE_BOX_BORDER_COLOR};
        #     color: {Settings.TEXT_COLOR};
        #     background-color: {Settings.VALUE_BOX_VALUE_BACKGROUND_COLOR};
        #     font-weight: bold;
        #     font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE}px;
        # """)
        self._set_input_stylesheet()
        self.value_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_input.setReadOnly(True)

        self.value_input.mouseDoubleClickEvent = self.on_double_click
        self.value_input.editingFinished.connect(self.set_input_value)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.value_input)

        self.setFixedSize(self.width, self.height)

    def _set_label_stylesheet(self, good: bool):
        if good:
            bgc = Settings.VALUE_BOX_TITLE_BACKGROUND_COLOR
            f_size = Settings.VALUE_BOX_VALUE_FONT_SIZE
        else:
            bgc = 'red'
            f_size = Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.5
        self.title_label.setStyleSheet(f"""
            border: 3px solid {Settings.VALUE_BOX_BORDER_COLOR};
            color: {Settings.TEXT_COLOR};
            background-color: {bgc};
            font-style: italic;
            border-bottom: none;
            font-size: {f_size}px;
        """)

    def _set_input_stylesheet(self):
        if self._is_active:
            c = Settings.TEXT_COLOR
            bgc = Settings.VALUE_BOX_VALUE_BACKGROUND_COLOR
        else:
            c = 'grey'
            bgc = 'lightgrey'
        self.value_input.setStyleSheet(f"""
            border: 3px solid {Settings.VALUE_BOX_BORDER_COLOR};
            color: {c};
            background-color: {bgc};
            font-weight: bold;
            font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE}px;
        """)

    def on_double_click(self, event):
        if not self._is_active:
            return
        self.title_label.setText(self.title)
        self._set_label_stylesheet(True)
        self.value_input.setReadOnly(False)
        self.value_input.selectAll()
        self.value_input.setFocus()

    def _get_error_text(self):
        text = f'Значение\nдолжно быть числом\n'
        if self.min_value:
            text += f'от {self.min_value}'
        if self.max_value:
            text += f'до {self.max_value}'
        return text

    def _validated_value(self, val):
        try:
            val = val.replace(',', '.')
            val = float(val)
            if self.min_value:
                if val < self.min_value:
                    self.error = self._get_error_text()
                    return None
            if self.max_value:
                if val > self.max_value:
                    self.error = self._get_error_text()
                    return None
            return val
        except ValueError:
            self.error = self._get_error_text()
            return None

    def set_input_value(self):
        self._is_active = False
        self._set_input_stylesheet()
        self.value_input.setReadOnly(True)
        val = self.value_input.text()
        validated_val = self._validated_value(val)
        if validated_val:
            bus.mqtt_publish_signal.emit(
                COMMAND_TOPIC,
                {
                    'name': self.tag.name,
                    'value': validated_val
                }
            )
        else:
            self.value_input.setText(self.value)
            self.value_input.setReadOnly(False)
            self._is_active = True
            self.title_label.setText(self.error)
            self._set_label_stylesheet(False)
            self._set_input_stylesheet()

    @Slot(float)
    def update_value(self, val: float):
        self._is_active = True
        self.value = str(val)
        self.value_input.setText(self.value)
        self._set_input_stylesheet()
        self.value_input.setReadOnly(False)

from PySide6.QtCore import Slot
from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

from core.models.tag import Tag
from core.settings import Settings
from core.widgets.ui_widgets.error_widget import ErrorWidget


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
            error_widget: bool | None = None,
            min_value: int | None = None,
            max_value: int | None = None,
            size: int = 2,
    ):
        super().__init__()

        self.tag = tag
        self.tag.update_ui.connect(self.update_ui)

        if error_widget:
            self.error_widget = ErrorWidget()

        self.title = title
        self.tag.value = 'n\\a'
        self.min_value = min_value
        self.max_value = max_value
        if self.min_value is not None:
            self.min_value = float(self.min_value)
        if self.max_value is not None:
            self.max_value = float(self.max_value)

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
        self._set_label_stylesheet()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_input = QLineEdit(self.tag.value)
        self._set_input_stylesheet()
        self.value_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_input.setReadOnly(True)

        self.value_input.mouseDoubleClickEvent = self.on_double_click
        self.value_input.editingFinished.connect(self.set_input_value)
        self.value_input.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        if self.error_widget:
            self.error_widget.close_error.connect(self.close_error)

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.value_input)

        self.setFixedSize(self.width, self.height)

    def _set_label_stylesheet(self):
        self.title_label.setStyleSheet(f"""
            border: 3px solid {Settings.VALUE_BOX_BORDER_COLOR};
            color: {Settings.TEXT_COLOR};
            background-color: {Settings.VALUE_BOX_TITLE_BACKGROUND_COLOR};
            font-style: italic;
            border-bottom: none;
            font-size: {Settings.VALUE_BOX_TITLE_FONT_SIZE}px;
        """)

    def _set_input_stylesheet(self):
        if not self.tag.disabled:
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
        if self.error_widget:
            self.error_widget.hide()
        if not self.tag.value:
            return
        self.value_input.setReadOnly(False)
        self.value_input.selectAll()

    def _get_error_text(self):
        text = f'Значение должно быть числом'
        if self.min_value:
            text += f' от {self.min_value}'
        if self.max_value:
            text += f' до {self.max_value}'
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
        if self.error_widget:
            self.error_widget.hide()

        self.value_input.setReadOnly(True)
        self._set_input_stylesheet()
        val = self.value_input.text()
        validated_val = self._validated_value(val)

        if validated_val:
            self.tag.set_disabled_value(True)
            self.tag.set_value(validated_val)
        else:
            self.value_input.setReadOnly(False)
            if self.error_widget:
                self.error_widget.label.setText(self.error)
            if self.error_widget:
                self.error_widget.show()

        self._set_input_stylesheet()


    @Slot()
    def update_ui(self):
        self.tag.set_disabled_value(False)
        self.value_input.setReadOnly(True)
        self.value_input.clearFocus()
        self.value_input.setText(str(self.tag.value))
        self._set_input_stylesheet()

    @Slot()
    def close_error(self):
        self.error_widget.hide()
        self.value_input.setText(self.tag.value)
        self.value_input.setReadOnly(True)
        self.value_input.clearFocus()

from PySide6.QtCore import Slot, Qt

from core.models.tag import Tag
from core.widgets.ui_widgets.error_widget import ErrorWidget


class Stateful:
    def __init__(
            self,
            tag: Tag | None = None,
            error_widget: bool = False
    ):
        self.tag = tag
        self.error_widget = error_widget

        if self.tag is not None:
            self.tag.update_ui.connect(self.update_ui)

        if self.error_widget:
            self.error_widget = ErrorWidget()
            if self.tag is not None:
                self.tag.timeout_error_signal.connect(self.handle_error)
            self.error_widget.close_error.connect(self.close_error)

    def set_new_status(self, val):
        if self.tag:
            self.tag.set_value(val)
            self.update_ui()

    @Slot()
    def update_ui(self):
        if self.tag.disabled or self.tag.pending:
            self.unsetCursor()
            self.update()
        else:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.update()

    @Slot(str)
    def handle_error(self, text: str):
        self.error_widget.label.setText(text)
        self.error_widget.show()

    @Slot()
    def close_error(self):
        self.error_widget.label.setText('')
        self.error_widget.hide()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

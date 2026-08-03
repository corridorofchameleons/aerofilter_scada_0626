from PySide6.QtGui import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit

from widgets.graphics.constants import VALUE_BOX_WIDTH, VALUE_BOX_HEIGHT


class ValueBox(QWidget):
    def __init__(
            self,
            title: str,
            editable: bool = False
    ):
        super().__init__()
        self.title = title
        self.value = '73.95'

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.title_label = QLabel(self.title)
        self.title_label.setObjectName('titleLabel')
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_label = QLineEdit(self.value)
        self.value_label.setReadOnly(True)
        self.value_label.setObjectName('valueLabel')
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

        self.setFixedSize(VALUE_BOX_WIDTH, VALUE_BOX_HEIGHT)
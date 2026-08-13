from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QApplication, QVBoxLayout

from widgets.ui_widgets.clock_widget import ClockWidget
from widgets.ui_widgets.menu_buttons import MenuButtons


class Header(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('header')
        self.layout.setContentsMargins(20, 0, 20, 5)

        self.right_container = QWidget()

        self.menu_buttons = MenuButtons()
        self.clock_widget = ClockWidget()
        self.clock_widget.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.right_layout = QVBoxLayout()
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.right_layout.addWidget(self.menu_buttons)
        self.right_layout.addWidget(self.clock_widget)

        self.right_container.setLayout(self.right_layout)

        self.layout.addStretch()
        self.layout.addWidget(self.right_container)

        self.setLayout(self.layout)

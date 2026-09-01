from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from pages.graph_dialog import GraphDialog
from widgets.graphics.scene import Scene
from widgets.ui_widgets.header import Header


class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName('mainPage')

        self.graph_dialog = None

        self.header = Header()
        self.header.menu_buttons.graph_button.clicked.connect(self.open_graph_modal)

        self.middle = QWidget()
        self.middle_layout = QHBoxLayout()
        self.scene = Scene()
        self.table_left = QLabel('left')
        self.table_right = QLabel('right')

        self.middle_layout.addWidget(self.table_left)
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.scene)
        self.middle_layout.addStretch()
        self.middle_layout.addWidget(self.table_right)

        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.middle.setLayout(self.middle_layout)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.middle)


    @Slot()
    def open_graph_modal(self):
        if not self.graph_dialog:
            self.graph_dialog = GraphDialog(self)

        if self.graph_dialog:
            if self.graph_dialog.isMinimized():
                self.graph_dialog.showNormal()
            else:
                screen_center = self.frameGeometry().center()
                self.graph_dialog.move(screen_center)

                geo = self.graph_dialog.frameGeometry()
                geo.moveCenter(screen_center)
                self.graph_dialog.move(geo.topLeft())
                self.graph_dialog.show()

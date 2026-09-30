from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from core.widgets.ui_widgets.button import SwitchButton, MenuButton
from core.widgets.ui_widgets.value_input import ValueInput


class LeftContainer(QWidget):
    choose_button_pressed = Signal()

    def __init__(
            self,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.layout.setContentsMargins(20,0,0,0)

        self.button_container = QWidget()
        self.button_container_layout = QVBoxLayout()
        self.button_container.setLayout(self.button_container_layout)

        self.value_input = ValueInput(
            tag=None,
            title='Количество\nизмерений',
            width=100,
            min_value=1,
            max_value=11,
            error_indicator=False
        )

        self.title_box = QWidget()
        self.title_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.title_box_layout = QVBoxLayout()
        self.title_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label = QLabel()
        self.title_label.setStyleSheet('''
            color: black;
            font-weight: bold;
        ''')
        self.title_label.setMinimumHeight(20)
        self.title_box_layout.addWidget(self.title_label)
        self.title_box.setLayout(self.title_box_layout)

        self.button_box = QWidget()
        self.button_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.button_box_layout = QVBoxLayout()
        self.button_box_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.button_box.setLayout(self.button_box_layout)

        self.button_box_layout.addWidget(self.value_input)

        self.choose_button = MenuButton('Выбор\nстенда', width=100)
        self.test_before_button = SwitchButton(
            tag=None,
            text_active='Измерение\nдо',
            text_inactive='Измерение\nдо',
            width=100
        )
        self.test_after_button = SwitchButton(
            tag=None,
            text_active='Измерение\nпосле',
            text_inactive='Измерение\nпосле',
            width=100
        )

        self.choose_button.pressed.connect(self.choose_stand)

        self.button_box_layout.addWidget(self.choose_button)
        self.button_box_layout.addWidget(self.test_before_button)
        self.button_box_layout.addWidget(self.test_after_button)

        self.layout.addWidget(self.title_box)
        self.layout.addWidget(self.button_box)

        self.setLayout(self.layout)

    @Slot()
    def choose_stand(self):
        self.choose_button.setDisabled(True)
        self.choose_button_pressed.emit()

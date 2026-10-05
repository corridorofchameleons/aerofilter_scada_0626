from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QStackedWidget, QLayout

from app.instances.particles import OilTable, FuelTable
from core.models.tag import Tag
from core.widgets.ui_widgets.button import SwitchButton, MenuButton, IncrementButton
from core.widgets.ui_widgets.value_input import ValueInput


class LeftBottomContainer(QWidget):
    def __init__(
            self,
            before_index: Tag,
            after_index: Tag,
            test_num: Tag,
            select_before: Tag,
            select_after: Tag,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.layout.setContentsMargins(20,0,0,0)

        self.before_index = before_index
        self.after_index = after_index
        self.test_num = test_num
        self.select_before = select_before
        self.select_after = select_after

        self.test_num.update_ui.connect(self.disable_button)
        self.before_index.update_ui.connect(self.disable_button)
        self.after_index.update_ui.connect(self.disable_button)
        self.select_before.update_ui.connect(self.disable_button)
        self.select_after.update_ui.connect(self.disable_button)

        self.button_box = QWidget()
        self.button_box_layout = QVBoxLayout()
        self.button_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.value_input = ValueInput(
            tag=test_num,
            title='Количество\nизмерений',
            width=100,
            min_value=1,
            max_value=11,
            error_indicator=False
        )
        self.test_before_button = IncrementButton(
            tag=self.select_before,
            text_active='Измерение\nдо',
            text_inactive='Измерение\nдо',
            width=100,
            extra_field=('index', self.before_index),
        )
        self.test_after_button = IncrementButton(
            tag=self.select_after,
            text_active='Измерение\nпосле',
            text_inactive='Измерение\nпосле',
            width=100,
            extra_field=('index', self.after_index),
        )

        self.button_box_layout.addWidget(self.value_input)
        self.button_box_layout.addWidget(self.test_before_button)
        self.button_box_layout.addWidget(self.test_after_button)
        self.button_box.setLayout(self.button_box_layout)

        #TODO delete this
        self.start_test = SwitchButton(
            tag=None,
            text_active='Делаем',
            text_inactive='Сделать',
            width=100
        )
        self.start_test.pressed.connect(lambda: self.start_test_process(self.test_before_button.tag, self.test_after_button.tag))
        self.button_box_layout.addWidget(self.start_test)

        self.layout.addWidget(self.button_box)
        self.setLayout(self.layout)

    @Slot()
    def disable_button(self):
        if self.before_index.value >= self.test_num.value:
            self.test_before_button.tag.disable_ui.emit()
        else:
            self.test_before_button.update_ui()

        if self.after_index.value >= self.test_num.value:
            self.test_after_button.set_force_disabled()
        else:
            self.test_after_button.update_ui()

    #TODO delete this
    @Slot()
    def start_test_process(self, tag_before: Tag, tag_after: Tag):
        if tag_before.value:
            name = tag_before.name
            prefix = name.split('_')[0]
            str_tag = f'{prefix}_test_before'
        elif tag_after.value:
            name = tag_after.name
            prefix = name.split('_')[0]
            str_tag = f'{prefix}_test_after'
        else:
            print('no test mode selected')
            return

        from core.signals.mqtt import bus
        bus.mqtt_publish_signal.emit({
            'name': str_tag,
            'value': None
        })

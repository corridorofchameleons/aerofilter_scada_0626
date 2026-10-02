from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy, QStackedWidget, QLayout

from app.instances.particles import OilTable, FuelTable
from core.models.tag import Tag
from core.widgets.ui_widgets.button import SwitchButton, MenuButton
from core.widgets.ui_widgets.value_input import ValueInput


class LeftContainer(QWidget):
    def __init__(
            self,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.layout.setContentsMargins(20,0,0,0)

        self.stacked_button_box = QStackedWidget()

        self.oil_button_box = QWidget()
        self.oil_button_box_layout = QVBoxLayout()
        self.oil_button_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.oil_value_input = ValueInput(
            tag=OilTable.oil_test_num,
            title='Количество\nизмерений',
            width=100,
            min_value=1,
            max_value=11,
            error_indicator=False
        )
        self.oil_test_before_button = SwitchButton(
            tag=OilTable.oil_select_before,
            text_active='Измерение\nдо',
            text_inactive='Измерение\nдо',
            width=100,
            extra_field=('index', OilTable.oil_before_index)
        )
        self.oil_test_after_button = SwitchButton(
            tag=OilTable.oil_select_after,
            text_active='Измерение\nпосле',
            text_inactive='Измерение\nпосле',
            width=100,
            extra_field=('index', OilTable.oil_after_index)
        )

        self.oil_button_box_layout.addWidget(self.oil_value_input)
        self.oil_button_box_layout.addWidget(self.oil_test_before_button)
        self.oil_button_box_layout.addWidget(self.oil_test_after_button)
        self.oil_button_box.setLayout(self.oil_button_box_layout)

        #TODO delete this
        self.oil_start_test = SwitchButton(
            tag=None,
            text_active='Делаем',
            text_inactive='Сделать',
            width=100
        )
        self.oil_start_test.pressed.connect(lambda: self.start_test_process(self.oil_test_before_button.tag, self.oil_test_after_button.tag))
        self.oil_button_box_layout.addWidget(self.oil_start_test)

        self.fuel_button_box = QWidget()
        self.fuel_button_box_layout = QVBoxLayout()
        self.fuel_button_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fuel_value_input = ValueInput(
            tag=FuelTable.fuel_test_num,
            title='Количество\nизмерений',
            width=100,
            min_value=1,
            max_value=11,
            error_indicator=False
        )
        self.fuel_test_before_button = SwitchButton(
            tag=FuelTable.fuel_select_before,
            text_active='Измерение\nдо',
            text_inactive='Измерение\nдо',
            width=100,
            extra_field=('index', FuelTable.fuel_before_index)
        )
        self.fuel_test_after_button = SwitchButton(
            tag=FuelTable.fuel_select_after,
            text_active='Измерение\nпосле',
            text_inactive='Измерение\nпосле',
            width=100,
            extra_field=('index', FuelTable.fuel_after_index)
        )

        self.fuel_button_box_layout.addWidget(self.fuel_value_input)
        self.fuel_button_box_layout.addWidget(self.fuel_test_before_button)
        self.fuel_button_box_layout.addWidget(self.fuel_test_after_button)
        self.fuel_button_box.setLayout(self.fuel_button_box_layout)

        # TODO delete this
        self.fuel_start_test = SwitchButton(
            tag=None,
            text_active='Делаем',
            text_inactive='Сделать',
            width=100
        )
        self.fuel_start_test.pressed.connect(
            lambda: self.start_test_process(self.fuel_test_before_button.tag, self.fuel_test_after_button.tag))
        self.fuel_button_box_layout.addWidget(self.fuel_start_test)

        self.stacked_button_box.addWidget(self.oil_button_box)
        self.stacked_button_box.addWidget(self.fuel_button_box)
        self.stacked_button_box.addWidget(QLabel())

        self.layout.addWidget(self.stacked_button_box)

        self.setLayout(self.layout)

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

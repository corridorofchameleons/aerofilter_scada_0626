from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout

from app.data.topics import SET_TOPIC
from app.instances.particles import oil_particle_dict_data, TEST_NUM
from app.ui.layouts.containers.bottom_left_container import LeftBottomContainer
from app.ui.layouts.containers.bottom_right_container import RightBottomContainer
from app.ui.components.tables.particle_table import PartTable
from core.models.tag import Tag
from core.signals.mqtt import bus


class BottomSection(QWidget):
    def __init__(
            self,
            test_num: Tag,
            select_before: Tag,
            select_after: Tag,
            effectiveness: Tag,
            particle_data: dict,
            clear_data: dict,
            before_index_tag: Tag,
            after_index_tag: Tag
    ):
        super().__init__()

        self.test_num = test_num
        self.select_before = select_before
        self.select_after = select_after
        self.effectiveness = effectiveness

        # self.select_before.update_ui.connect(self.update_before_button)
        # self.select_after.update_ui.connect(self.update_after_button)
        self.before_button_disabled = False
        self.after_button_disabled = False

        self.bus = bus

        self.particle_data = particle_data
        self.clear_data = clear_data

        self.before_index = before_index_tag
        self.after_index = after_index_tag

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(800, 100)

        self.table_box = QWidget()
        self.table_box_layout = QVBoxLayout()
        self.table_box_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.table_box_layout.setContentsMargins(0,0,0,0)

        self.table = PartTable(
            num_tag=self.test_num,
            tags=self.particle_data,
            calculate_index=self.calculate_index,
         )

        self.table_box.setLayout(self.table_box_layout)
        self.table_box_layout.addWidget(self.table)

        self.left_container = LeftBottomContainer(
            test_num=self.test_num,
            select_before=self.select_before,
            select_after=self.select_after,
        )

        self.left_container.test_before_button.pressed.connect(
            lambda: self.handle_clicked(1))
        self.left_container.test_before_button.tag.update_ui.connect(
            lambda: self.update_button(1)
        )
        self.left_container.test_after_button.pressed.connect(
            lambda: self.handle_clicked(2))
        self.left_container.test_after_button.tag.update_ui.connect(
            lambda: self.update_button(2)
        )

        self.right_container = RightBottomContainer(
            effectiveness_tag=self.effectiveness,
            clear_data=self.clear_data
        )

        self.layout.addWidget(self.left_container, stretch=1)
        self.layout.addWidget(self.table_box, stretch=4)
        self.layout.addWidget(self.right_container, stretch=1)

        self.setLayout(self.layout)

    @Slot()
    def calculate_index(self, pos: int):
        if pos == 1:
            tag = self.before_index
            button = self.left_container.test_before_button
        elif pos == 2:
            tag = self.after_index
            button = self.left_container.test_after_button
        else:
            return

        index = TEST_NUM
        for col, items in self.particle_data.items():
            data = items.get(pos)
            index_tag = data.get('index')
            index_status = index_tag.value
            if index_status in (0,2):
                if col < index:
                    index = col

        if index > self.test_num.value:
            button.setDisabled(True)
            if pos == 1:
                self.before_button_disabled = True
            elif pos == 2:
                self.after_button_disabled = True
        else:
            button.setDisabled(False)
            if pos == 1:
                self.before_button_disabled = False
            elif pos == 2:
                self.after_button_disabled = False

        tag.value = index
        self.bus.mqtt_publish_signal.emit({'name': tag.name, 'value': tag.value}, SET_TOPIC)

    @Slot()
    def update_button(self, pos: int):
        if pos == 1:
            button = self.left_container.test_before_button
            disabled = self.before_button_disabled
        elif pos == 2:
            button = self.left_container.test_after_button
            disabled = self.after_button_disabled
        else:
            return

        button.setText(button.text_active if button.tag.value else button.text_inactive)
        button.set_style(not button.tag.value)
        if not disabled:
            button.setDisabled(False)

    @Slot()
    def handle_clicked(self, pos: int):
        if pos == 1:
            index = self.before_index.value
            button = self.left_container.test_before_button
        elif pos == 2:
            index = self.after_index.value
            button = self.left_container.test_after_button
        else:
            return

        button.setDisabled(True)

        self.bus.mqtt_publish_signal.emit({
            'name': button.tag.name,
            'value': not button.tag.value,
            'index': index
        }, SET_TOPIC)

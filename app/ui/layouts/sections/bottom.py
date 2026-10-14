from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout
from loguru import logger

from app.data.topics import SET_TOPIC, SET_LIST_TOPIC
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

        self.left_container.test_after_button.pressed.connect(
            lambda: self.handle_clicked(2))

        self.right_container = RightBottomContainer(
            effectiveness_tag=self.effectiveness,
            clear_data=self.clear_data
        )

        self.layout.addWidget(self.left_container, stretch=1)
        self.layout.addWidget(self.table_box, stretch=4)
        self.layout.addWidget(self.right_container, stretch=1)

        self.setLayout(self.layout)
        self.table.compose_table()

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
            button.set_disabled(True)
        else:
            button.set_disabled(False)

        tag.value = index
        logger.info(f'Setting value: {tag.value} for tag: {tag.name}. Will not return as a result')
        self.bus.mqtt_publish_signal.emit({'name': tag.name, 'value': tag.value}, SET_TOPIC)

    @Slot()
    def handle_clicked(self, pos: int):
        if pos == 1:
            index = self.before_index
            button = self.left_container.test_before_button
        elif pos == 2:
            index = self.after_index
            button = self.left_container.test_after_button
        else:
            return

        button.setDisabled(True)

        logger.info(f'Setting index: {index.value} for tag: {button.tag.name}')
        self.bus.mqtt_publish_multiple_signal.emit([{
                'ns_name': button.tag.ns_name,
                'name': button.tag.name,
                'value': not button.tag.value
            },
            {
                'ns_name': index.ns_name,
                'name': index.name,
                'value': index.value,
            }
        ], SET_LIST_TOPIC)

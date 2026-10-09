from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout

from app.data.topics import SET_TOPIC
from app.instances.particles import oil_particle_dict_data
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
            clear_tests: Tag,
            particle_data: dict,
            clear_data: dict
    ):
        super().__init__()

        self.test_num = test_num
        self.select_before = select_before
        self.select_after = select_after
        self.effectiveness = effectiveness
        self.clear_tests = clear_tests

        self.bus = bus

        self.particle_data = particle_data
        self.clear_data = clear_data

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
            clear_tag=self.clear_tests,
        )

        self.table_box.setLayout(self.table_box_layout)
        self.table_box_layout.addWidget(self.table)

        self.left_container = LeftBottomContainer(
            test_num=self.test_num,
            select_before=self.select_before,
            select_after=self.select_after,
            revalidate_before=self.table.revalidate_before,
            revalidate_after=self.table.revalidate_after,
        )

        self.left_container.test_before_button.pressed.connect(
            lambda: self.handle_clicked(self.left_container.test_before_button.tag, 1))
        self.left_container.test_after_button.pressed.connect(
            lambda: self.handle_clicked(self.left_container.test_after_button.tag, 2))

        self.right_container = RightBottomContainer(
            effectiveness_tag=self.effectiveness,
            clear_data=self.clear_data
        )

        self.layout.addWidget(self.left_container, stretch=1)
        self.layout.addWidget(self.table_box, stretch=4)
        self.layout.addWidget(self.right_container, stretch=1)

        self.setLayout(self.layout)

    @Slot()
    def handle_clicked(self, tag: Tag, col_index: int):
        tag.set_disabled_value(True)
        index = 1
        for col, items in self.particle_data.items():
            data = items.get(col_index)
            index_tag = data.get('index')
            index_status = index_tag.value
            if index_status in (0,2):
                index = col
                break

        self.bus.mqtt_publish_signal.emit({
            'name': tag.name,
            'value': not tag.value,
            'index': index
        }, SET_TOPIC)

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout

from app.ui.layouts.containers.bottom_left_container import LeftBottomContainer
from app.ui.layouts.containers.bottom_right_container import RightBottomContainer
from app.ui.components.tables.particle_table import PartTable
from core.models.tag import IntTag, BoolTag, FloatTag, Tag
from core.settings import Settings
from core.signals.mqtt import bus


class BottomSection(QWidget):
    def __init__(
            self,
            test_num: IntTag,
            before_index: IntTag,
            after_index: IntTag,
            select_before: BoolTag,
            select_after: BoolTag,
            effectiveness: FloatTag,
            clear_tests: BoolTag,
            particle_data: dict,
            clear_data: dict
    ):
        super().__init__()

        self.test_num = test_num
        self.before_index = before_index
        self.after_index = after_index
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
            index_before_tag=self.before_index,
            index_after_tag=self.after_index
        )

        self.table_box.setLayout(self.table_box_layout)
        self.table_box_layout.addWidget(self.table)

        self.left_container = LeftBottomContainer(
            test_num=self.test_num,
            select_before=self.select_before,
            select_after=self.select_after,
            tests_before=self.table.tests_before,
            tests_after=self.table.tests_after,
            revalidate_before=self.table.revalidate_before,
            revalidate_after=self.table.revalidate_after
        )

        self.left_container.test_before_button.pressed.connect(
            lambda: self.handle_clicked(self.left_container.test_before_button.tag, self.table.tests_before.items()))
        self.left_container.test_after_button.pressed.connect(
            lambda: self.handle_clicked(self.left_container.test_after_button.tag, self.table.tests_after.items()))

        self.right_container = RightBottomContainer(
            effectiveness_tag=self.effectiveness,
            clear_data=self.clear_data
        )
        # self.right_container.clear_tests.connect(self.clear_tests)

        self.layout.addWidget(self.left_container, stretch=1)
        self.layout.addWidget(self.table_box, stretch=4)
        self.layout.addWidget(self.right_container, stretch=1)

        self.setLayout(self.layout)

    # @Slot()
    # def clear_tests(self):
    #     self.table.clear_tests()

    @Slot()
    def handle_clicked(self, tag: Tag, items: list):
        print(items)
        tag.set_force_disabled_value(True)
        index = 1
        for test, val in items:
            if not val:
                index = test
                break
        print(index)
        self.bus.mqtt_publish_signal.emit({
            'name': tag.name,
            'value': not tag.value,
            'index': index
        })

    # @Slot()
    # def handle_current_state(self):
    #     if self.before_index.value >= self.test_num.value:
    #         self.left_container.test_before_button.tag.disable_ui.emit()
    #     else:
    #         self.left_container.test_before_button.update_ui()
    #
    #     if self.after_index.value >= self.test_num.value:
    #         self.left_container.test_after_button.set_force_disabled()
    #     else:
    #         self.left_container.test_after_button.update_ui()

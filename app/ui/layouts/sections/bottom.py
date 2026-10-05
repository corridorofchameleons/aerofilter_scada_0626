from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout

from app.ui.layouts.containers.bottom_left_container import LeftBottomContainer
from app.ui.layouts.containers.bottom_right_container import RightBottomContainer
from app.ui.components.tables.particle_table import PartTable
from core.models.tag import IntTag, BoolTag, FloatTag
from core.settings import Settings


class BottomSection(QWidget):
    def __init__(
            self,
            test_num: IntTag,
            before_index: IntTag,
            after_index: IntTag,
            select_before: BoolTag,
            select_after: BoolTag,
            effectiveness: FloatTag,
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

        self.particle_data = particle_data
        self.clear_data = clear_data

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.left_container = LeftBottomContainer(
            before_index=self.before_index,
            after_index=self.after_index,
            test_num=self.test_num,
            select_before=self.select_before,
            select_after=self.select_after
        )

        self.table_box = QWidget()
        self.table_box.setFixedWidth(Settings.SCENE_WIDTH)
        self.table_box_layout = QVBoxLayout()

        self.table = PartTable(
            num_tag=self.test_num,
            tags=self.particle_data,
            index_before_tag=self.before_index,
            index_after_tag=self.after_index
        )

        self.table_box.setLayout(self.table_box_layout)
        self.table_box_layout.addWidget(self.table)

        self.right_container = RightBottomContainer(
            effectiveness_tag=self.effectiveness,
            clear_data=self.clear_data
        )

        self.layout.addWidget(self.left_container, stretch=1)
        self.layout.addWidget(self.table_box, stretch=4)
        self.layout.addWidget(self.right_container, stretch=1)

        self.setLayout(self.layout)

    @Slot()
    def handle_current_state(self):
        if self.before_index.value >= self.test_num.value:
            self.left_container.test_before_button.tag.disable_ui.emit()
        else:
            self.left_container.test_before_button.update_ui()

        if self.after_index.value >= self.test_num.value:
            self.left_container.test_after_button.set_force_disabled()
        else:
            self.left_container.test_after_button.update_ui()

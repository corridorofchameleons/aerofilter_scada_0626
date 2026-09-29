from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QStackedWidget, QLabel

from app.handlers import main_handler
from app.instances.particles import oil_particles_dict, fuel_particles_dict, oil_particle_dict_data, \
    fuel_particle_dict_data, OilTable, FuelTable
from app.instances.stands import FuelStand, OilStand
from app.pages.graph_dialog import GraphDialog
from app.ui.containers.rigth_container import RightContainer
from app.ui.elements.particle_table import PartTable
from app.ui.schemes.scheme import Scheme
from app.ui.containers.left_container import LeftContainer
from core.models.tag import IntTag
from core.settings import Settings
from app.ui.containers.header import Header
from core.widgets.ui_widgets.value_input import ValueInput


class MainPage(QWidget):
    set_stand = Signal(int)

    def __init__(self, tag: IntTag, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('mainPage')

        self.stand: int | None = OilStand.num
        self.tag = tag

        self.tag.update_value.connect(self.update_active_stand)
        self.tag.timeout_error_signal.connect(self.handle_error)

        self.graph_dialog = None

        self.header_box = QWidget()
        self.header_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.header_layout = QVBoxLayout()
        self.header = Header()
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.header.menu_buttons.graph_button.clicked.connect(self.open_graph_modal)
        self.header_layout.addWidget(self.header)
        self.header_box.setLayout(self.header_layout)
        self.header_box.adjustSize()

        self.middle = QWidget()
        self.middle.setStyleSheet(f'''
            border: 1px solid red;
        ''')
        self.middle_layout = QHBoxLayout()
        self.middle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.middle_layout.setContentsMargins(0,0,0,0)

        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle.setLayout(self.middle_layout)

        self.scene = QWidget(self)
        self.scene.setFixedSize(Settings.SCENE_SIZE[0] + 40, Settings.SCENE_SIZE[1] + 40)
        self.scene_layout = QHBoxLayout(self.scene)
        self.scene_layout.setContentsMargins(0, 0, 0, 0)
        self.scheme = Scheme()
        self.scene_layout.addWidget(self.scheme)

        self.middle_layout.addStretch()
        # self.middle_layout.addWidget(self.table_left)
        self.middle_layout.addWidget(self.scene)
        # self.middle_layout.addWidget(self.table_right)
        self.middle_layout.addStretch()

        self.bottom = QWidget()
        self.bottom.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.bottom.setStyleSheet('border: 1px solid green;')

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0,0,0,0)

        self.table_box = QWidget()
        self.table_box.setFixedWidth(Settings.SCENE_SIZE[0] * 1.1)
        self.table_box_layout = QVBoxLayout()
        self.table_stack = QStackedWidget()

        self.oil_table = PartTable(
            num_tag=OilTable.oil_test_num,
            tags=oil_particle_dict_data,
            index_before_tag=OilTable.oil_before_index,
            index_after_tag=OilTable.oil_after_index
        )
        self.table_stack.addWidget(self.oil_table)

        self.fuel_table = PartTable(
            FuelTable.fuel_test_num,
            fuel_particle_dict_data,
            index_before_tag=FuelTable.fuel_before_index,
            index_after_tag=FuelTable.fuel_after_index
        )
        self.table_stack.addWidget(self.fuel_table)

        self.table_box_layout.addWidget(self.table_stack)
        self.table_box.setLayout(self.table_box_layout)

        self.left_container = LeftContainer()
        self.left_container.choose_button_pressed.connect(self.set_active_stand)

        self.right_container = RightContainer()

        self.bottom_layout.addWidget(self.left_container)
        self.bottom_layout.addWidget(self.table_box)
        self.bottom_layout.addWidget(self.right_container)

        self.bottom.setLayout(self.bottom_layout)

        self.layout.addWidget(self.header_box)
        self.layout.addWidget(self.middle)
        self.layout.addWidget(self.bottom)

        if self.tag.value is None:
            self.update_active_stand(1)

        self.adjustSize()
        self.header.adjustSize()


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

    @Slot(int)
    def update_active_stand(self, val: int):
        self.stand = val

        if val == OilStand.num:
            self.left_container.value_input.connect_tag(OilTable.oil_test_num)
            self.left_container.test_before_button.connect_tag(OilTable.oil_select_before)
            self.left_container.test_after_button.connect_tag(OilTable.oil_select_after)
            self.left_container.title_label.setText(OilStand.name)
            self.table_stack.setCurrentIndex(0)
        elif val == FuelStand.num:
            self.left_container.value_input.connect_tag(FuelTable.fuel_test_num)
            self.left_container.test_before_button.connect_tag(FuelTable.fuel_select_before)
            self.left_container.test_after_button.connect_tag(FuelTable.fuel_select_after)
            self.left_container.title_label.setText(FuelStand.name)
            self.table_stack.setCurrentIndex(1)

        self.left_container.choose_button.setDisabled(False)

    @Slot()
    def set_active_stand(self):
        if self.stand == OilStand.num:
            self.tag.set_value(FuelStand.num)
        elif self.stand == FuelStand.num:
            self.tag.set_value(OilStand.num)

    @Slot(str)
    def handle_error(self, text: str):
        self.left_container.choose_button.setDisabled(False)
        self.left_container.choose_button.setCursor(Qt.CursorShape.PointingHandCursor)
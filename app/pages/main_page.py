from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QStackedWidget, QLabel

from app.handlers import main_handler
from app.instances.particles import oil_particles_dict, fuel_particles_dict, oil_particle_dict_data, \
    fuel_particle_dict_data, OilTable, FuelTable, oil_effectiveness_dict_data, fuel_effectiveness_dict_data
from app.instances.stands import FuelStand, OilStand
from app.pages.graph_dialog import GraphDialog
from app.ui.containers.rigth_bottom_container import RightContainer
from app.ui.elements.effectiveness_table import EffTable
from app.ui.elements.particle_table import PartTable
from app.ui.schemes.scheme import Scheme
from app.ui.containers.left_bottom_container import LeftContainer
from core.models.tag import IntTag
from core.settings import Settings
from app.ui.containers.header import Header
from core.widgets.ui_widgets.button import MenuButton
from core.widgets.ui_widgets.value_input import ValueInput


class MainPage(QWidget):
    set_stand = Signal(int)
    choose_button_pressed = Signal()

    def __init__(self, tag: IntTag, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        # self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('mainPage')

        self.stand: int | None = 0
        self.tag = tag

        self.oil_select_before = OilTable.oil_select_before
        self.oil_select_after = OilTable.oil_select_after
        self.fuel_select_before = FuelTable.fuel_select_before
        self.fuel_select_after = FuelTable.fuel_select_after
        self.oil_test_num = OilTable.oil_test_num
        self.fuel_test_num = FuelTable.fuel_test_num
        self.oil_before_index = OilTable.oil_before_index
        self.oil_after_index = OilTable.oil_after_index
        self.fuel_before_index = FuelTable.fuel_before_index
        self.fuel_after_index = FuelTable.fuel_after_index

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
        # self.middle.setStyleSheet(f'''
        #     border: 1px solid red;
        # ''')
        self.middle_layout = QHBoxLayout()
        self.middle.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.middle.setLayout(self.middle_layout)

        self.scene = QWidget(self)
        # self.scene.setStyleSheet('border: 1px solid green;')
        self.scene_layout = QHBoxLayout(self.scene)
        self.scene_layout.setContentsMargins(0,0,0,0)
        self.scheme = Scheme()
        self.scene_layout.addWidget(self.scheme)
        self.scheme.choose_button.pressed.connect(self.set_active_stand)

        self.side_table_box = QWidget()
        # self.side_table_box.setStyleSheet('border: 1px solid purple;')
        self.side_table_box.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.side_table_box_layout = QVBoxLayout()
        self.side_table_box.setLayout(self.side_table_box_layout)

        self.side_table_stack = QStackedWidget()

        self.oil_eff_table = EffTable(
            tags=oil_effectiveness_dict_data
        )
        self.side_table_stack.addWidget(self.oil_eff_table)

        self.fuel_eff_table = EffTable(
            tags=fuel_effectiveness_dict_data
        )
        self.side_table_stack.addWidget(self.fuel_eff_table)

        self.side_table_stack.addWidget(QWidget())

        self.side_table_box_layout.addWidget(self.side_table_stack)

        # self.middle_layout.addWidget(self.title_box, stretch=1)
        self.middle_layout.addStretch(stretch=1)
        self.middle_layout.addWidget(self.scene, stretch=4)
        self.middle_layout.addWidget(self.side_table_box, stretch=1)

        self.bottom = QWidget()
        self.bottom.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0,0,0,0)

        self.table_box = QWidget()
        self.table_box.setFixedWidth(Settings.SCENE_WIDTH)
        self.table_box_layout = QVBoxLayout()
        self.table_stack = QStackedWidget()

        self.oil_table = PartTable(
            num_tag=OilTable.oil_test_num,
            tags=oil_particle_dict_data,
            index_before_tag=self.oil_before_index,
            index_after_tag=self.oil_after_index
        )
        self.table_stack.addWidget(self.oil_table)

        self.fuel_table = PartTable(
            num_tag=self.fuel_test_num,
            tags=fuel_particle_dict_data,
            index_before_tag=self.fuel_before_index,
            index_after_tag=self.fuel_after_index
        )
        self.table_stack.addWidget(self.fuel_table)

        self.table_stack.addWidget(QWidget())

        self.table_box_layout.addWidget(self.table_stack)
        self.table_box.setLayout(self.table_box_layout)

        self.stacked_left_container = QStackedWidget()

        self.oil_left_container = LeftContainer(
            before_index=self.oil_before_index,
            after_index=self.oil_after_index,
            test_num=self.oil_test_num,
            select_before=self.oil_select_before,
            select_after=self.oil_select_after
        )
        self.fuel_left_container = LeftContainer(
            before_index=self.fuel_before_index,
            after_index=self.fuel_after_index,
            test_num=self.fuel_test_num,
            select_before=self.fuel_select_before,
            select_after=self.fuel_select_after
        )

        self.stacked_left_container.addWidget(self.oil_left_container)
        self.stacked_left_container.addWidget(self.fuel_left_container)
        self.stacked_left_container.addWidget(QWidget())

        self.right_container = RightContainer()

        self.bottom_layout.addWidget(self.stacked_left_container)
        self.bottom_layout.addWidget(self.table_box)
        self.bottom_layout.addWidget(self.right_container)

        self.bottom.setLayout(self.bottom_layout)

        self.layout.addWidget(self.header_box)
        self.layout.addWidget(self.middle)
        self.layout.addWidget(self.bottom)

        if self.tag.value == 0:
            self.update_active_stand(0)

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

    @Slot()
    def choose_stand(self):
        self.scheme.choose_button.setDisabled(True)
        self.choose_button_pressed.emit()

    @Slot(int)
    def update_active_stand(self, val: int):
        self.stand = val

        if val == OilStand.num:

            self.stacked_left_container.setCurrentIndex(0)
            self.right_container.stacked_button_box.setCurrentIndex(0)

            # self.title_label.setText(OilStand.name)

            self.table_stack.setCurrentIndex(0)
            self.side_table_stack.setCurrentIndex(0)
            self.scheme.scheme_borders.oil_border.set_highlighted(True)
            self.scheme.scheme_borders.fuel_border.set_highlighted(False)
        elif val == FuelStand.num:

            self.stacked_left_container.setCurrentIndex(1)
            self.right_container.stacked_button_box.setCurrentIndex(1)

            # self.title_label.setText(FuelStand.name)
            self.table_stack.setCurrentIndex(1)
            self.side_table_stack.setCurrentIndex(1)
            self.scheme.scheme_borders.oil_border.set_highlighted(False)
            self.scheme.scheme_borders.fuel_border.set_highlighted(True)
        else:
            self.table_stack.setCurrentIndex(2)
            self.side_table_stack.setCurrentIndex(2)
            self.stacked_left_container.setCurrentIndex(2)
            self.right_container.stacked_button_box.setCurrentIndex(2)
        self.scheme.choose_button.setDisabled(False)

    @Slot()
    def set_active_stand(self):
        self.scheme.choose_button.setDisabled(True)
        if self.stand == OilStand.num:
            self.tag.set_value(FuelStand.num)
        elif self.stand == FuelStand.num:
            self.tag.set_value(OilStand.num)
        else:
            self.tag.set_value(OilStand.num)

    @Slot(str)
    def handle_error(self, text: str):
        self.scheme.choose_button.setDisabled(False)
        self.scheme.choose_button.setCursor(Qt.CursorShape.PointingHandCursor)
from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from app.handlers import main_handler
from app.instances.particles import oil_particles_dict, fuel_particles_dict, oil_particle_dict_data, \
    fuel_particle_dict_data, OilTable, FuelTable
from app.instances.stands import FuelStand, OilStand
from app.pages.graph_dialog import GraphDialog
from app.ui.containers.rigth_container import RightContainer
from app.ui.elements.particle_table import ParticleTable
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
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('mainPage')

        self.stand: int | None = OilStand.num
        self.tag = tag
        self.tag.update_value.connect(self.update_active_stand)
        self.tag.timeout_error_signal.connect(self.handle_error)

        self.graph_dialog = None

        self.header = Header()
        self.header.menu_buttons.graph_button.clicked.connect(self.open_graph_modal)

        self.middle = QWidget()
        self.middle_layout = QHBoxLayout()
        self.middle_layout.setContentsMargins(0,0,0,0)
        # self.middle.setStyleSheet(f'''
        #     border: 2px solid blue;
        # ''')

        self.scene = QWidget(self)
        # self.scene.setStyleSheet(f'''
        #     border: 2px solid red;
        # ''')
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

        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.middle_layout.setContentsMargins(0,0,0,0)
        self.middle.setLayout(self.middle_layout)

        self.bottom = QWidget()

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0,0,0,0)
        self.oil_table = ParticleTable(OilTable.oil_test_num, oil_particle_dict_data)
        self.fuel_table = ParticleTable(FuelTable.fuel_test_num, fuel_particle_dict_data)

        self.left_container = LeftContainer()
        self.left_container.setFixedWidth(200)
        self.left_container.choose_button_pressed.connect(self.set_active_stand)

        self.right_container = RightContainer()
        self.right_container.setFixedWidth(200)
        # self.right_container.setStyleSheet('border: 1px solid blue')

        self.bottom_layout.addWidget(self.left_container, stretch=1)
        self.bottom_layout.addWidget(self.oil_table, stretch=4)
        self.bottom_layout.addWidget(self.fuel_table, stretch=4)
        self.bottom_layout.addWidget(self.right_container, stretch=1)

        self.bottom.setLayout(self.bottom_layout)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.middle)
        self.layout.addWidget(self.bottom)


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
        if self.stand == OilStand.num:
            self.fuel_table.hide()
            self.oil_table.show()
            self.left_container.title_label.setText(OilStand.name)
            self.left_container.fuel_value_input.hide()
            self.left_container.oil_value_input.show()
            self.right_container.fuel_effectiveness_box.hide()
            self.right_container.oil_effectiveness_box.show()
        elif self.stand == FuelStand.num:
            self.oil_table.hide()
            self.fuel_table.show()
            self.left_container.title_label.setText(FuelStand.name)
            self.left_container.oil_value_input.hide()
            self.left_container.fuel_value_input.show()
            self.right_container.oil_effectiveness_box.hide()
            self.right_container.fuel_effectiveness_box.show()
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
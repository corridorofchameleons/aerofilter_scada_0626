from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from app.instances.particles import oil_particles_dict, fuel_particles_dict, oil_particle_dict_data, \
    fuel_particle_dict_data
from app.instances.stands import FuelStand, OilStand
from app.pages.graph_dialog import GraphDialog
from app.ui.elements.particle_table import ParticleTable
from app.ui.schemes.scheme import Scheme
from app.ui.containers.side_container import SideContainer
from core.settings import Settings
from app.ui.containers.header import Header


class MainPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('mainPage')

        self.graph_dialog = None

        self.header = Header()
        self.header.menu_buttons.graph_button.clicked.connect(self.open_graph_modal)

        self.middle = QWidget()
        self.middle_layout = QHBoxLayout()
        self.middle_layout.setContentsMargins(0,0,0,0)
        self.middle.setStyleSheet(f'''
            border: 2px solid blue;
        ''')

        self.scene = QWidget(self)
        self.scene.setStyleSheet(f'''
            border: 2px solid red;
        ''')
        self.scene.setFixedSize(Settings.SCENE_SIZE[0] + 40, Settings.SCENE_SIZE[1] + 40)
        self.scene_layout = QHBoxLayout(self.scene)
        self.scene_layout.setContentsMargins(0, 0, 0, 0)
        self.scheme = Scheme()
        self.scene_layout.addWidget(self.scheme)

        self.table_left = SideContainer(OilStand, oil_particle_dict_data)
        self.table_right = SideContainer(FuelStand, fuel_particle_dict_data)

        self.middle_layout.addStretch()
        # self.middle_layout.addWidget(self.table_left)
        self.middle_layout.addWidget(self.scene)
        # self.middle_layout.addWidget(self.table_right)
        self.middle_layout.addStretch()

        self.middle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.middle.setLayout(self.middle_layout)

        self.bottom = QWidget()

        self.bottom_layout = QHBoxLayout()
        self.oil_table = ParticleTable(oil_particle_dict_data)
        self.fuel_table = ParticleTable(fuel_particle_dict_data)
        self.fuel_table.hide()

        self.bottom_layout.addStretch()
        # self.middle_layout.addWidget(self.table_left)
        self.bottom_layout.addWidget(self.oil_table)
        self.bottom_layout.addWidget(self.fuel_table)
        # self.middle_layout.addWidget(self.table_right)
        self.bottom_layout.addStretch()

        self.bottom.setLayout(self.bottom_layout)
        self.bottom.setStyleSheet(f'''
            border: 2px solid green;
        ''')

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

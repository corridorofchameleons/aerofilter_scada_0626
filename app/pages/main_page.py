from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QStackedWidget, QSplitter

from app.instances.particles import oil_particles_dict, fuel_particles_dict, oil_particle_dict_data, \
    fuel_particle_dict_data, OilTable, FuelTable, oil_effectiveness_dict, oil_table_data_dict, fuel_effectiveness_dict, fuel_table_data_dict
from app.instances.stands import FuelStand, OilStand
from app.pages.graph_dialog import GraphDialog
from app.ui.layouts.sections.bottom import BottomSection
from app.ui.layouts.sections.middle import MiddleSection
from core.models.tag import Tag
from app.ui.layouts.sections.header import Header


class MainPage(QWidget):
    set_stand = Signal(int)
    choose_button_pressed = Signal()

    def __init__(self, tag: Tag, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setObjectName('mainPage')

        self.stand: int | None = 0
        self.tag = tag

        self.oil_select_before = OilTable.oil_select_before
        self.oil_select_after = OilTable.oil_select_after
        self.oil_test_num = OilTable.oil_test_num
        self.oil_before_index = OilTable.oil_before_index
        self.oil_after_index = OilTable.oil_after_index
        self.oil_effectiveness = OilTable.oil_effectiveness
        self.fuel_test_num = FuelTable.fuel_test_num
        self.fuel_select_before = FuelTable.fuel_select_before
        self.fuel_select_after = FuelTable.fuel_select_after
        self.fuel_before_index = FuelTable.fuel_before_index
        self.fuel_after_index = FuelTable.fuel_after_index
        self.fuel_effectiveness = FuelTable.fuel_effectiveness

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

        self.middle = MiddleSection()
        self.choose_button = self.middle.scheme_box.scheme.choose_button
        self.choose_button.pressed.connect(self.set_active_stand)

        self.bottom = QStackedWidget()

        self.oil_bottom = BottomSection(
            test_num=self.oil_test_num,
            select_before=self.oil_select_before,
            select_after=self.oil_select_after,
            effectiveness=self.oil_effectiveness,
            particle_data=oil_particle_dict_data,
            clear_data=oil_table_data_dict | oil_effectiveness_dict | oil_particles_dict,
            before_index_tag=self.oil_before_index,
            after_index_tag=self.oil_after_index
        )

        self.fuel_bottom = BottomSection(
            test_num=self.fuel_test_num,
            select_before=self.fuel_select_before,
            select_after=self.fuel_select_after,
            effectiveness=self.fuel_effectiveness,
            particle_data=fuel_particle_dict_data,
            clear_data=fuel_particles_dict | fuel_effectiveness_dict | fuel_table_data_dict,
            before_index_tag=self.fuel_before_index,
            after_index_tag=self.fuel_after_index
        )

        self.bottom.addWidget(self.oil_bottom)
        self.bottom.addWidget(self.fuel_bottom)
        self.bottom.addWidget(QWidget())

        self.splitter = QSplitter(Qt.Orientation.Vertical)
        self.splitter.setHandleWidth(4)
        self.splitter.setStyleSheet(""" 
        QSplitter::handle { 
            background-color: grey; 
        } 
            QSplitter::handle:hover { 
            background-color: darkgray; 
        } 
         """)
        self.splitter.setOpaqueResize(True)
        # self.splitter.setSizes([self.middle.scheme_box.height(), 200])
        self.splitter.addWidget(self.middle)
        self.splitter.addWidget(self.bottom)
        self.splitter.setStretchFactor(0, 4)
        self.splitter.setStretchFactor(1, 3)

        self.layout.addWidget(self.header_box)
        self.layout.addWidget(self.splitter)

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
        self.choose_button.setDisabled(True)
        self.choose_button_pressed.emit()

    @Slot(int)
    def update_active_stand(self, val: int):
        self.stand = val

        if val == OilStand.num:
            self.bottom.setCurrentIndex(0)
            self.middle.right_box.side_table_stack.setCurrentIndex(0)
            self.middle.scheme_box.scheme.scheme_borders.oil_border.set_highlighted(True)
            self.middle.scheme_box.scheme.scheme_borders.fuel_border.set_highlighted(False)
        elif val == FuelStand.num:
            self.bottom.setCurrentIndex(1)
            self.middle.right_box.side_table_stack.setCurrentIndex(1)
            self.middle.scheme_box.scheme.scheme_borders.oil_border.set_highlighted(False)
            self.middle.scheme_box.scheme.scheme_borders.fuel_border.set_highlighted(True)
        else:
            self.bottom.setCurrentIndex(2)
            self.middle.right_box.side_table_stack.setCurrentIndex(2)
        self.choose_button.setDisabled(False)

    @Slot()
    def set_active_stand(self):
        self.choose_button.setDisabled(True)
        if self.stand == OilStand.num:
            self.tag.set_value(FuelStand.num)
        elif self.stand == FuelStand.num:
            self.tag.set_value(OilStand.num)
        else:
            self.tag.set_value(OilStand.num)

    @Slot(str)
    def handle_error(self, text: str):
        self.choose_button.setDisabled(False)
        self.choose_button.setCursor(Qt.CursorShape.PointingHandCursor)
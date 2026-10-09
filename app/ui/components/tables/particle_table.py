from typing import OrderedDict

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QTableView, QAbstractScrollArea, \
    QAbstractItemView, QVBoxLayout

from app.instances.particles import PARTICLES, TEST_NUM, OilTable
from core.widgets.ui_widgets.table_cell import Cell, EnumCell
from core.models.tag import Tag
from core.settings import Settings

class PartTable(QWidget):
    highlight_cell_signal = Signal(int)
    disconnect_signal = Signal()
    revalidate_before = Signal()
    revalidate_after = Signal()

    def __init__(
            self,
            num_tag: Tag,
            tags: dict,
            clear_tag: Tag,
    ):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet('color: black;')

        self.tags = tags
        self.num_tag = num_tag
        if self.num_tag:
            self.num_tag.update_ui.connect(self.compose_table)

        self.before_cancelled = False
        self.before_buffer = {}
        self.after_cancelled = False
        self.after_buffer = {}

        self.tests_before = OrderedDict()
        self.tests_after = OrderedDict()
        # self.clear_tests()

        self.clear_tag = clear_tag
        self.clear_tag.update_ui.connect(self.clear_tests)

        # self.index_before_tag = index_before_tag
        # self.index_after_tag = index_after_tag

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.table = QTableView()
        self.model = QStandardItemModel()

    @Slot()
    def handle_revalidate_before(self):
        self.revalidate_before.emit()

    @Slot()
    def handle_revalidate_after(self):
        self.revalidate_after.emit()

    @Slot()
    def clear_tests(self):
        for test in range(1, TEST_NUM + 1):
            self.tests_before[test] = False
            self.tests_after[test] = False

    def compose_table(self):
        self.disconnect_signal.emit()

        cols = self.num_tag.value
        if cols is None:
            cols = 0
        self.layout.removeWidget(self.table)
        self.model.clear()
        self.table.deleteLater()

        self.table = QTableView()
        self.model = QStandardItemModel(len(PARTICLES) + 1, cols * 2 + 1)
        self.table.setModel(self.model)

        for col in range(cols + 1):
            if col <= 0:
                self.table.horizontalHeader().resizeSection(col, 70)
                self.table.verticalHeader().resizeSection(0, 40)
                label = QLabel('Диапазон')
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet(f'''
                    border: none;
                    font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                    font-weight: bold;
                    background-color: silver;
                    border-right: 1px solid dimgray;
                    border-bottom: 1px solid dimgray;
                ''')

                index = self.model.index(0, col)
                self.table.setIndexWidget(index, label)

                for i, val in enumerate(PARTICLES):
                    label_text = f'>{val} мкм' if isinstance(val, int) else 'Класс'
                    label = QLabel(label_text)
                    label.setContentsMargins(5, 0, 0, 0)
                    label.setStyleSheet(f'''
                        border: none;
                        font-size: {Settings.VALUE_BOX_VALUE_FONT_SIZE * 0.8}px;
                        background-color: silver;
                        border-right: 1px solid dimgray;
                        {'border-bottom: 1px solid dimgray;' if i < len(PARTICLES) - 1 else 'border-bottom: none;'}
                    ''')
                    index = self.model.index(i + 1, col)
                    self.table.setIndexWidget(index, label)

            else:
                col_tags = self.tags.get(col)

                index_tag_before = col_tags[1].get('index')
                index_tag_after = col_tags[2].get('index')

                before_value_label = EnumCell(index_tag_before,
                                              enum_data={
                                                  0: {'title': f'ДО {col}', 'color': 'silver'},
                                                  1: {'title': f'ОТМЕНИТЬ\nДО {col}', 'color': 'lightblue'},
                                                  2: {'title': f'ВЕРНУТЬ\nДО {col}', 'color': 'lightgreen'}
                                              }, victims=col_tags[1]['items'], col=col, tests=self.tests_before, disconnect_signal=self.disconnect_signal)
                # before_value_label.cleared_col.connect(self.check_before_index)
                before_value_label.revalidate.connect(self.handle_revalidate_before)
                before_value_label.update_ui()

                after_value_label = EnumCell(index_tag_after,
                                              enum_data={
                                                  0: {'title': f'ПОСЛЕ {col}', 'color': 'silver'},
                                                  1: {'title': f'ОТМЕНИТЬ\nПОСЛЕ {col}', 'color': 'lightblue'},
                                                  2: {'title': f'ВЕРНУТЬ\nПОСЛЕ {col}', 'color': 'lightgreen'}
                                              }, victims=col_tags[2]['items'], col=col, tests=self.tests_after, disconnect_signal=self.disconnect_signal)
                # after_value_label.cleared_col.connect(self.check_after_index)
                after_value_label.revalidate.connect(self.handle_revalidate_after)
                after_value_label.update_ui()

                index_before = self.model.index(0, col * 2 - 1)
                self.table.setIndexWidget(index_before, before_value_label)
                index_after = self.model.index(0, col * 2)
                self.table.setIndexWidget(index_after, after_value_label)

                for i, val in enumerate(PARTICLES):

                    before_value_label = Cell(col_tags[1]['items'].get(val))
                    after_value_label = Cell(col_tags[2]['items'].get(val))

                    before_value_label.update_ui()
                    after_value_label.update_ui()

                    index_before = self.model.index(i + 1, col * 2 - 1)
                    self.table.setIndexWidget(index_before, before_value_label)
                    index_after = self.model.index(i + 1, col * 2)
                    self.table.setIndexWidget(index_after, after_value_label)

        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.table.setStyleSheet('''
            background-color: lightgray; 
            border: 2px solid dimgray;
        ''')
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(16)
        self.table.verticalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setDefaultSectionSize(55)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setShowGrid(False)

        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.table.updateGeometry()
        self.layout.addWidget(self.table)

    # @Slot(int)
    # def check_before_index(self, val: int):
    #     if val < self.index_before_tag.value:
    #         self.index_before_tag.value = val
    #
    # @Slot()
    # def check_after_index(self, val: int):
    #     if val < self.index_after_tag.value:
    #         self.index_after_tag.value = val

    # @staticmethod
    # def __label_button(fn):
    #     label = Cell()
    #     label.unsetCursor()
    #     label.set_style('#EE8888')
    #     label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    #     label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
    #     label.setCursor(Qt.CursorShape.PointingHandCursor)
    #     label.mousePressEvent = fn
    #     return label

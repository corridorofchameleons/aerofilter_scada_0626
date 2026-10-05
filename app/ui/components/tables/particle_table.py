from typing import OrderedDict

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QTableView, QAbstractScrollArea, \
    QAbstractItemView, QVBoxLayout

from app.instances.particles import PARTICLES
from core.widgets.ui_widgets.particle_table_cell import Cell
from core.models.tag import IntTag
from core.settings import Settings

class PartTable(QWidget):
    highlight_cell_signal = Signal(int)

    def __init__(
            self,
            num_tag: IntTag,
            tags: dict,
            index_before_tag: IntTag,
            index_after_tag: IntTag
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

        self.cancel_before_button = None
        self.cancel_after_button = None

        self.index_before_tag = index_before_tag
        self.index_after_tag = index_after_tag
        self.index_before_tag.update_ui.connect(lambda: self.handle_indexes(1))
        self.index_after_tag.update_ui.connect(lambda: self.handle_indexes(2))

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.table = QTableView()
        self.compose_table()
        self.model = QStandardItemModel()

    def compose_table(self):
        # self.restore_before(event=None)
        # self.restore_after(event=None)

        cols = self.num_tag.value
        if cols is None:
            cols = 0
        self.layout.removeWidget(self.table)
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
                self.compose_header_row()

                col_tags = self.tags.get(col)
                for i, val in enumerate(PARTICLES):
                    tag_couple = col_tags.get(val)
                    tag_couple_list = list(tag_couple.values())

                    before_value_label = Cell(tag_couple_list[0], index=col, highlight_tag=self.index_before_tag)
                    after_value_label = Cell(tag_couple_list[1], index=col, highlight_tag=self.index_after_tag)

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

    @staticmethod
    def __label_button(fn):
        label = Cell()
        label.unsetCursor()
        label.set_style('#EE8888')
        label.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        label.setCursor(Qt.CursorShape.PointingHandCursor)
        label.mousePressEvent = fn
        return label

    @Slot(int)
    def handle_indexes(self, pos: int):
        if self.before_cancelled and pos == 2:
            self.restore_before(event=None)
        if self.after_cancelled and pos == 1:
            self.restore_after(event=None)
        self.compose_header_row()


    def compose_header_row(self):
        cols = self.num_tag.value
        for col in range(1, cols + 1):
            if (self.index_before_tag.value == col - 1) and self.before_cancelled:
                self.restore_before(event=None)
            elif self.index_before_tag.value == col:
                before_label = self.__label_button(self.clear_before)
                before_label.setText(f'Отменить\nДО {self.index_before_tag.value}')
                self.cancel_before_button = before_label
                self.cancel_before_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                before_label = Cell(text=f'ДО {col}')
                before_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                before_label.set_style('silver')

            if (self.index_after_tag.value == col - 1) and self.after_cancelled:
                self.restore_after(event=None)
            if self.index_after_tag.value == col:
                after_label = self.__label_button(self.clear_after)
                after_label.setText(f'Отменить\nПОСЛЕ {self.index_after_tag.value}')
                self.cancel_after_button = after_label
                self.cancel_after_button.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                after_label = Cell(text=f'ПОСЛЕ {col}')
                after_label.set_style('silver')
                after_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            index_before = self.model.index(0, col * 2 - 1)
            self.table.setIndexWidget(index_before, before_label)
            index_after = self.model.index(0, col * 2)
            self.table.setIndexWidget(index_after, after_label)

    def clear_before(self, event):
        index = self.index_before_tag.value
        tag_data = self.tags.get(index)
        self.before_buffer = {}
        for pair in tag_data.values():
            name, tag = list(pair.items())[0]
            self.before_buffer[name] = tag.value
            tag.value = None
            tag.update_ui.emit()
        self.index_before_tag.value -= 1
        self.before_cancelled = True
        if isinstance(self.cancel_before_button, Cell):
            self.cancel_before_button.setText(f'Вернуть\nДО {self.index_before_tag.value + 1}')
            self.cancel_before_button.set_style('#88EE88')
            self.cancel_before_button.mousePressEvent = self.restore_before

    def restore_before(self, event):
        self.index_before_tag.value += 1
        tag_data = self.tags.get(self.index_before_tag.value)
        for pair in tag_data.values():
            name, tag = list(pair.items())[0]
            tag.value = self.before_buffer.get(name)
            tag.update_ui.emit()
        self.before_buffer = {}
        self.before_cancelled = False
        if isinstance(self.cancel_before_button, Cell):
            self.cancel_before_button.setText(f'Отменить\nДО {self.index_before_tag.value}')
            self.cancel_before_button.set_style('#EE8888')
            self.cancel_before_button.mousePressEvent = self.clear_before

    def clear_after(self, event):
        tag_data = self.tags.get(self.index_after_tag.value)
        self.after_buffer = OrderedDict()
        for pair in tag_data.values():
            name, tag = list(pair.items())[1]
            self.after_buffer[name] = tag.value
            tag.value = None
            tag.update_ui.emit()
        self.index_after_tag.value -= 1
        self.after_cancelled = True
        if isinstance(self.cancel_after_button, Cell):
            self.cancel_after_button.setText(f'Вернуть\nПОСЛЕ {self.index_after_tag.value + 1}')
            self.cancel_after_button.set_style('#88EE88')
            self.cancel_after_button.mousePressEvent = self.restore_after

    def restore_after(self, event):
        self.index_after_tag.value += 1
        tag_data = self.tags.get(self.index_after_tag.value)
        for pair in tag_data.values():
            name, tag = list(pair.items())[1]
            tag.value = self.after_buffer.get(name)
            tag.update_ui.emit()
        self.after_buffer = None
        self.after_cancelled = False
        if isinstance(self.cancel_after_button, Cell):
            self.cancel_after_button.setText(f'Отменить\nПОСЛЕ {self.index_after_tag.value}')
            self.cancel_after_button.set_style('#EE8888')
            self.cancel_after_button.mousePressEvent = self.clear_after


from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from loguru import logger

from app.data.topics import SET_LIST_TOPIC
from core.models.tag import Tag
from core.signals.mqtt import bus
from core.widgets.ui_widgets.button import Button
from core.widgets.ui_widgets.value_box import ValueBox
from mock.mock import SET_TOPIC


class RightBottomContainer(QWidget):
    def __init__(
            self,
            effectiveness_tag: Tag,
            clear_data: dict,
            prefix: str,
            parent=None,
    ):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 20, 20, 0)
        self.setMinimumHeight(self.height())

        self.effectiveness_tag = effectiveness_tag
        self.clear_data = clear_data

        self.prefix = prefix
        self.bus = bus

        self.button_box = QWidget()
        self.button_box_layout = QVBoxLayout()
        self.button_box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.effectiveness_box = ValueBox(
            self.effectiveness_tag,
            'Эффективность\nфильтра',
            width=110,
            height=60,
            error_widget=False,
            scada=False
        )
        self.calculate_button = Button('Рассчитать', width=110)
        self.new_test_button = Button('Новое\nиспытание', width=110, custom=True)
        self.new_test_button.clicked.connect(
            lambda: self.clear_table(self.clear_data))
        self.report_button = Button('Сформировать\nотчет', width=110, custom=True)
        self.report_button.clicked.connect(
            self.request_report
        )

        # self.button_box_layout.addWidget(self.effectiveness_box)
        # self.button_box_layout.addWidget(self.calculate_button)
        self.button_box_layout.addWidget(self.new_test_button)
        self.button_box_layout.addWidget(self.report_button)
        self.button_box.setLayout(self.button_box_layout)

        self.setLayout(self.layout)
        self.layout.addWidget(self.button_box)

    @Slot()
    def clear_table(self, tags_to_clear):

        reply = QMessageBox.question(self, 'Новое испытание', 'Вы уверены, что хотите очистить все измерения?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No:
            return
        else:
            logger.info(f'CLEARING {self.prefix} TABLE')
            tags = [tag for tag in tags_to_clear.values() if isinstance(tag, Tag)]

            data = [{'name': tag.name, 'value': tag.initial_value} for tag in tags]
            logger.info(f'Resetting values')
            bus.mqtt_publish_multiple_signal.emit(data, SET_LIST_TOPIC)

    @Slot()
    def request_report(self):
        msg = {
            'ns_name': 'stand',
            'name': f'{self.prefix}_report_request',
            'value': True
        }

        logger.info(f'REQUESTING {self.prefix} report')

        self.bus.mqtt_publish_signal.emit(msg, SET_TOPIC)

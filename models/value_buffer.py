from collections import deque
from dataclasses import dataclass

from PySide6.QtCore import QObject, Slot, Signal

from widgets.settings import Settings


@dataclass
class DataPoint:
    ts: int
    val: float


class ValueBuffer(QObject):
    update_graph_signal = Signal()

    def __init__(
            self,
            name: str,
            signal_fn
    ):
        super().__init__()

        self.buffer = deque(maxlen=Settings.BUFFER_LEN)

        self.name = name
        self.signal_fn = signal_fn
        self.signal_fn.connect(self.add_point)


    @Slot('q', float)
    def add_point(self, timestamp: int, value: float):
        self.buffer.append(DataPoint(timestamp, value))
        self.update_graph_signal.emit()

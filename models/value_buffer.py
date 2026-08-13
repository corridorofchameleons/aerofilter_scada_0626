from collections import deque
from bisect import bisect_left
from dataclasses import dataclass
import time

from PySide6.QtCore import QObject, Slot

from widgets.settings import Settings


@dataclass
class DataPoint:
    ts: int
    val: float


class ValueBuffer(QObject):
    def __init__(
            self,
            name: str,
            device: str,
            signal_fn
    ):
        super().__init__()

        self.buffer = deque(maxlen=Settings.BUFFER_LEN)

        self.name = name
        self.device = device
        self.signal_fn = signal_fn
        self.signal_fn.connect(self.add_point)


    @Slot('q', float)
    def add_point(self, timestamp: int, value: float):
        self.buffer.append(DataPoint(timestamp, value))
        print(self.buffer)


    # def sample_for_grid(self, target_times: list[float], threshold: float) -> list[float | None]:
    #     if not self.buffer:
    #         return [None] * len(target_times)
    #
    #     t_stamps = [p.ts for p in self.buffer]
    #     values = [p.val for p in self.buffer]
    #
    #     result = []
    #     idx_hint = 0  # Оптимизация: начинаем поиск от прошлого найденного индекса
    #
    #     for t_target in target_times:
    #         # Ищем позицию вставки
    #         idx = bisect_left(t_stamps, t_target, lo=idx_hint)
    #
    #         best_match = None
    #         min_diff = float('inf')
    #
    #         # Проверяем правый соседний элемент
    #         if idx < len(t_stamps):
    #             diff = abs(t_stamps[idx] - t_target)
    #             if diff <= threshold and diff < min_diff:
    #                 min_diff = diff
    #                 best_match = values[idx]
    #
    #         # Проверяем левый соседний элемент
    #         if idx > 0:
    #             diff = abs(t_stamps[idx - 1] - t_target)
    #             if diff <= threshold and diff < min_diff:
    #                 best_match = values[idx - 1]
    #
    #         result.append(best_match)
    #         idx_hint = max(0, idx - 1)  # Подсказываем следующий индекс ближе к текущему
    #
    #     return result
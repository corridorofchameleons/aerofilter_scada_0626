from PySide6.QtCore import Qt, QTimer, QTime, QDate
from PySide6.QtWidgets import QLabel, QSizePolicy


class ClockWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('clockWidget')

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)

        self.run()

    def run(self):
        self.update_time()
        self.timer.start(1000)

    def update_time(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        time_text = current_time.toString('hh:mm:ss')
        date_text = current_date.toString('d.MM.yyyy')
        self.setText(f'{time_text} {date_text}')

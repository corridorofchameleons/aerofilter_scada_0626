from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QTextEdit

from mqtt.mqtt_client import MQTTClient
from pages.main_page import MainPage
WINDOW_SIZE: tuple[int, int] = 1980, 1080

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(*WINDOW_SIZE)

        main_page = MainPage(self)

        self.setCentralWidget(main_page)

        self.mqtt_thread = QThread()
        self.mqtt_worker = MQTTClient()

        self.mqtt_worker.moveToThread(self.mqtt_thread)
        self.mqtt_thread.started.connect(self.mqtt_worker.connect_and_run)
        self.mqtt_thread.finished.connect(self.mqtt_worker.deleteLater)

        self.mqtt_thread.start()

    def closeEvent(self, event):
        print("Finishing...")
        self.mqtt_worker.stop_client()
        self.mqtt_thread.quit()

        if not self.mqtt_thread.wait(2000):
            print('could not kill thread')

        print("Closing...")
        event.accept()


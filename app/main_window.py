import time

from PySide6.QtWidgets import QMainWindow

from app.pages.main_page import MainPage
from app.services.mqtt_handler import MQTTHandler

WINDOW_SIZE: tuple[int, int] = 1980, 1080

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(*WINDOW_SIZE)

        self.main_page = MainPage(self)

        self.setCentralWidget(self.main_page)

        self.mqtt_handler = MQTTHandler(self)

    def closeEvent(self, event):
        print("Finishing threads...")
        self.mqtt_handler.kill_mqtt()
        print("Closing app...")
        event.accept()


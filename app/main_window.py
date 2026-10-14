from PySide6.QtWidgets import QMainWindow

from loguru import logger
from app.instances.particles import MetaStand
from app.pages.main_page import MainPage
from app.handlers.main_handler import MainHandler


WINDOW_SIZE: tuple[int, int] = 1280, 720

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mqtt_handler = MainHandler(self)

        self.main_page = MainPage(MetaStand.stand_select, self)
        self.setCentralWidget(self.main_page)

    def closeEvent(self, event):
        logger.info("CLOSING THREADS...")
        self.mqtt_handler.kill_mqtt()
        logger.info("CLOSING APP...")
        event.accept()


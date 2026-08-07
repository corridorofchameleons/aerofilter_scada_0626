from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QTextEdit

from mqtt.mqtt_client import MQTTReceiver, MQTTSender
from pages.main_page import MainPage
WINDOW_SIZE: tuple[int, int] = 1980, 1080

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(*WINDOW_SIZE)

        main_page = MainPage(self)

        self.setCentralWidget(main_page)

        self.mqtt_receive_thread = QThread()
        self.mqtt_send_thread = QThread()

        self.mqtt_receiver = MQTTReceiver()
        self.mqtt_sender = MQTTSender()

        self.mqtt_receiver.moveToThread(self.mqtt_receive_thread)
        self.mqtt_sender.moveToThread(self.mqtt_send_thread)

        self.mqtt_receive_thread.started.connect(self.mqtt_receiver.connect_and_run)
        self.mqtt_send_thread.started.connect(self.mqtt_sender.connect_and_run)
        self.mqtt_receive_thread.finished.connect(self.mqtt_receiver.deleteLater)
        self.mqtt_send_thread.finished.connect(self.mqtt_sender.deleteLater)

        self.mqtt_receive_thread.start()
        self.mqtt_send_thread.start()

    def closeEvent(self, event):
        print("Finishing...")
        self.mqtt_receiver.stop_client()
        self.mqtt_sender.stop_client()
        self.mqtt_receive_thread.quit()
        self.mqtt_send_thread.quit()

        if not self.mqtt_receive_thread.wait(2000):
            print('could not kill thread')

        print("Closing...")
        event.accept()


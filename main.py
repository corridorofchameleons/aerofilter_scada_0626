from PySide6.QtWidgets import QApplication

from loguru import logger
from app.main_window import MainWindow
from app.utils.load_styles import load_styles
from logger import setup_logger

if __name__ == "__main__":
    import sys
    setup_logger()
    logger.info('STARTING APP...')

    app = QApplication(sys.argv)
    load_styles(app)

    window = MainWindow()
    window.setWindowTitle('AF-SCADA')
    window.showMaximized()
    sys.exit(app.exec())

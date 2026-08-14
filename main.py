from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from app_utils import load_styles


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    load_styles(app)

    window = MainWindow()
    window.setWindowTitle('AF-SCADA')
    window.show()
    sys.exit(app.exec())

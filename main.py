from PySide6.QtWidgets import QApplication

from main_window import MainWindow
from utils import load_styles

def main():
    import sys
    app = QApplication(sys.argv)
    load_styles(app)

    window = MainWindow()
    window.setWindowTitle('AF-SCADA')
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

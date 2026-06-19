from PySide6.QtWidgets import QApplication, QMainWindow, QWidget

from pages.main_page import MainPage
from utils import load_styles


def main():
    import sys
    app = QApplication(sys.argv)
    load_styles(app)

    window = QMainWindow()
    window.setWindowTitle("Мнемосхема")
    window.resize(1280, 720)

    main_page = MainPage(window)

    window.setCentralWidget(main_page)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

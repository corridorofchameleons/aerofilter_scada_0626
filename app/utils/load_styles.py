from pathlib import Path

STYLE_FILE = Path(__file__).resolve().parent.parent / 'styles' / 'styles.qss'

def load_styles(app):
    try:
        with open(STYLE_FILE) as f:
            style_sheet = f.read()
            app.setStyleSheet(style_sheet)
            print("Файл стилей успешно загружен.")
    except FileNotFoundError:
        print("Файл style.qss не найден. Продолжаем со стилями по умолчанию.")
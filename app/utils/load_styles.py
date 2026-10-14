from pathlib import Path
from loguru import logger

STYLE_FILE = Path(__file__).resolve().parent.parent / 'styles' / 'styles.qss'

def load_styles(app):
    try:
        with open(STYLE_FILE) as f:
            style_sheet = f.read()
            app.setStyleSheet(style_sheet)
            logger.success('Stylesheet loaded successfully')

    except FileNotFoundError:
        logger.warning('Stylesheet not found. Using default')
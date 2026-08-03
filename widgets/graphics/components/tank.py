from PySide6.QtCore import QRectF, QPointF, Slot
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath, QPolygonF, QLinearGradient, Qt, QBrush
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup

from widgets.graphics.constants import TANK_HALF_WIDTH, TANK_HALF_HEIGHT, TANK_LINE_WIDTH, \
    BORDER_COLOR, TANK_CORNER_HEIGHT, ELEMENT_GRADIENT_LIGHT, ELEMENT_GRADIENT_DARK, \
    ELEMENT_GRADIENT_DARKER, TANK_HEATER_HEIGHT, TANK_HEATER_WIDTH, HEATER_ON_COLOR, TANK_BACKGROUND_COLOR, \
    HEATER_OFF_COLOR, TANK_LAMP_SIZE, LAMP_OK_COLOR, LAMP_ALARM_COLOR, TANK_LIQUID_LEVEL_HEIGHT, \
    TANK_LIQUID_LEVEL_WIDTH, LEVEL_INDICATOR_COLOR, SCENE_SCALE


class TankBody(QGraphicsItem):
    def __init__(self):
        super().__init__()

    def boundingRect(self):
        coords = [
            int(coord) for coord in
            [
                - TANK_HALF_WIDTH,
                - TANK_HALF_HEIGHT,
                TANK_HALF_WIDTH * 2,
                TANK_HALF_HEIGHT * 2
            ]
        ]
        return QRectF(*coords)

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()

        rect = self.boundingRect()

        pen = QPen(QColor(BORDER_COLOR), TANK_LINE_WIDTH)
        painter.setPen(pen)

        body_gradient = QLinearGradient(rect.topLeft(), rect.topRight())

        body_gradient.setColorAt(0.0, ELEMENT_GRADIENT_DARKER)
        body_gradient.setColorAt(0.2, ELEMENT_GRADIENT_DARK)
        body_gradient.setColorAt(0.4, ELEMENT_GRADIENT_LIGHT)
        body_gradient.setColorAt(0.6, ELEMENT_GRADIENT_LIGHT)
        body_gradient.setColorAt(0.8, ELEMENT_GRADIENT_DARK)
        body_gradient.setColorAt(1.0, ELEMENT_GRADIENT_DARKER)

        painter.setBrush(body_gradient)

        path.addRect(rect)

        ch = int(TANK_CORNER_HEIGHT)

        cutter1 = QPolygonF([
            QPointF(rect.left(), rect.top()),
            QPointF(rect.left() + ch, rect.top()),
            QPointF(rect.left(), rect.top() + ch)
        ])

        cutter2 = QPolygonF([
            QPointF(rect.right(), rect.top()),
            QPointF(rect.right() - ch, rect.top()),
            QPointF(rect.right(), top_y := rect.top() + ch)
        ])

        cutter3 = QPolygonF([
            QPointF(rect.left(), rect.bottom()),
            QPointF(rect.left() + ch, rect.bottom()),
            QPointF(rect.left(), rect.bottom() - ch)
        ])

        cutter4 = QPolygonF([
            QPointF(rect.right(), rect.bottom()),
            QPointF(rect.right() - ch, rect.bottom()),
            QPointF(rect.right(), rect.bottom() - ch)
        ])

        tri_1 = QPainterPath()
        tri_2 = QPainterPath()
        tri_3 = QPainterPath()
        tri_4 = QPainterPath()

        tri_1.addPolygon(cutter1)
        tri_2.addPolygon(cutter2)
        tri_3.addPolygon(cutter3)
        tri_4.addPolygon(cutter4)

        path = path.subtracted(tri_1)
        path = path.subtracted(tri_2)
        path = path.subtracted(tri_3)
        path = path.subtracted(tri_4)

        painter.drawPath(path)

        painter.drawLine(
            int(rect.left() * 0.98), int(rect.top() + ch),
            int(rect.right() * 0.98), int(rect.top() + ch)
        )

        painter.drawLine(
            int(rect.left() * 0.98), int(rect.bottom() - ch),
            int(rect.right() * 0.98), int(rect.bottom() - ch)
        )


class HeaterElement(QGraphicsItem):
    def __init__(
            self,
    ):
        super().__init__()
        self.height = TANK_HEATER_HEIGHT
        self.width = TANK_HEATER_WIDTH

        self.is_active = False

    def boundingRect(self):
        return QRectF(
            - TANK_HEATER_WIDTH / 2,
            - TANK_HEATER_HEIGHT / 2,
            TANK_HEATER_WIDTH,
            TANK_HEATER_HEIGHT
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()
        w, h = r.width(), r.height()

        border_pen = QPen(Qt.NoPen)
        painter.setPen(border_pen)
        painter.setBrush(QColor(TANK_BACKGROUND_COLOR))
        painter.drawRect(r)

        # Волна
        wave_path = QPainterPath()

        start_y = r.center().y()
        wave_path.moveTo(r.left(), start_y)

        segments = 5
        step_x = w / segments

        for i in range(segments):
            x1 = r.left() + i * step_x
            x2 = x1 + step_x

            ctrl1 = QPointF(x1 + step_x * 0.5, r.top() - TANK_HEATER_HEIGHT * 0.45)
            ctrl2 = QPointF(x1 + step_x * 0.5, r.bottom() + TANK_HEATER_HEIGHT * 0.45)

            end_x = x2
            end_y = start_y

            wave_path.cubicTo(ctrl1.x(), ctrl1.y(), ctrl2.x(), ctrl2.y(), end_x, end_y)

        color = HEATER_ON_COLOR if self.is_active else HEATER_OFF_COLOR

        pen = QPen(QColor(color), 3)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(wave_path)

        border_pen = QPen(QColor(BORDER_COLOR), TANK_LINE_WIDTH)
        painter.setPen(border_pen)
        painter.drawRect(r)

    def set_active(self, val: bool):
        self.is_active = val
        self.update()


class IndicatorLamp(QGraphicsItem):
    def __init__(
            self,
            text: str | None = None
    ):
        super().__init__()
        self.text = text
        self.alarm = False

    def boundingRect(self):
        return QRectF(
            -TANK_LAMP_SIZE / 2,
            -TANK_LAMP_SIZE / 2,
            TANK_LAMP_SIZE,
            TANK_LAMP_SIZE
        )

    def set_alarm(self, val: bool):
        self.alarm = val
        self.update()

    def paint(self, painter, option, widget=None):

        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()

        pen = QPen(Qt.black, TANK_LINE_WIDTH / 2)

        color = LAMP_OK_COLOR if not self.alarm else LAMP_ALARM_COLOR

        painter.setBrush(QColor(color))
        painter.setPen(pen)

        painter.drawEllipse(r)

        if self.text:
            font = painter.font()
            font.setItalic(True)

            pen = QPen(QColor('black'))
            painter.setPen(pen)
            painter.setFont(font)

            painter.drawText(
                QRectF(
                    - 55 * SCENE_SCALE,
                    - TANK_LAMP_SIZE,
                    50 * SCENE_SCALE,
                    TANK_LAMP_SIZE * 2
                ),
                Qt.AlignCenter,
                self.text
            )


class LiquidLevel(QGraphicsItem):
    def __init__(
            self,
    ):
        super().__init__()
        self.height = TANK_LIQUID_LEVEL_HEIGHT
        self.width = TANK_LIQUID_LEVEL_WIDTH

        self.max = 100
        self.min = 20

        self.level = (self.max + self.min) / 2

    def boundingRect(self):
        return QRectF(
            - TANK_LIQUID_LEVEL_WIDTH / 2,
            - TANK_LIQUID_LEVEL_HEIGHT / 2,
            TANK_LIQUID_LEVEL_WIDTH,
            TANK_LIQUID_LEVEL_HEIGHT
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()

        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(TANK_BACKGROUND_COLOR))
        painter.drawRect(r)

        # непосредственно уровень
        start_x = r.x()
        start_y = r.y() + r.height() * (1 - self.level / 100)
        amplitude = 10

        path = QPainterPath()
        path.moveTo(start_x, start_y)

        ctrl_up = QPointF(start_x + TANK_LIQUID_LEVEL_WIDTH * 0.3, start_y - amplitude)
        ctrl_down = QPointF(start_x + TANK_LIQUID_LEVEL_WIDTH * 0.7, start_y + amplitude)
        end_point = QPointF(start_x + TANK_LIQUID_LEVEL_WIDTH, start_y)

        path.cubicTo(ctrl_up, ctrl_down, end_point)

        path.lineTo(r.right(), r.bottom())
        path.lineTo(r.left(), r.bottom())
        path.lineTo(r.left(), start_y)

        path.closeSubpath()

        painter.setBrush(QBrush(QColor(LEVEL_INDICATOR_COLOR)))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        border_pen = QPen(QColor(BORDER_COLOR), TANK_LINE_WIDTH)
        painter.setPen(border_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(r)


class Tank(QGraphicsItemGroup):
    def __init__(
            self,
            heater_fn,
            alarm_max_fn,
            alarm_min_fn,
    ):
        super().__init__()

        heater_fn.connect(self.set_heater_active)
        alarm_max_fn.connect(self.set_max_alarm)
        alarm_min_fn.connect(self.set_min_alarm)

        self.body = TankBody()

        self.heater = HeaterElement()
        self.heater.setPos(TANK_HALF_WIDTH * 0.5, TANK_HALF_HEIGHT * 0.75)

        self.liquid_level = LiquidLevel()
        self.liquid_level.setPos(TANK_HALF_WIDTH / 1.6, -TANK_HALF_HEIGHT / 6)

        self.min_lamp = IndicatorLamp('Мин.\nобъем')
        self.min_lamp.setPos(TANK_HALF_WIDTH / 5, TANK_HALF_HEIGHT / 3)
        self.max_lamp = IndicatorLamp('Макс.\nобъем')
        self.max_lamp.setPos(TANK_HALF_WIDTH / 5, -TANK_HALF_HEIGHT / 1.5)

        self.addToGroup(self.body)
        self.addToGroup(self.heater)
        self.addToGroup(self.liquid_level)
        self.addToGroup(self.min_lamp)
        self.addToGroup(self.max_lamp)


    @Slot()
    def set_heater_active(self, val: bool):
        self.heater.set_active(val)

    @Slot()
    def set_max_alarm(self, val: bool):
        self.max_lamp.set_alarm(val)

    @Slot()
    def set_min_alarm(self, val: bool):
        self.min_lamp.set_alarm(val)

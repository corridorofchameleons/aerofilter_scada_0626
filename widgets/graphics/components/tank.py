from PySide6.QtCore import QRectF, QPointF, Slot
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath, QPolygonF, QLinearGradient, Qt, QBrush, QTransform
from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup

from models.tag import BinaryTag
from mqtt.topics import COMMAND_TOPIC
from signals.mqtt import bus
from widgets.settings import Settings


class _TankBody(QGraphicsItem):
    def __init__(
            self,
            height: int,
            width: int,
    ):
        super().__init__()

        self.height = height
        self.width = width
        self.corner_height = self.height * 0.08

        self.setZValue(2)

    def boundingRect(self):
        return QRectF(
            -self.width,
            -self.height,
            self.width * 2,
            self.height * 2
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        path = QPainterPath()

        rect = self.boundingRect()

        pen = QPen(QColor(Settings.BORDER_COLOR), Settings.LINE_WIDTH)
        painter.setPen(pen)

        body_gradient = QLinearGradient(rect.topLeft(), rect.topRight())

        body_gradient.setColorAt(0.0, Settings.ELEMENT_GRADIENT_DARKER)
        body_gradient.setColorAt(0.2, Settings.ELEMENT_GRADIENT_DARK)
        body_gradient.setColorAt(0.4, Settings.ELEMENT_GRADIENT_LIGHT)
        body_gradient.setColorAt(0.6, Settings.ELEMENT_GRADIENT_LIGHT)
        body_gradient.setColorAt(0.8, Settings.ELEMENT_GRADIENT_DARK)
        body_gradient.setColorAt(1.0, Settings.ELEMENT_GRADIENT_DARKER)

        painter.setBrush(body_gradient)

        path.addRect(rect)

        ch = int(self.corner_height)

        cutter1 = QPolygonF([
            QPointF(rect.left(), rect.top()),
            QPointF(rect.left() + ch, rect.top()),
            QPointF(rect.left(), rect.top() + ch)
        ])

        cutter2 = QPolygonF([
            QPointF(rect.right(), rect.top()),
            QPointF(rect.right() - ch, rect.top()),
            QPointF(rect.right(), rect.top() + ch)
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

        transform = QTransform()
        transform.rotate(90)

        painter.drawPath(path)

        painter.drawLine(
            int(rect.left() * 0.98), int(rect.top() + ch),
            int(rect.right() * 0.98), int(rect.top() + ch)
        )

        painter.drawLine(
            int(rect.left() * 0.98), int(rect.bottom() - ch),
            int(rect.right() * 0.98), int(rect.bottom() - ch)
        )


class _HeaterElement(QGraphicsItem):
    def __init__(
            self,
            heater_tag: BinaryTag,
            height: int,
            width: int
    ):
        super().__init__()
        self.height = height
        self.width = width

        self.setCursor(Qt.PointingHandCursor)

        self._is_active = False
        self.pending = False

        self.heater_tag = heater_tag
        self.heater_tag.status_signal.connect(self.update_status)
        self.setZValue(3)


    def boundingRect(self):
        return QRectF(
            -self.width / 2,
            -self.height / 2,
            self.width,
            self.height
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()
        w, h = r.width(), r.height()

        border_pen = QPen(Qt.NoPen)
        painter.setPen(border_pen)
        painter.setBrush(QColor(Settings.BACKGROUND_COLOR))
        painter.drawRect(r)

        # Волна
        wave_path = QPainterPath()

        start_y = r.center().y()
        wave_path.moveTo(r.left(), start_y)

        segments = 10
        step_x = w / segments

        for i in range(segments):
            x1 = r.left() + i * step_x
            x2 = x1 + step_x

            ctrl1 = QPointF(x1 + step_x * 0.5, r.top() - self.height * 0.45)
            ctrl2 = QPointF(x1 + step_x * 0.5, r.bottom() + self.height * 0.45)

            end_x = x2
            end_y = start_y

            wave_path.cubicTo(ctrl1.x(), ctrl1.y(), ctrl2.x(), ctrl2.y(), end_x, end_y)

        color = Settings.HEATER_ON_COLOR if self._is_active else Settings.HEATER_OFF_COLOR

        pen = QPen(QColor(color), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(wave_path)

        border_pen = QPen(QColor(Settings.BORDER_COLOR), Settings.LINE_WIDTH)
        painter.setPen(border_pen)
        painter.drawRect(r)

    @Slot(bool)
    def update_status(self, val: bool):
        self.setCursor(Qt.PointingHandCursor)
        self._is_active = val
        self.pending = False
        self.update()

    def set_new_status(self):
        print('here')
        self.unsetCursor()
        bus.mqtt_publish_signal.emit(
            COMMAND_TOPIC,
            {
                'name': self.heater_tag.name,
                'value': not self._is_active
            }
        )


class _IndicatorLamp(QGraphicsItem):
    def __init__(
            self,
            radius: int,
            text: str | None = None
    ):
        super().__init__()
        self.radius = radius
        self.text = text
        self.alarm = False

    def boundingRect(self):
        return QRectF(
            -self.radius / 2,
            -self.radius / 2,
            self.radius,
            self.radius
        )

    def set_alarm(self, val: bool):
        self.alarm = val
        self.update()

    def paint(self, painter, option, widget=None):

        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()

        pen = QPen(Qt.black, 3)

        color = Settings.LAMP_OK_COLOR if not self.alarm else Settings.LAMP_ALARM_COLOR

        painter.setBrush(QColor(color))
        painter.setPen(pen)

        painter.drawEllipse(r)

        if self.text:
            font = painter.font()
            font.setItalic(True)

            pen = QPen(QColor(Settings.TEXT_COLOR))
            painter.setPen(pen)
            painter.setFont(font)

            painter.drawText(
                QRectF(
                    -self.radius * 4,
                    -self.radius,
                    self.radius * 3.5,
                    self.radius * 2
                ),
                Qt.AlignCenter,
                self.text
            )


class _LiquidLevel(QGraphicsItem):
    def __init__(
            self,
            height: int,
            width: int
    ):
        super().__init__()
        self.height = height
        self.width = width

        self.max = 100
        self.min = 20

        self.level = (self.max + self.min) / 2

    def boundingRect(self):
        return QRectF(
            -self.width / 2,
            -self.height / 2,
            self.width,
            self.height
        )

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        r = self.boundingRect()

        painter.setPen(Qt.NoPen)

        painter.setBrush(QColor(Settings.BACKGROUND_COLOR))
        painter.drawRect(r)

        # непосредственно уровень
        start_x = r.x()
        start_y = r.y() + r.height() * (1 - self.level / 100)
        amplitude = 10

        path = QPainterPath()
        path.moveTo(start_x, start_y)

        ctrl_up = QPointF(start_x + self.width * 0.3, start_y - amplitude)
        ctrl_down = QPointF(start_x + self.width * 0.7, start_y + amplitude)
        end_point = QPointF(start_x + self.width, start_y)

        path.cubicTo(ctrl_up, ctrl_down, end_point)

        path.lineTo(r.right(), r.bottom())
        path.lineTo(r.left(), r.bottom())
        path.lineTo(r.left(), start_y)

        path.closeSubpath()

        painter.setBrush(QBrush(QColor(Settings.LEVEL_INDICATOR_COLOR)))
        painter.setPen(Qt.NoPen)
        painter.drawPath(path)

        border_pen = QPen(QColor(Settings.BORDER_COLOR), Settings.LINE_WIDTH)
        painter.setPen(border_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(r)


class Tank(QGraphicsItemGroup):
    def __init__(
            self,
            heater_tag: BinaryTag | None,
            # alarm_max_fn,
            # alarm_min_fn,
            rotate: bool = False,
            small: bool = False,

            height: int = Settings.TANK_HEIGHT,
            width: int = Settings.TANK_WIDTH,

            heater_height: int = Settings.TANK_HEATER_HEIGHT,
            heater_width: int = Settings.TANK_HEATER_WIDTH,

            lamp_radius: int = Settings.TANK_LAMP_SIZE,
            level_height: int = Settings.TANK_LIQUID_LEVEL_HEIGHT,
            level_width: int = Settings.TANK_LIQUID_LEVEL_WIDTH
    ):
        super().__init__()

        self.height = height
        self.width = width
        self.heater_height = heater_height
        self.heater_width = heater_width

        if small:
            self.height *= 0.5
            self.width *= 0.5

        self.lamp_radius = lamp_radius
        self.level_height = level_height
        self.level_width = level_width

        self.heater_tag = heater_tag

        # heater_fn.connect(self.set_heater_active)
        # alarm_max_fn.connect(self.set_max_alarm)
        # alarm_min_fn.connect(self.set_min_alarm)

        self.body = _TankBody(self.height, self.width)
        if rotate:
            self.body.setRotation(90)
        self.addToGroup(self.body)

        self.heater = None

        if self.heater_tag:
            self.heater = _HeaterElement(self.heater_tag, self.heater_height, self.heater_width)
            self.heater.setPos(-self.width * 0.3, self.height * 0.4)
            self.addToGroup(self.heater)

        # self.liquid_level = _LiquidLevel(self.level_height, self.level_width)
        # self.liquid_level.setPos(self.width * 0.6, -self.height * 0.166)

        # self.min_lamp = _IndicatorLamp(self.lamp_radius, 'Мин.\nобъем')
        # self.min_lamp.setPos(self.width * 0.2, self.height * 0.33)
        # self.max_lamp = _IndicatorLamp(self.lamp_radius, 'Макс.\nобъем')
        # self.max_lamp.setPos(self.width * 0.2, -self.height * 0.66)

        # self.addToGroup(self.liquid_level)
        # self.addToGroup(self.min_lamp)
        # self.addToGroup(self.max_lamp)

    def mousePressEvent(self, event):
        x_clicked = event.scenePos().x()
        y_clicked = event.scenePos().y()

        if self.heater and not self.heater.pending:
            x = self.heater.scenePos().x()
            y = self.heater.scenePos().y()
            if (x - self.heater.width * 0.5 <= x_clicked < x + self.heater.width * 0.5) and \
                (y - self.heater.height * 0.5 <= y_clicked < y + self.heater.height * 0.5):
                self.heater.pending = True
                self.heater.set_new_status()

    # @Slot()
    # def set_max_alarm(self, val: bool):
    #     self.max_lamp.set_alarm(val)
    #
    # @Slot()
    # def set_min_alarm(self, val: bool):
    #     self.min_lamp.set_alarm(val)

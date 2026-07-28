from PySide6.QtWidgets import QGraphicsItem, QGraphicsObject, QGraphicsBlurEffect
from PySide6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QPainterPathStroker, QPainterPath, QPolygonF, QPen
from PySide6.QtCore import Qt, QRectF, QPointF, Slot, QLineF, QTimer

from widgets.scheme.utils.pipes import joint_polygon

THICK_WIDTH = 16
THIN_WIDTH = 8

FLOW_OFFSET = 3
FLOW_TIMER = 300


class PipeBody(QGraphicsItem):
    def __init__(
            self,
            x1: int,
            y1: int,
            x2: int,
            y2: int,
            horizontal: bool,
            start_joint: str | None = None,
            end_joint: str | None = None,
            thin: bool = False,
    ):
        super().__init__()

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.p1 = QPointF(x1, y1)
        self.p2 = QPointF(x2, y2)
        self.width = THIN_WIDTH if thin else THICK_WIDTH
        self.start_joint = start_joint
        self.end_joint = end_joint
        self.is_horizontal: bool = horizontal
        self._is_selected: bool = False

        self.setZValue(0)

        self._flow_timer = None
        self._flow_offset = 0


    @Slot(bool)
    def set_selected(self, val: bool):
        self._is_selected = val
        self.update()

    @Slot(bool)
    def start_flow(self):
        if not self._flow_timer:
            self._flow_timer = QTimer()
            self._flow_timer.timeout.connect(self._on_flow_tick)
            self._flow_timer.start(FLOW_TIMER)

    @Slot()
    def stop_flow(self):
        if self._flow_timer:
            self._flow_timer.stop()
            self._flow_timer.deleteLater()
            self._flow_timer = None

    def _on_flow_tick(self):
        self._flow_offset -= FLOW_OFFSET
        self.update()


    def boundingRect(self):
        half_w = self.width / 2.0
        rect = QRectF(self.p1, self.p2).normalized()
        return rect.adjusted(-half_w, -half_w, half_w, half_w)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Градиент трубы
        gradient = QLinearGradient(0, 0, 0, 1)

        if self._is_selected:
            c_dark = QColor("#2E7D32")
            c_light = QColor(180, 230, 205)  # Светло-ментоловый
        else:
            c_dark = QColor("#B0BEC5")
            c_light = QColor("#ECEFF1")

        gradient.setColorAt(0.0, c_dark)
        gradient.setColorAt(0.48, c_light)
        gradient.setColorAt(0.52, c_light)
        gradient.setColorAt(1.0, c_dark)

        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)

        if not self.is_horizontal:
            gradient.setStart(0, 0)
            gradient.setFinalStop(1, 0)

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)

        # Отрисовка трубы
        line_path = QPainterPath()
        line_path.moveTo(self.p1)
        line_path.lineTo(self.p2)

        stroker = QPainterPathStroker()
        stroker.setWidth(self.width)

        pipe_shape = stroker.createStroke(line_path)

        # Стык трубы
        joint_1_path = QPainterPath()
        joint_2_path = QPainterPath()

        joint_1, joint_2 = self._get_joints()
        if joint_1:
            joint_1_path.addPolygon(joint_1)
        joint_1_path.closeSubpath()
        if joint_2:
            joint_2_path.addPolygon(joint_2)
        joint_2_path.closeSubpath()

        final_shape = pipe_shape.subtracted(joint_1_path).subtracted(joint_2_path)

        painter.drawPath(final_shape)

        # Движение жидкости
        if self._flow_timer and self._flow_timer.isActive():
            pen = QPen(QColor("#1565C0"), 3)
            pen.setDashPattern([2, 20])
            pen.setCapStyle(Qt.FlatCap)

            pen.setDashOffset(self._flow_offset)

            painter.setPen(pen)
            path = QPainterPath()
            path.moveTo(self.p1)
            path.lineTo(self.p2)
            painter.drawPath(path)

    def _get_joints(self) -> tuple[QPolygonF, QPolygonF]:
        return joint_polygon(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            'horizontal' if self.is_horizontal else 'vertical',
            self.start_joint,
            self.end_joint,
            self.width
        )



# class FlowLayer(QGraphicsItem):
#     def __init__(self, p1, p2, width=5):
#         super().__init__()
#         self.p1 = QPointF(p1)
#         self.p2 = QPointF(p2)
#         self.width = width
#
#         self._timer = QTimer()
#         self._offset = 0
#         self._timer.timeout.connect(self._on_tick)
#         self._timer.start(30)
#
#     def _on_tick(self):
#         self._offset += 2
#         self.update()
#
#     def boundingRect(self):
#         return QRectF(self.p1, self.p2).normalized().adjusted(-5, -5, 5, 5)
#
#     def paint(self, painter, option, widget=None):
#         if not (self.p1 and self.p2):
#             return
#
#         line = QLineF(self.p1, self.p2)
#
#         pen = QPen(Qt.white, self.width)
#         pen.setStyle(Qt.DashLine)  # Включаем пунктир
#         pen.setCapStyle(Qt.FlatCap)
#
#         # Ключевая магия: смещаем начало штрихов
#         pen.setDashOffset(self._offset)
#
#         painter.setPen(pen)
#         painter.drawLine(line)


# class UnderGlow(QGraphicsItem):
#     def __init__(
#             self,
#             x1: int,
#             y1: int,
#             x2: int,
#             y2: int,
#             horizontal: bool,
#             thin: bool = False
#     ):
#         super().__init__()
#
#         # Сохраняем координаты углов как точки для удобства
#         self.p1 = QPointF(x1, y1)
#         self.p2 = QPointF(x2, y2)
#         self.width = THIN_WIDTH if thin else THICK_WIDTH
#         self.horizontal = horizontal
#
#         self.setZValue(-1)
#
#         blur = QGraphicsBlurEffect()
#         blur.setBlurRadius(5)
#         self.setGraphicsEffect(blur)
#
#     def boundingRect(self):
#         rect = QRectF(self.p1, self.p2).normalized()
#         return rect.adjusted(-2, -2, 2, 2)
#
#     def paint(self, painter, option, widget=None):
#         painter.setRenderHint(QPainter.Antialiasing, True)
#
#         gradient = QLinearGradient(0, 0, 0, 1)
#         gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
#
#         c = QColor(50, 205, 50, 80)
#         gradient.setColorAt(0.0, QColor(0, 0, 0, 0))
#         gradient.setColorAt(0.5, c)
#
#         pen = QPen(QBrush(gradient), self.width * 1.5)
#         pen.setCapStyle(Qt.RoundCap)
#         painter.setPen(pen)
#
#         path = QPainterPath()
#         path.moveTo(self.p1)
#         path.lineTo(self.p2)
#         painter.drawPath(path)



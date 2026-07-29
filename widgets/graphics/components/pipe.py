from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup
from PySide6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QPainterPathStroker, QPainterPath, QPolygonF, QPen
from PySide6.QtCore import Qt, QRectF, QPointF, Slot, QTimer

from widgets.graphics.utils.pipes import joint_polygon

THICK_WIDTH = 16
THIN_WIDTH = 8

FLOW_OFFSET = 3
FLOW_TIMER = 300


class PipeBody(QGraphicsItem):
    def __init__(
            self,
            p1: QPointF,
            p2: QPointF,
            width: float,
            horizontal: bool,
            start_joint: str | None = None,
            end_joint: str | None = None,
    ):
        super().__init__()

        self.p1 = p1
        self.p2 = p2
        self.width = width
        self.start_joint = start_joint
        self.end_joint = end_joint
        self.is_horizontal: bool = horizontal
        self._is_selected: bool = False

        self.setZValue(0)

    def set_selected(self, val: bool):
        self._is_selected = val
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
            c_light = QColor(180, 230, 205)
        else:
            c_dark = QColor("#78909C")  # Глубокий серо-голубой
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


    def _get_joints(self) -> tuple[QPolygonF, QPolygonF]:
        return joint_polygon(
            self.p1.x(),
            self.p1.y(),
            self.p2.x(),
            self.p2.y(),
            'horizontal' if self.is_horizontal else 'vertical',
            self.start_joint,
            self.end_joint,
            self.width
        )


class FlowLayer(QGraphicsItem):
    def __init__(
            self,
            p1: QPointF,
            p2: QPointF,
            width: float
    ):
        super().__init__()

        self.p1 = p1
        self.p2 = p2
        self.width = width

        self._flow_timer = None
        self._flow_offset = 0

    def start_flow(self):
        if not self._flow_timer:
            self._flow_timer = QTimer()
            self._flow_timer.timeout.connect(self._on_flow_tick)
            self._flow_timer.start(FLOW_TIMER)

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

    def paint(self, painter, option, widget = None):
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


class Pipe(QGraphicsItemGroup):
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
            ratio: float = 1.2,
    ):
        super().__init__()

        self.p1 = QPointF(x1 * ratio, y1 * ratio)
        self.p2 = QPointF(x2 * ratio, y2 * ratio)
        self.width = THIN_WIDTH * ratio if thin else THICK_WIDTH * ratio

        self.pipe_body = PipeBody(
            p1=self.p1,
            p2=self.p2,
            width=self.width,
            horizontal=horizontal,
            start_joint=start_joint,
            end_joint=end_joint
        )
        self.flow_layer = FlowLayer(
            p1=self.p1,
            p2=self.p2,
            width=self.width
        )
        self.addToGroup(self.pipe_body)
        self.addToGroup(self.flow_layer)

    @Slot(bool)
    def set_selected(self, val: bool):
        self.pipe_body.set_selected(val)

    @Slot()
    def start_flow(self):
        self.flow_layer.start_flow()

    @Slot()
    def stop_flow(self):
        self.flow_layer.stop_flow()

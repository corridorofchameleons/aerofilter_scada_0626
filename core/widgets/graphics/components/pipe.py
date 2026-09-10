import math

from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup
from PySide6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QPainterPathStroker, QPainterPath, QPolygonF, QPen
from PySide6.QtCore import Qt, QRectF, QPointF, Slot, QTimer, QObject

from core.widgets.graphics.components.arrow import Arrow
from app.utils.pipes import joint_polygon
from core.settings import Settings


class _PipeBody(QGraphicsItem):
    def __init__(
            self,
            width: float,
            length: float,
            start_joint: str | None = None,
            end_joint: str | None = None,
    ):
        super().__init__()

        self.width = width
        self.length = length

        self.p1 = QPointF(-self.length / 2, 0)
        self.p2 = QPointF(self.length / 2, 0)

        self.start_joint = start_joint
        self.end_joint = end_joint
        self._is_selected: bool = False

        self.setZValue(0)

    def set_selected(self, val: bool):
        self._is_selected = val
        self.update()

    def is_selected(self):
        return self._is_selected

    def boundingRect(self):
        return QRectF(
            -self.length / 2,
            -self.width / 2,
            self.length,
            self.width
        )

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        # Градиент трубы
        gradient = QLinearGradient(0, 0, 0, 1)

        if self._is_selected:
            c_dark = QColor(Settings.PIPE_OUTER_COLOR_ACTIVE)
            c_light = QColor(Settings.PIPE_INNER_COLOR_INACTIVE)
        else:
            c_dark = QColor(Settings.PIPE_OUTER_COLOR_INACTIVE)
            c_light = QColor(Settings.PIPE_INNER_COLOR_INACTIVE)

        gradient.setColorAt(0.0, c_dark)
        gradient.setColorAt(0.48, c_light)
        gradient.setColorAt(0.52, c_light)
        gradient.setColorAt(1.0, c_dark)

        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)

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
            self.start_joint,
            self.end_joint,
            self.width
        )


class _FlowLayer(QGraphicsItem):
    def __init__(
            self,
            p1: QPointF,
            p2: QPointF,
            width: float,
            length: float
    ):
        super().__init__()

        self.width = width
        self.length = length

        self.p1 = QPointF(-self.length / 2, 0)
        self.p2 = QPointF(self.length / 2, 0)

        # self.p1 = p1
        # self.p2 = p2
        # self.width = width

        self._flow_timer = None
        self._flow_offset = 0

    def boundingRect(self):
        return QRectF(
            -self.length / 2,
            -self.width / 2,
            self.length,
            self.width
        )

    def start_flow(self):
        if not self._flow_timer:
            self._flow_timer = QTimer()
            self._flow_timer.timeout.connect(self._on_flow_tick)
            self._flow_timer.start(Settings.STREAM_TIMER)

    def stop_flow(self):
        if self._flow_timer:
            self._flow_timer.stop()
            self._flow_timer.deleteLater()
            self._flow_timer = None

    def _on_flow_tick(self):
        self._flow_offset -= Settings.STREAM_OFFSET
        self.update()

    def paint(self, painter, option, widget = None):
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._flow_timer and self._flow_timer.isActive():
            pen = QPen(QColor(Settings.FLOW_COLOR), 2)
            pen.setDashPattern([4, 15])
            pen.setCapStyle(Qt.FlatCap)

            pen.setDashOffset(self._flow_offset)

            painter.setPen(pen)
            path = QPainterPath()
            path.moveTo(self.p1)
            path.lineTo(self.p2)
            painter.drawPath(path)


class _ArrowLayer(QGraphicsItemGroup):
    def __init__(
            self,
            parent: QGraphicsItemGroup,
            coords: tuple,
            thin: bool,
            length: int | float,
    ):
        super().__init__()

        self.coords = coords
        self.length = length

        self.parent = parent
        self.thin = thin

        for c in self.coords:
            offset = self.length * c
            arrow = Arrow(small=self.thin)
            arrow.setPos(-self.length / 2 + offset, 0)
            self.addToGroup(arrow)


class Pipe(QGraphicsItemGroup):
    def __init__(
            self,
            x: int | float,
            y: int | float,
            x2: int | float | None = None,
            y2: int | float | None = None,
            start_joint: str | None = None,
            end_joint: str | None = None,
            thin: bool = False,
            contour: tuple = (),
            arrows: tuple = (),
            activate_flow=None
    ):
        super().__init__()
        self.contour = set(contour)

        if activate_flow:
            activate_flow.connect(self.handle_flow_change)

        self.x1 = x
        self.y1 = y

        self.x2 = x2 if x2 is not None else x
        self.y2 = y2 if y2 is not None else y

        self.thin = thin

        self.p1 = QPointF(self.x1, self.y1)
        self.p2 = QPointF(self.x2, self.y2)

        self.pos_x = (self.x1 + self.x2) * 0.5
        self.pos_y = (self.y1 + self.y2) * 0.5

        self.length = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.width = Settings.PIPE_THIN_WIDTH if self.thin else Settings.PIPE_THICK_WIDTH

        self.rotation_angle = math.degrees(math.atan2((self.y2 - self.y1), (self.x2 - self.x1)))

        self.flow_active = None

        self.pipe_body = _PipeBody(
            width=self.width,
            length=self.length,
            start_joint=start_joint,
            end_joint=end_joint
        )
        self.pipe_body.setRotation(self.rotation_angle)
        self.pipe_body.setPos(self.pos_x, self.pos_y)

        self.flow_layer = _FlowLayer(
            p1=self.p1,
            p2=self.p2,
            width=self.width,
            length=self.length
        )
        self.flow_layer.setRotation(self.rotation_angle)
        self.flow_layer.setPos(self.pos_x, self.pos_y)

        self.arrow_layer = _ArrowLayer(
            self,
            coords=arrows,
            thin=self.thin,
            length=self.length,
        )
        self.arrow_layer.setPos(self.pos_x, self.pos_y)
        self.arrow_layer.setRotation(self.rotation_angle)

        self.addToGroup(self.pipe_body)
        self.addToGroup(self.flow_layer)
        self.addToGroup(self.arrow_layer)

    @Slot(set)
    def handle_contour_change(self, active_conts: set):
        was_active = self.flow_active
        self.stop_flow()
        if self.contour.intersection(active_conts):
            self.set_selected(True)
        else:
            self.set_selected(False)
        if was_active:
            self.start_flow()

    @Slot(set, bool)
    def handle_flow_change(self, contours: set, start: bool):
        if contours.intersection(self.contour):
            if start:
                self.start_flow()
            else:
                self.stop_flow()

    def set_selected(self, val: bool):
        self.pipe_body.set_selected(val)

    def start_flow(self):
        # здесь важно обозначить, что поток в принципе существует,
        # чтобы если труба попала в рабочий контур, по ней бы поползли частицы
        # (труба ждет и готова принять поток)
        self.flow_active = True

        if self.pipe_body.is_selected():
            self.flow_layer.start_flow()
            self.update()

    def stop_flow(self):
        self.flow_active = False
        self.flow_layer.stop_flow()
        self.update()

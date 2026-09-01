from PySide6.QtWidgets import QGraphicsItem, QGraphicsItemGroup
from PySide6.QtGui import QPainter, QColor, QBrush, QLinearGradient, QPainterPathStroker, QPainterPath, QPolygonF, QPen
from PySide6.QtCore import Qt, QRectF, QPointF, Slot, QTimer, QObject

from widgets.graphics.components.arrow import Arrow
from widgets.graphics.utils.pipes import joint_polygon
from widgets.settings import Settings


class _PipeBody(QGraphicsItem):
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

    def is_selected(self):
        return self._is_selected

    def boundingRect(self):
        half_w = self.width / 2.0
        rect = QRectF(self.p1, self.p2).normalized()
        return rect.adjusted(-half_w, -half_w, half_w, half_w)

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


class _FlowLayer(QGraphicsItem):
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
            self._flow_timer.start(Settings.STREAM_TIMER)

    def stop_flow(self):
        if self._flow_timer:
            self._flow_timer.stop()
            self._flow_timer.deleteLater()
            self._flow_timer = None

    def _on_flow_tick(self):
        self._flow_offset -= Settings.STREAM_OFFSET
        self.update()

    def boundingRect(self):
        half_w = self.width / 2.0
        rect = QRectF(self.p1, self.p2).normalized()
        return rect.adjusted(-half_w, -half_w, half_w, half_w)

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


class _ArrowLayer(QObject):
    def __init__(
            self,
            parent: QGraphicsItemGroup,
            arrow_number: int,
            rotation_angle: int,
            horizontal: bool,
            thin: bool,
            x1: int | float,
            x2: int | float,
            y1: int | float,
            y2: int | float
    ):
        super().__init__()
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.parent = parent
        self.arrow_num = arrow_number
        self.rotation_angle = rotation_angle
        self.horizontal = horizontal
        self.thin = thin

        if self.horizontal:
            try:
                arrow_step = 1 / (self.arrow_num - 1)
                arrow_points = [i * arrow_step for i in range(self.arrow_num)]
                length = self.x2 - self.x1
                start = self.x1 + length * 0.05
                end = self.x1 + length * 0.95
                new_length = end - start
                self.arrow_coords = [[start + new_length * arst, (self.y1 + self.y2) * 0.5] for arst in arrow_points]
            except ZeroDivisionError:
                self.arrow_coords = [[(self.x1 + self.x2) * 0.5, (self.y1 + self.y2) * 0.5]]

        else:
            arrow_step = 1 / (self.arrow_num + 1)
            arrow_points = [i * arrow_step for i in range(1, self.arrow_num + 1)]
            height = self.y2 - self.y1
            self.arrow_coords = [[(self.x1 + self.x2) * 0.5, self.y1 + height * arst] for arst in arrow_points]

        for c in self.arrow_coords:
            arrow = Arrow(small=self.thin, rotation_angle=self.rotation_angle)
            arrow.setPos(c[0], c[1])
            arrow.setZValue(2)
            self.parent.addToGroup(arrow)


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
            contour: tuple = (),
            arrow_num: int = 2,
            arrow_rotation = 0,
            activate_flow=None
    ):
        super().__init__()
        self.contour = set(contour)

        if activate_flow:
            activate_flow.connect(self.handle_flow_change)

        self.horizontal = horizontal

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.thin = thin
        self.arrow_num = arrow_num
        self.rotation_angle = arrow_rotation

        self.p1 = QPointF(self.x1, self.y1)
        self.p2 = QPointF(self.x2, self.y2)
        self.width = Settings.PIPE_THIN_WIDTH if self.thin else Settings.PIPE_THICK_WIDTH

        self.counter = 0

        self.flow_active = None

        self.pipe_body = _PipeBody(
            p1=self.p1,
            p2=self.p2,
            width=self.width,
            horizontal=self.horizontal,
            start_joint=start_joint,
            end_joint=end_joint
        )

        self.flow_layer = _FlowLayer(
            p1=self.p1,
            p2=self.p2,
            width=self.width
        )
        self.arrow_layer = _ArrowLayer(
            self,
            arrow_number=self.arrow_num,
            rotation_angle=self.rotation_angle,
            horizontal=self.horizontal,
            thin=self.thin,
            x1=self.x1,
            x2=self.x2,
            y1=self.y1,
            y2=self.y2
        )
        self.addToGroup(self.pipe_body)
        self.addToGroup(self.flow_layer)

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

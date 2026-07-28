from PySide6.QtCore import QPointF
from PySide6.QtGui import QPolygonF

def _get_right_horizontal_pg(x, y, width, reverse=False) -> QPolygonF:
    if reverse:
        p1 = QPointF(x + width / 2, y - width / 2)
        p2 = QPointF(x + width / 2, y + width / 2)
        p3 = QPointF(x - width / 2, y - width / 2)
    else:
        p1 = QPointF(x - width /2, y + width / 2)
        p2 = QPointF(x - width / 2, y - width / 2)
        p3 = QPointF(x + width / 2, y + width / 2)
    tri = QPolygonF()
    tri.append([p1, p2, p3])
    return tri


def _get_left_horizontal_pg(x, y, width, reverse=False) -> QPolygonF:
    if reverse:
        p1 = QPointF(x + width / 2, y - width / 2)
        p2 = QPointF(x + width / 2, y + width / 2)
        p3 = QPointF(x - width / 2, y + width / 2)
    else:
        p1 = QPointF(x - width / 2, y + width / 2)
        p2 = QPointF(x - width / 2, y - width / 2)
        p3 = QPointF(x + width / 2, y - width / 2)
    tri = QPolygonF()
    tri.append([p1, p2, p3])
    return tri


def _get_sharp_horizontal_pg(x, y, width, reverse=False):
    if reverse:
        p1 = QPointF(x - width / 2, y - width / 2)
        p2 = QPointF(x + width / 2, y - width / 2)
        p3 = QPointF(x + width / 2, y + width / 2)
        p4 = QPointF(x - width / 2, y + width / 2)
        p5 = QPointF(x + width / 2, y)
    else:
        p1 = QPointF(x + width / 2, y + width / 2)
        p2 = QPointF(x - width / 2, y + width / 2)
        p3 = QPointF(x - width / 2, y - width / 2)
        p4 = QPointF(x + width / 2, y - width / 2)
        p5 = QPointF(x - width / 2, y)
    tri = QPolygonF()
    tri.append([p1, p2, p3, p4, p5])
    return tri


def _get_right_vertical_pg(x, y, width, reverse=False):
    if reverse:
        p1 = QPointF(x + width / 2, y - width / 2)
        p2 = QPointF(x - width / 2, y - width / 2)
        p3 = QPointF(x - width / 2, y + width / 2)
    else:
        p1 = QPointF(x - width / 2, y + width / 2)
        p2 = QPointF(x + width / 2, y + width / 2)
        p3 = QPointF(x + width / 2, y - width / 2)
    tri = QPolygonF()
    tri.append([p1, p2, p3])
    return tri


def _get_left_vertical_pg(x, y, width, reverse=False):
    if reverse:
        p1 = QPointF(x - width / 2, y - width / 2)
        p2 = QPointF(x + width / 2, y - width / 2)
        p3 = QPointF(x + width / 2, y + width / 2)
    else:
        p1 = QPointF(x + width / 2, y + width / 2)
        p2 = QPointF(x - width / 2, y + width / 2)
        p3 = QPointF(x - width / 2, y - width / 2)
    tri = QPolygonF()
    tri.append([p1, p2, p3])
    return tri


def _get_sharp_vertical_pg(x, y, width, reverse=False):
    if reverse:
        p1 = QPointF(x + width / 2, y - width / 2)
        p2 = QPointF(x + width / 2, y + width / 2)
        p3 = QPointF(x, y - width / 2)
        p4 = QPointF(x - width / 2, y + width / 2)
        p5 = QPointF(x - width / 2, y - width / 2)
    else:
        p1 = QPointF(x - width / 2, y + width / 2)
        p2 = QPointF(x - width / 2, y - width / 2)
        p3 = QPointF(x, y + width / 2)
        p4 = QPointF(x + width / 2, y - width / 2)
        p5 = QPointF(x + width / 2, y + width / 2)
    tri = QPolygonF()
    tri.append([p1, p2, p3, p4, p5])
    return tri


def joint_polygon(
        x1,
        y1,
        x2,
        y2,
        direction,
        start,
        end,
        width
) -> tuple[QPolygonF | None, QPolygonF | None]:

    if direction == 'horizontal':
        pg_1 = None
        pg_2 = None

        if start == 'right':
            pg_1 = _get_right_horizontal_pg(x1, y1, width, x1 > x2)
        elif start == 'left':
            pg_1 = _get_left_horizontal_pg(x1, y1, width, x1 > x2)
        elif start == 'sharp':
            pg_1 = _get_sharp_horizontal_pg(x1, y1, width, x1 > x2)

        if end == 'left':
            pg_2 = _get_right_horizontal_pg(x2, y2, width, x1 < x2)
        elif end == 'right':
            pg_2 = _get_left_horizontal_pg(x2, y2, width, x1 < x2)
        elif end == 'sharp':
            pg_2 = _get_sharp_horizontal_pg(x2, y2, width, x1 < x2)

        return pg_1, pg_2

    elif direction == 'vertical':
        pg_1 = None
        pg_2 = None

        if start == 'right':
            pg_1 = _get_right_vertical_pg(x1, y1, width, y1 < y2)
        elif start == 'left':
            pg_1  = _get_left_vertical_pg(x1, y1, width, y1 < y2)
        elif start == 'sharp':
            pg_1 = _get_sharp_vertical_pg(x1, y1, width, y1 < y2)

        if end == 'left':
            pg_2 = _get_right_vertical_pg(x2, y2, width, y1 > y2)
        if end == 'right':
            pg_2 = _get_left_vertical_pg(x2, y2, width, y1 > y2)
        elif end == 'sharp':
            pg_2 = _get_sharp_vertical_pg(x2, y2, width, y1 > y2)

        return pg_1, pg_2

    else:
        return None, None

    #
    #     case 'vert_right':
    #         p1 = QPointF(self.x1 - self.width / 2, self.y1 + self.width / 2)
    #         p2 = QPointF(self.x1 + self.width / 2, self.y1 + self.width / 2)
    #         p3 = QPointF(self.x1 + self.width / 2, self.y1 - self.width / 2)
    #         tri = QPolygonF()
    #         tri.append([p1, p2, p3])
    #         return tri
    #     case 'vert_left':
    #         p1 = QPointF(self.x1 + self.width / 2, self.y1 + self.width / 2)
    #         p2 = QPointF(self.x1 - self.width / 2, self.y1 + self.width / 2)
    #         p3 = QPointF(self.x1 - self.width / 2, self.y1 - self.width / 2)
    #         tri = QPolygonF()
    #         tri.append([p1, p2, p3])
    #         return tri
    #     # case 'vert_sharp':
    #     #     p1 = QPointF(self.x1 - self.width, self.y1 - self.width / 2)
    #     #     p2 = QPointF(self.x1, self.y1 - self.width / 2)
    #     #     p3 = QPointF(self.x1, self.y1 + self.width / 2)
    #     #     p4 = QPointF(self.x1 - self.width, self.y1 + self.width / 2)
    #     #     p5 = QPointF(self.x1, self.y1)
    #     #     tri = QPolygonF()
    #     #     tri.append([p1, p2, p3, p4, p5])
    #     #     return tri
    #     case _:
    #         return None

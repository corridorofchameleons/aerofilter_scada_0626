from app.ui.layouts.scheme.scheme import Scheme
from core.widgets.graphics.components.pipe import Pipe
from core.widgets.graphics.components.pump import Pump
from core.widgets.graphics.components.tank import Tank, _HeaterElement
from core.widgets.graphics.components.valve import Valve


def test_valve(qtbot, tags):
    scheme = Scheme()

    v1 = Valve(contour=(1,), tag=tags.tag_v1, signal=scheme.handle_contour_status)
    v2 = Valve(contour=(2,), tag=tags.tag_v2, signal=scheme.handle_contour_status)

    pipe1 = Pipe(x=0, y=0, x2=10, contour=(1,2))
    pipe2 = Pipe(x=0, y=0, x2=10, contour=(3,4))

    scheme.set_active_contours.connect(pipe1.handle_contour_change)
    scheme.set_active_contours.connect(pipe1.handle_contour_change)

    v1.set_new_status()
    v2.set_new_status()

    assert v1.tag.pending == True
    assert v2.tag.pending == True

    v1.tag.handle_value(True)

    assert v1.tag.pending == False
    assert pipe1.pipe_body._is_selected == True
    assert pipe2.pipe_body._is_selected == False

    v2.tag.handle_value(True)

    assert v2.tag.pending == False
    assert pipe1.pipe_body._is_selected == True
    assert pipe2.pipe_body._is_selected == False

    v1.tag.handle_value(False)

    assert v1.tag.pending == False
    assert pipe1.pipe_body._is_selected == True
    assert pipe2.pipe_body._is_selected == False

    v2.tag.handle_value(False)

    assert v2.tag.pending == False
    assert pipe1.pipe_body._is_selected == False
    assert pipe2.pipe_body._is_selected == False


def test_pump(qtbot, tags):
    scheme = Scheme()

    p1 = Pump(contour=(1,), tag=tags.tag_v1, switch_flow=scheme.activate_flow)
    p2 = Pump(contour=(2,), tag=tags.tag_v2, switch_flow=scheme.activate_flow)

    pipe1 = Pipe(x=0, y=0, x2=10, contour=(1, 2))
    pipe1.pipe_body.set_selected(True)
    pipe2 = Pipe(x=0, y=0, x2=10, contour=(3, 4))
    pipe2.pipe_body.set_selected(True)

    scheme.activate_flow.connect(pipe1.handle_flow_change)
    scheme.activate_flow.connect(pipe1.handle_flow_change)

    p1.set_new_status()
    p2.set_new_status()

    assert p1.tag.pending == True
    assert p2.tag.pending == True

    p1.tag.handle_value(True)
    p2.tag.handle_value(True)

    assert p1.tag.pending == False
    assert p2.tag.pending == False
    assert pipe1.flow_active == True
    assert pipe2.flow_active == False


def test_tank_heater(qtbot, tags):
    h = _HeaterElement(tag=tags.tag_v1, height=1, width=1)

    h.set_new_status()

    assert h.tag.pending == True

    h.tag.handle_value(True)

    assert h.tag.pending == False
    assert h.tag.value == True

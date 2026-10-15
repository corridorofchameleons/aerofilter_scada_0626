from core.widgets.ui_widgets.button import SwitchButton
from app.ui.components.tables.cells.table_cell import Cell
from core.widgets.ui_widgets.value_box import ValueBox
from core.widgets.ui_widgets.value_input import ValueInput
from tests.test_core.conftest import BUTTON_ACTIVE, BUTTON_INACTIVE, FLOAT_VALUE


def test_button(qtbot, tags):
    button = SwitchButton(
        text_active=BUTTON_ACTIVE,
        text_inactive=BUTTON_INACTIVE,
        tag=tags.tag_button,
    )

    assert button.text() == BUTTON_INACTIVE
    assert button.error_widget == False

    button.set_new_status()

    assert button.tag.pending == True

    button.tag.handle_value(True)
    button.tag.update_ui.emit()

    assert button.text() == BUTTON_ACTIVE
    assert button.tag.pending == False

    button.tag.set_disabled_value(True)
    button.set_new_status()

    assert button.tag.pending == False

    button.custom = True
    button.set_new_status()

    assert button.tag.pending == False

def text_cell(qtbot, tags):
    cell = Cell(
        tag=tags.tag_3
    )

    cell.tag.update_ui.emit()

    assert cell.text == str(FLOAT_VALUE)

    cell.tag.value = 69.0
    cell.tag.update_ui.emit()

    assert cell.text == str(69.0)

def test_value_box(qtbot, tags):
    vb = ValueBox(
        tag=tags.tag_3,
        title='title'
    )

    assert vb.tag._timer_active == True

    vb.tag.update_ui.emit()

    assert vb.value_label.text() == str(FLOAT_VALUE)

    vb.tag.value = 69.0
    vb.tag.update_ui.emit()

    assert vb.value_label.text() == str(69.0)

def test_value_input(qtbot, tags):
    vi = ValueInput(
        tag=tags.tag_3,
        title='title'
    )

    vi.tag.update_ui.emit()

    assert vi.value_input.text() == str(FLOAT_VALUE)

    vi.set_new_status(69.0)

    assert vi.tag.pending == True
    assert vi.tag._timer_active == True

    vi.tag.pending = True

    vi.tag.handle_value(69.0)

    assert vi.value_input.text() == str(69.0)
    assert vi.tag.pending == False

def test_value_input_validate_value(qtbot, tags):
    vi1 = ValueInput(
        tag=tags.tag_3,
        title='title',
        min_value = 10,
        max_value = 20
    )

    vi2 = ValueInput(
        tag=tags.tag_3,
        title='title'
    )

    res_1 = vi1._validated_value('0')
    res_2 = vi1._validated_value('11,5')
    res_3 = vi1._validated_value('11.5')
    res_4 = vi1._validated_value('11.5.5')
    res_5 = vi2._validated_value('0')
    res_6 = vi2._validated_value('11.5.5')

    assert res_1 is None
    assert res_2 == 11.5
    assert res_3 == 11.5
    assert res_4 is None
    assert res_5 == 0.0
    assert res_6 is None

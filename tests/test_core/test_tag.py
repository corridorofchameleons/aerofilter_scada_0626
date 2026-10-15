from tests.test_core.conftest import INT_VALUE, FLOAT_VALUE, NEW_INT_VALUE, NEW_FLOAT_VALUE


def test_create_tag(tags):

    assert tags.tag_1.name == 'tag_1'
    assert tags.tag_1.update_value == tags.tag_1.set_bool_value
    assert tags.tag_1.initial_value is None

    assert tags.tag_2.name == 'tag_2'
    assert tags.tag_2.update_value == tags.tag_2.set_int_value
    assert tags.tag_2.initial_value == INT_VALUE

    assert tags.tag_3.name == 'tag_3'
    assert tags.tag_3.update_value == tags.tag_3.set_float_value
    assert tags.tag_3.initial_value == FLOAT_VALUE

def test_set_disabled_value(tags):

    tags.tag_1.set_disabled_value(True)
    tags.tag_2.set_disabled_value(False)

    assert tags.tag_1.disabled == True
    assert tags.tag_2.disabled == False

def test_set_initial(tags):

    tags.tag_1.set_initial()
    tags.tag_2.set_initial()
    tags.tag_3.set_initial()

    assert tags.tag_1.value is None
    assert tags.tag_2.value == INT_VALUE
    assert tags.tag_3.value == FLOAT_VALUE

def test_set_value(tags):

    tags.tag_1.set_value(True)
    tags.tag_2.set_value(NEW_INT_VALUE)
    tags.tag_3.set_value(NEW_FLOAT_VALUE)

    assert tags.tag_1._timer_active == True
    assert tags.tag_2._timer_active == False
    assert tags.tag_3._timer_active == True


def test_handle_value(tags):

    tags.tag_1.handle_value(True)
    tags.tag_2.handle_value(NEW_INT_VALUE)
    tags.tag_3.handle_value(NEW_FLOAT_VALUE)

    assert tags.tag_1.value == True
    assert tags.tag_1._timer_active == False
    assert tags.tag_2.value == NEW_INT_VALUE
    assert tags.tag_2._timer_active == False
    assert tags.tag_3.value == NEW_FLOAT_VALUE
    assert tags.tag_3._timer_active == False


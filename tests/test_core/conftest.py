import pytest

from core.models.tag import Tag, ValueType

INT_VALUE = 1
NEW_INT_VALUE = 2
FLOAT_VALUE = 1.3
NEW_FLOAT_VALUE = 1.4

BUTTON_ACTIVE = 'button_active'
BUTTON_INACTIVE = 'button_inactive'

@pytest.fixture
def tags():
    ns_name = 'ns_name'

    class Tags:
        tag_1 = Tag(ns_name, ValueType.type_bool)
        tag_2 = Tag(ns_name, ValueType.type_int, initial=INT_VALUE, timeout=0)
        tag_3 = Tag(ns_name, ValueType.type_float, initial=FLOAT_VALUE, timeout=200)
        tag_button = Tag(ns_name, ValueType.type_bool, initial=False, timeout=200)
        tag_v1 = Tag(ns_name, ValueType.type_bool, initial=False)
        tag_v2 = Tag(ns_name, ValueType.type_bool, initial=False)
    return Tags

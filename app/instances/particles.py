from typing import OrderedDict

from core.models.tag import Tag, ValueType

NS_NAME_TABLE = 'value_table'
NS_NAME_BUTTONS = 'particle_select'
PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200, 'class')

TEST_NUM = 11
OIL_PREFIX = 'oil_'
FUEL_PREFIX = 'fuel_'

class MetaStand:
    stand_select = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_int, initial=0)

class DisableTags:
    oil_before_disabled = Tag(NS_NAME_TABLE, value_type=ValueType.type_bool, initial=True)

class OilTable:
    oil_test_num = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_int, initial=11)
    oil_effectiveness = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_float)
    oil_before_index = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_int, initial=0)
    oil_after_index = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_int, initial=0)
    oil_select_before = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool, initial=False)
    oil_select_after = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool, initial=False)
    oil_clear_tests = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)

class FuelTable:
    fuel_test_num = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_int, initial=11)
    fuel_effectiveness = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_float)
    fuel_before_index = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_int, initial=0)
    fuel_after_index = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_int, initial=0)
    fuel_select_before = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool, initial=False)
    fuel_select_after = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool, initial=False)
    fuel_clear_tests = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)


class OilParticles:
    ns_name = NS_NAME_TABLE

class FuelParticles:
    ns_name = NS_NAME_TABLE

class OilEffectiveness:
    ns_name = NS_NAME_TABLE

class FuelEffectiveness:
    ns_name = NS_NAME_TABLE


def generate_particle_attrs(prefix: str, particles: tuple, class_):
    particle_dict = OrderedDict((i, OrderedDict()) for i in range(1, TEST_NUM + 1))

    for i in range(1, TEST_NUM + 1):
        index_name_before = f'{prefix}before_index_{i}'
        index_tag_before = Tag(ns_name=class_.ns_name, name=index_name_before, value_type=ValueType.type_int, initial=0)
        index_name_after = f'{prefix}after_index_{i}'
        index_tag_after = Tag(ns_name=class_.ns_name, name=index_name_after, value_type=ValueType.type_int, initial=0)

        setattr(
            class_,
            index_name_before,
            index_tag_before
        )
        setattr(
            class_,
            index_name_after,
            index_tag_after
        )

        particle_dict[i][1] = {}
        particle_dict[i][2] = {}
        particle_dict[i][1]['index'] = index_tag_before
        particle_dict[i][2]['index'] = index_tag_after

        particle_dict[i][1]['items'] = {}
        particle_dict[i][2]['items'] = {}

        for val in particles:
            if isinstance(val, int):
                name_before = f'{prefix}before_{val}um_{i}'
                tag_before = Tag(ns_name=class_.ns_name, name=name_before, value_type=ValueType.type_int)
                name_after = f'{prefix}after_{val}um_{i}'
                tag_after = Tag(ns_name=class_.ns_name, name=name_after, value_type=ValueType.type_int)
            else:
                name_before = f'{prefix}before_{val}_{i}'
                tag_before = Tag(ns_name=class_.ns_name, name=name_before, value_type=ValueType.type_int)
                name_after = f'{prefix}after_{val}_{i}'
                tag_after = Tag(ns_name=class_.ns_name, name=name_after, value_type=ValueType.type_int)
            setattr(
                class_,
                name_before,
                tag_before
            )
            setattr(
                class_,
                name_after,
                tag_after
            )
            particle_dict[i][1]['items'][val] = tag_before
            particle_dict[i][2]['items'][val] = tag_after

    return class_.__dict__, particle_dict


def generate_effectiveness_attrs(prefix: str, particles: tuple, class_):
    eff_dict = OrderedDict()

    for val in particles:
        name = f'{prefix}effectiveness_{val}'
        tag = Tag(ns_name=class_.ns_name, value_type=ValueType.type_float, name=name)
        eff_dict[val] = tag

        setattr(
            class_,
            name,
            tag
        )

    return class_.__dict__, eff_dict


oil_particles_dict, oil_particle_dict_data = generate_particle_attrs(OIL_PREFIX, PARTICLES, OilParticles)
# oil_particles_dict = oil_particles_class.__dict__
fuel_particles_dict, fuel_particle_dict_data = generate_particle_attrs(FUEL_PREFIX, PARTICLES, FuelParticles)
# fuel_particles_dict = oil_particles_class.__dict__

oil_table_data_dict = OilTable.__dict__
fuel_table_data_dict = FuelTable.__dict__
meta_stand_dict = MetaStand.__dict__

oil_effectiveness_dict, oil_effectiveness_dict_data = generate_effectiveness_attrs(OIL_PREFIX, PARTICLES, OilEffectiveness)
# oil_effectiveness_dict = oil_effectiveness_obj.__dict__
fuel_effectiveness_dict, fuel_effectiveness_dict_data = generate_effectiveness_attrs(FUEL_PREFIX, PARTICLES, FuelEffectiveness)
# fuel_effectiveness_dict = fuel_effectiveness_obj.__dict__

# for k, v in oil_particle_dict_data.items():
#     print(k, v)
#
# for k, v in oil_particles_dict.items():
#     print(k, v)
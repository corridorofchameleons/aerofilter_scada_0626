from typing import OrderedDict

from core.models.tag import IntTag, FloatTag, BoolTag, Tag

NS_NAME_TABLE = 'value_table'
NS_NAME_BUTTONS = 'particle_select'
PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200, 'class')

TEST_NUM = 11
OIL_PREFIX = 'oil_'
FUEL_PREFIX = 'fuel_'

class MetaStand:
    stand_select = IntTag(NS_NAME_BUTTONS, initial=0)

class DisableTags:
    oil_before_disabled = BoolTag(NS_NAME_TABLE, initial=True)

class OilTable:
    oil_test_num = IntTag(NS_NAME_BUTTONS, initial=11)
    oil_effectiveness = FloatTag(NS_NAME_BUTTONS)
    oil_before_index = IntTag(NS_NAME_BUTTONS, initial=0)
    oil_after_index = IntTag(NS_NAME_BUTTONS, initial=0)
    oil_select_before = BoolTag(NS_NAME_BUTTONS, initial=False, disable_tag=DisableTags.oil_before_disabled)
    oil_select_after = BoolTag(NS_NAME_BUTTONS, initial=False)
    oil_clear_tests = BoolTag(NS_NAME_BUTTONS)

class FuelTable:
    fuel_test_num = IntTag(NS_NAME_BUTTONS, initial=11)
    fuel_effectiveness = FloatTag(NS_NAME_BUTTONS)
    fuel_before_index = IntTag(NS_NAME_BUTTONS, initial=0)
    fuel_after_index = IntTag(NS_NAME_BUTTONS, initial=0)
    fuel_select_before = BoolTag(NS_NAME_BUTTONS, initial=False)
    fuel_select_after = BoolTag(NS_NAME_BUTTONS, initial=False)
    fuel_clear_tests = BoolTag(NS_NAME_BUTTONS)


class Particles:
    ns_name = NS_NAME_TABLE


class Effectiveness:
    ns_name = NS_NAME_TABLE


def generate_particle_attrs(prefix: str, particles: tuple):
    particle_dict = OrderedDict((i, OrderedDict()) for i in range(1, TEST_NUM + 1))

    particles_obj = Particles()
    for i in range(1, TEST_NUM + 1):
        index_name_before = f'{prefix}before_index_{i}'
        index_tag_before = IntTag(ns_name=Particles.ns_name, name=index_name_before, initial=0)
        index_name_after = f'{prefix}after_index_{i}'
        index_tag_after = IntTag(ns_name=Particles.ns_name, name=index_name_after, initial=0)

        setattr(
            particles_obj,
            index_name_before,
            index_tag_before
        )
        setattr(
            particles_obj,
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
                tag_before = IntTag(ns_name=Particles.ns_name, sign=val)
                name_after = f'{prefix}after_{val}um_{i}'
                tag_after = IntTag(ns_name=Particles.ns_name, sign=val)
            else:
                name_before = f'{prefix}before_{val}_{i}'
                tag_before = IntTag(ns_name=Particles.ns_name, sign=val)
                name_after = f'{prefix}after_{val}_{i}'
                tag_after = IntTag(ns_name=Particles.ns_name, sign=val)

            setattr(
                particles_obj,
                name_before,
                tag_before
            )
            setattr(
                particles_obj,
                name_after,
                tag_after
            )
            particle_dict[i][1]['items'][val] = tag_before
            particle_dict[i][2]['items'][val] = tag_after

    return particles_obj, particle_dict


def generate_effectiveness_attrs(prefix: str, particles: tuple):
    class_obj = Effectiveness()
    eff_dict = OrderedDict()

    for val in particles:
        name = f'{prefix}effectiveness_{val}'
        tag = FloatTag(ns_name=Effectiveness.ns_name, name=name)
        eff_dict[val] = tag

        setattr(
            class_obj,
            name,
            tag
        )

    return class_obj, eff_dict


oil_particles_obj, oil_particle_dict_data = generate_particle_attrs(OIL_PREFIX, PARTICLES)
oil_particles_dict = oil_particles_obj.__dict__
fuel_particles_obj, fuel_particle_dict_data = generate_particle_attrs(FUEL_PREFIX, PARTICLES)
fuel_particles_dict = fuel_particles_obj.__dict__

oil_table_data_dict = OilTable.__dict__
fuel_table_data_dict = FuelTable.__dict__
meta_stand_dict = MetaStand.__dict__

oil_effectiveness_obj, oil_effectiveness_dict_data = generate_effectiveness_attrs(OIL_PREFIX, PARTICLES)
oil_effectiveness_dict = oil_effectiveness_obj.__dict__
fuel_effectiveness_obj, fuel_effectiveness_dict_data = generate_effectiveness_attrs(FUEL_PREFIX, PARTICLES)
fuel_effectiveness_dict = fuel_effectiveness_obj.__dict__

for k, v in oil_particle_dict_data.items():
    print(k, v)


from cgi import initlog
from typing import OrderedDict

from core.models.tag import IntTag, FloatTag, BoolTag

NS_NAME_TABLE = 'value_table'
NS_NAME_BUTTONS = 'particle_select'
PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200, 'class')

TEST_NUM = 11
OIL_PREFIX = 'oil_'
FUEL_PREFIX = 'fuel_'

class MetaStand:
    stand_select = IntTag(NS_NAME_BUTTONS, initial=0)

class OilTable:
    oil_test_num = IntTag(NS_NAME_BUTTONS, initial=11)
    oil_effectiveness = FloatTag(NS_NAME_BUTTONS)
    oil_before_index = IntTag(NS_NAME_BUTTONS)
    oil_after_index = IntTag(NS_NAME_BUTTONS)
    oil_select_before = BoolTag(NS_NAME_BUTTONS, initial=False)
    oil_select_after = BoolTag(NS_NAME_BUTTONS, initial=False)

class FuelTable:
    fuel_test_num = IntTag(NS_NAME_BUTTONS, initial=11)
    fuel_effectiveness = FloatTag(NS_NAME_BUTTONS)
    fuel_before_index = FloatTag(NS_NAME_BUTTONS)
    fuel_after_index = FloatTag(NS_NAME_BUTTONS)
    fuel_select_before = BoolTag(NS_NAME_BUTTONS, initial=False)
    fuel_select_after = BoolTag(NS_NAME_BUTTONS, initial=False)

class Particles:
    ns_name = NS_NAME_TABLE

def generate_particle_attrs(prefix: str, particles: tuple):
    particle_dict = OrderedDict((i, OrderedDict()) for i in range(1, TEST_NUM + 1))

    particles_obj = Particles()
    for i in range(1, TEST_NUM + 1):
        for val in particles:
            particle_dict[i][val] = {}
            name_before = f'{prefix}before_{val}um_{i}'
            tag_before = IntTag(ns_name=Particles.ns_name, sign=val)
            name_after = f'{prefix}after_{val}um_{i}'
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

            particle_dict[i][val][name_before] = tag_before
            particle_dict[i][val][name_after] = tag_after

    return particles_obj, particle_dict


oil_particles_data, oil_particle_dict_data = generate_particle_attrs(OIL_PREFIX, PARTICLES)
oil_particles_dict = oil_particles_data.__dict__
fuel_particles_data, fuel_particle_dict_data = generate_particle_attrs(FUEL_PREFIX, PARTICLES)
fuel_particles_dict = fuel_particles_data.__dict__

oil_table_data_dict = OilTable.__dict__
fuel_table_data_dict = FuelTable.__dict__
meta_stand_dict = MetaStand.__dict__

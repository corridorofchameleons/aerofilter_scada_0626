from typing import OrderedDict

from core.models.tag import IntTag

NS_NAME = 'pamas_s40'
PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200, 'class')

TEST_NUM = 11
OIL_PREFIX = 'oil_'
FUEL_PREFIX = 'fuel_'

class Particles:
    ns_name = NS_NAME

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

from typing import OrderedDict

from core.models.tag import IntTag

NS_NAME = 'pamas_s40'
OIL_PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200)
FUEL_PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200)
OIL_PREFIX = 'oil_'
FUEL_PREFIX = 'fuel_'

class Particles:
    ns_name = NS_NAME

def generate_particle_data(prefix: str, particles: tuple):
    fuel_particles = Particles()

    for val in particles:
        setattr(
            fuel_particles,
            f'{prefix}before_{val}um',
            IntTag(ns_name=Particles.ns_name, sign=val)
        )
        setattr(
            fuel_particles,
            f'{prefix}after_{val}um',
            IntTag(ns_name=Particles.ns_name, sign=val)
        )
    return fuel_particles


oil_particles_data = generate_particle_data(OIL_PREFIX, OIL_PARTICLES)
oil_particles_dict = oil_particles_data.__dict__
fuel_particles_data = generate_particle_data(FUEL_PREFIX, FUEL_PARTICLES)
fuel_particles_dict = fuel_particles_data.__dict__

def generate_particle_dict_data(data: dict):
    d = OrderedDict()
    for name, tag in data.items():
        if tag.sign not in d:
            d[tag.sign] = [None, None]
        if 'before' in name:
            d[tag.sign][0] = tag
        elif 'after' in name:
            d[tag.sign][1] = tag
    return d

oil_particle_dict_data = generate_particle_dict_data(oil_particles_dict)
fuel_particle_dict_data = generate_particle_dict_data(fuel_particles_dict)

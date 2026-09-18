from core.models.tag import IntTag

NS_NAME = 'pamas_s40'
OIL_PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200)
FUEL_PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200)
OIL_PREFIX = 'oil_particle_'
FUEL_PREFIX = 'fuel_particle_'

class OilParticles:
    pass

class FuelParticles:
    pass


def generate_oil_particle_data():
    oil_particles = OilParticles()
    oil_particles.ns_name = NS_NAME

    for val in OIL_PARTICLES:
        setattr(
            oil_particles,
            f'{OIL_PREFIX}{val}um',
            IntTag(oil_particles.ns_name)
        )
    return oil_particles.__dict__

def generate_fuel_particle_data():
    fuel_particles = OilParticles()
    fuel_particles.ns_name = NS_NAME

    for val in OIL_PARTICLES:
        setattr(
            fuel_particles,
            f'{OIL_PREFIX}{val}um',
            IntTag(fuel_particles.ns_name)
        )
    return fuel_particles.__dict__

oil_particles_data = generate_oil_particle_data()
fuel_particles_data = generate_fuel_particle_data()

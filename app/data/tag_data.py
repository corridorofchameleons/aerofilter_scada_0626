from app.instances.particles import oil_particles_dict, fuel_particles_dict
from app.instances.stands import oil_stand_dict, fuel_stand_dict

TAG_DATA = oil_stand_dict | fuel_stand_dict | oil_particles_dict | fuel_particles_dict

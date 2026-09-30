from app.instances.particles import oil_particles_dict, fuel_particles_dict, oil_table_data_dict, fuel_table_data_dict, \
    meta_stand_dict, oil_effectiveness_dict, fuel_effectiveness_dict
from app.instances.stands import oil_stand_dict, fuel_stand_dict, disable_tags_dict

TAG_DATA = (oil_stand_dict | fuel_stand_dict | oil_particles_dict | fuel_particles_dict |
            meta_stand_dict | oil_table_data_dict | fuel_table_data_dict | disable_tags_dict |
            oil_effectiveness_dict | fuel_effectiveness_dict)

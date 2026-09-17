from core.models.tag import Tag, BoolTag, FloatTag

OIL_PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200)

STAND_NAME = 'delta_as200'

class Particle:
    def __init__(
            self,
            stand_name: str,
            particle: int,
    ):
        name = f'{stand_name}_particle.{particle}um'
        self.tag = Tag(STAND_NAME)


class FuelStand:
    name = 'fuel_stand'

    fuel_stand = BoolTag(STAND_NAME)
    num = 2

    fuel_probe_after_6ka3 = BoolTag(STAND_NAME)
    fuel_probe_before_6ka4 = BoolTag(STAND_NAME)
    fuel_mixer_input_valve = BoolTag(STAND_NAME)
    fuel_mixer_output_valve = BoolTag(STAND_NAME)

    fuel_pressure_before = FloatTag(STAND_NAME)
    fuel_pressure_after = FloatTag(STAND_NAME)
    fuel_temperature_before = FloatTag(STAND_NAME)
    fuel_temperature_after = FloatTag(STAND_NAME)
    fuel_moisture_before = FloatTag(STAND_NAME)
    fuel_moisture_after = FloatTag(STAND_NAME)
    fuel_tank_temperature = FloatTag(STAND_NAME)
    fuel_flow_meter = FloatTag(STAND_NAME)

    fuel_main_pump = BoolTag(STAND_NAME)
    fuel_mixing_pump = BoolTag(STAND_NAME)

    fuel_tank_heater = BoolTag(STAND_NAME)

    fuel_light = BoolTag(STAND_NAME)

    fuel_set_tank_temperature = FloatTag(STAND_NAME)
    fuel_set_pump_frequency = FloatTag(STAND_NAME)
    fuel_set_flow = FloatTag(STAND_NAME)

        # particles = [Particle('oil', n) for n in OIL_PARTICLES]

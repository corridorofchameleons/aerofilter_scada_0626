from core.models.tag import Tag, BoolTag, FloatTag

OIL_PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200)


class Particle:
    def __init__(
            self,
            stand_name: str,
            particle: int,
    ):
        name = f'{stand_name}_particle.{particle}um'
        self.tag = Tag()


class FuelStand:
    name = 'fuel_stand'

    fuel_stand = BoolTag()
    num = 2

    fuel_probe_after_6ka3 = BoolTag()
    fuel_probe_before_6ka4 = BoolTag()
    fuel_mixer_input_valve = BoolTag()
    fuel_mixer_output_valve = BoolTag()

    fuel_pressure_before = FloatTag()
    fuel_pressure_after = FloatTag()
    fuel_temperature_before = FloatTag()
    fuel_temperature_after = FloatTag()
    fuel_moisture_before = FloatTag()
    fuel_moisture_after = FloatTag()
    fuel_tank_temperature = FloatTag()
    fuel_flow_meter = FloatTag()

    fuel_main_pump = BoolTag()
    fuel_mixing_pump = BoolTag()

    fuel_tank_heater = BoolTag()

    fuel_light = BoolTag()

    fuel_set_tank_temperature = FloatTag()
    fuel_set_pump_frequency = FloatTag()
    fuel_set_flow = FloatTag()

        # particles = [Particle('oil', n) for n in OIL_PARTICLES]

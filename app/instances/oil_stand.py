from core.models.tag import Tag, ValueType, BoolTag, FloatTag

OIL_PARTICLES = (2, 3, 4, 5, 6, 7, 8, 10, 15, 20, 25, 30, 50, 100, 150, 200)


class Particle:
    def __init__(
            self,
            stand_name: str,
            particle: int,
    ):
        name = f'{stand_name}_particle.{particle}um'
        self.tag = Tag()


class OilStand:
    name = 'oil_stand'

    oil_stand = BoolTag()
    num = 1

    oil_probe_after_6ka3 = BoolTag()
    oil_probe_before_6ka4 = BoolTag()
    oil_mixer_input_valve = BoolTag()
    oil_mixer_output_valve = BoolTag()

    oil_pressure_before = FloatTag()
    oil_pressure_after = FloatTag()
    oil_temperature_before = FloatTag()
    oil_temperature_after = FloatTag()
    oil_moisture_before = FloatTag()
    oil_moisture_after = FloatTag()
    oil_tank_temperature = FloatTag()
    oil_flow_meter = FloatTag()

    oil_main_pump = BoolTag()
    oil_mixing_pump = BoolTag()

    oil_tank_heater = BoolTag()

    oil_light = BoolTag()

    oil_set_tank_temperature = FloatTag()
    oil_set_pump_frequency = FloatTag()
    oil_set_flow = FloatTag()

        # particles = [Particle('oil', n) for n in OIL_PARTICLES]

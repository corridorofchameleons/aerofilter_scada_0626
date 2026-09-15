from core.models.tag import Tag

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

    oil_stand = Tag()
    num = 1

    oil_counter_after_valve: Tag = Tag()
    oil_counter_before_valve: Tag = Tag()
    oil_mixer_input_valve: Tag = Tag()
    oil_mixer_output_valve: Tag = Tag()

    oil_pressure_before: Tag = Tag()
    oil_pressure_after: Tag = Tag()
    oil_temperature_before: Tag = Tag()
    oil_temperature_after: Tag = Tag()
    oil_moisture_before: Tag = Tag()
    oil_moisture_after: Tag = Tag()
    oil_tank_temperature: Tag = Tag()
    oil_flow_meter: Tag = Tag()

    oil_main_pump: Tag = Tag()
    oil_mixing_pump: Tag = Tag()

    oil_tank_heater: Tag = Tag()

    oil_light: Tag = Tag()

    oil_set_tank_temperature: Tag = Tag()
    oil_set_pump_frequency: Tag = Tag()
    oil_set_flow: Tag = Tag()

        # particles = [Particle('oil', n) for n in OIL_PARTICLES]

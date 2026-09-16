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


class FuelStand:
    name = 'fuel_stand'

    fuel_stand = Tag()
    num = 2

    fuel_counter_after_valve: Tag = Tag()
    fuel_counter_before_valve: Tag = Tag()
    fuel_mixer_input_valve: Tag = Tag()
    fuel_mixer_output_valve: Tag = Tag()

    fuel_pressure_before: Tag = Tag()
    fuel_pressure_after: Tag = Tag()
    fuel_temperature_before: Tag = Tag()
    fuel_temperature_after: Tag = Tag()
    fuel_moisture_before: Tag = Tag()
    fuel_moisture_after: Tag = Tag()
    fuel_tank_temperature: Tag = Tag()
    fuel_flow_meter: Tag = Tag()

    fuel_main_pump: Tag = Tag()
    fuel_mixing_pump: Tag = Tag()

    fuel_tank_heater: Tag = Tag()

    fuel_light: Tag = Tag()

    fuel_set_tank_temperature: Tag = Tag()
    fuel_set_pump_frequency: Tag = Tag()
    fuel_set_flow: Tag = Tag()

        # particles = [Particle('oil', n) for n in OIL_PARTICLES]

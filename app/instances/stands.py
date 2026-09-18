from core.models.tag import BoolTag, FloatTag

NS_NAME = 'delta_as200'

class OilStand:
    name = 'oil_stand'

    oil_stand = BoolTag(NS_NAME)
    num = 1

    oil_probe_after_6ka3 = BoolTag(NS_NAME)
    oil_probe_before_6ka4 = BoolTag(NS_NAME)
    oil_mixer_input_valve = BoolTag(NS_NAME)
    oil_mixer_output_valve = BoolTag(NS_NAME)

    oil_pressure_before = FloatTag(NS_NAME)
    oil_pressure_after = FloatTag(NS_NAME)
    oil_temperature_before = FloatTag(NS_NAME)
    oil_temperature_after = FloatTag(NS_NAME)
    oil_moisture_before = FloatTag(NS_NAME)
    oil_moisture_after = FloatTag(NS_NAME)
    oil_tank_temperature = FloatTag(NS_NAME)
    oil_flow_meter = FloatTag(NS_NAME)

    oil_main_pump = BoolTag(NS_NAME)
    oil_mixing_pump = BoolTag(NS_NAME)

    oil_tank_heater = BoolTag(NS_NAME)

    oil_light = BoolTag(NS_NAME)

    oil_set_tank_temperature = FloatTag(NS_NAME)
    oil_set_pump_frequency = FloatTag(NS_NAME)
    oil_set_flow = FloatTag(NS_NAME)


class FuelStand:
    name = 'fuel_stand'

    fuel_stand = BoolTag(NS_NAME)
    num = 2

    fuel_probe_after_6ka3 = BoolTag(NS_NAME)
    fuel_probe_before_6ka4 = BoolTag(NS_NAME)
    fuel_mixer_input_valve = BoolTag(NS_NAME)
    fuel_mixer_output_valve = BoolTag(NS_NAME)

    fuel_pressure_before = FloatTag(NS_NAME)
    fuel_pressure_after = FloatTag(NS_NAME)
    fuel_temperature_before = FloatTag(NS_NAME)
    fuel_temperature_after = FloatTag(NS_NAME)
    fuel_moisture_before = FloatTag(NS_NAME)
    fuel_moisture_after = FloatTag(NS_NAME)
    fuel_tank_temperature = FloatTag(NS_NAME)
    fuel_flow_meter = FloatTag(NS_NAME)

    fuel_main_pump = BoolTag(NS_NAME)
    fuel_mixing_pump = BoolTag(NS_NAME)

    fuel_tank_heater = BoolTag(NS_NAME)

    fuel_light = BoolTag(NS_NAME)

    fuel_set_tank_temperature = FloatTag(NS_NAME)
    fuel_set_pump_frequency = FloatTag(NS_NAME)
    fuel_set_flow = FloatTag(NS_NAME)


oil_stand_data = OilStand.__dict__
fuel_stand_data = FuelStand.__dict__

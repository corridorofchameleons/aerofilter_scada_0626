from core.models.tag import BoolTag, FloatTag, IntTag

NS_NAME = 'delta_as200'
NS_NAME_PUMPS = 'pump_values'

class DisableTags:
    oil_probe_disabled = BoolTag(NS_NAME, initial=True)
    fuel_probe_disabled = BoolTag(NS_NAME, initial=True)

class OilStand:
    name = 'Масляный стенд'
    num = 1

    oil_probe_after_6ka3 = BoolTag(NS_NAME, disable_tag=DisableTags.oil_probe_disabled)
    oil_probe_before_6ka4 = BoolTag(NS_NAME, disable_tag=DisableTags.oil_probe_disabled)

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

    oil_main_pump_start = BoolTag(NS_NAME)
    oil_mixing_pump_start = BoolTag(NS_NAME)

    oil_tank_heater = BoolTag(NS_NAME)

    oil_light = BoolTag(NS_NAME)

    oil_set_tank_temperature = FloatTag(NS_NAME)
    oil_pump_frequency_setpoint = FloatTag(NS_NAME_PUMPS)
    oil_set_flow = FloatTag(NS_NAME)


class FuelStand:
    name = 'Топливный стенд'
    num = 2

    fuel_probe_after_6ka3 = BoolTag(NS_NAME, disable_tag=DisableTags.fuel_probe_disabled)
    fuel_probe_before_6ka4 = BoolTag(NS_NAME, disable_tag=DisableTags.fuel_probe_disabled)

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

    fuel_main_pump_start = BoolTag(NS_NAME)
    fuel_mixing_pump_start = BoolTag(NS_NAME)

    fuel_tank_heater = BoolTag(NS_NAME)

    fuel_light = BoolTag(NS_NAME)

    fuel_set_tank_temperature = FloatTag(NS_NAME)
    fuel_pump_frequency_setpoint = FloatTag(NS_NAME_PUMPS)
    fuel_set_flow = FloatTag(NS_NAME)

oil_stand_dict = OilStand.__dict__
fuel_stand_dict = FuelStand.__dict__
disable_tags_dict = DisableTags.__dict__

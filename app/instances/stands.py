from core.models.tag import Tag, ValueType

NS_NAME = 'delta_as200'
NS_NAME_PUMPS = 'pump_values'

class OilStand:
    name = 'Масляный стенд'
    num = 1

    oil_probe_after_6ka3 = Tag(NS_NAME, value_type=ValueType.type_bool)
    oil_probe_before_6ka4 = Tag(NS_NAME, value_type=ValueType.type_bool)

    oil_mixer_input_valve = Tag(NS_NAME, value_type=ValueType.type_bool)
    oil_mixer_output_valve = Tag(NS_NAME, value_type=ValueType.type_bool)

    oil_pressure_before = Tag(NS_NAME, value_type=ValueType.type_float)
    oil_pressure_after = Tag(NS_NAME, value_type=ValueType.type_float)
    oil_temperature_before = Tag(NS_NAME, value_type=ValueType.type_float)
    oil_temperature_after = Tag(NS_NAME, value_type=ValueType.type_float)
    oil_moisture_before = Tag(NS_NAME, value_type=ValueType.type_float)
    oil_moisture_after = Tag(NS_NAME, value_type=ValueType.type_float)
    oil_tank_temperature = Tag(NS_NAME, value_type=ValueType.type_float)
    oil_flow_meter = Tag(NS_NAME, value_type=ValueType.type_float)

    oil_main_pump_start = Tag(NS_NAME, value_type=ValueType.type_bool)
    oil_mixing_pump_start = Tag(NS_NAME, value_type=ValueType.type_bool)

    oil_tank_heater = Tag(NS_NAME, value_type=ValueType.type_bool)

    oil_light = Tag(NS_NAME, value_type=ValueType.type_bool)

    oil_set_tank_temperature = Tag(NS_NAME, value_type=ValueType.type_float)
    oil_pump_frequency_setpoint = Tag(NS_NAME_PUMPS, value_type=ValueType.type_float)
    oil_set_flow = Tag(NS_NAME, value_type=ValueType.type_float)


class FuelStand:
    name = 'Топливный стенд'
    num = 2

    fuel_probe_after_6ka3 = Tag(NS_NAME, value_type=ValueType.type_bool)
    fuel_probe_before_6ka4 = Tag(NS_NAME, value_type=ValueType.type_bool)

    fuel_mixer_input_valve = Tag(NS_NAME, value_type=ValueType.type_bool)
    fuel_mixer_output_valve = Tag(NS_NAME, value_type=ValueType.type_bool)

    fuel_pressure_before = Tag(NS_NAME, value_type=ValueType.type_float)
    fuel_pressure_after = Tag(NS_NAME, value_type=ValueType.type_float)
    fuel_temperature_before = Tag(NS_NAME, value_type=ValueType.type_float)
    fuel_temperature_after = Tag(NS_NAME, value_type=ValueType.type_float)
    fuel_moisture_before = Tag(NS_NAME, value_type=ValueType.type_float)
    fuel_moisture_after = Tag(NS_NAME, value_type=ValueType.type_float)
    fuel_tank_temperature = Tag(NS_NAME, value_type=ValueType.type_float)
    fuel_flow_meter = Tag(NS_NAME, value_type=ValueType.type_float)

    fuel_main_pump_start = Tag(NS_NAME, value_type=ValueType.type_bool)
    fuel_mixing_pump_start = Tag(NS_NAME, value_type=ValueType.type_bool)

    fuel_tank_heater = Tag(NS_NAME, value_type=ValueType.type_bool)

    fuel_light = Tag(NS_NAME, value_type=ValueType.type_bool)

    fuel_set_tank_temperature = Tag(NS_NAME, value_type=ValueType.type_float)
    fuel_pump_frequency_setpoint = Tag(NS_NAME_PUMPS, value_type=ValueType.type_float)
    fuel_set_flow = Tag(NS_NAME, value_type=ValueType.type_float)

oil_stand_dict = OilStand.__dict__
fuel_stand_dict = FuelStand.__dict__

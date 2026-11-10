from core.models.tag import Tag, ValueType

NS_NAME = 'delta_as200'
NS_NAME_PUMPS = 'pump_values'
NS_NAME_BUTTONS = 'stand_buttons'
NS_NAME_VT = 'virtual_telemetry'

class OilStand:
    name = 'Масляный стенд'
    num = 1

    oil_probe_after_6ka4 = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)
    oil_probe_before_6ka3 = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)

    oil_pollutant_inlet_6ka1 = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)
    oil_pollutant_outlet_6ka2 = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)

    oil_pressure_before = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    oil_pressure_after = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    oil_pressure_delta = Tag(NS_NAME_VT, value_type=ValueType.type_float, log=False)
    oil_temperature_before = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    oil_temperature_after = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    oil_moisture_before = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    oil_moisture_after = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    oil_flow_meter = Tag(NS_NAME, value_type=ValueType.type_float, log=False)

    oil_main_pump_start = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)
    oil_mixing_pump_start = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)

    oil_heat_button = Tag(NS_NAME, value_type=ValueType.type_bool)

    oil_pump_mode = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)
    oil_pollutant_supply = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)
    oil_clean_system = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)
    oil_light = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool, initial=False)

    oil_tank_temp_setpoint = Tag(NS_NAME_VT, value_type=ValueType.type_float)
    oil_tank_temp = Tag(NS_NAME_VT, value_type=ValueType.type_float, log=False)

    oil_pump_frequency_setpoint = Tag(NS_NAME_PUMPS, value_type=ValueType.type_float, initial=0.0)
    oil_increment_freq = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)
    oil_decrement_freq = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)

    oil_flow_setpoint = Tag(NS_NAME_VT, value_type=ValueType.type_float)
    oil_expected_flow = Tag(NS_NAME_VT, value_type=ValueType.type_float)


class FuelStand:
    name = 'Топливный стенд'
    num = 2

    fuel_probe_after_6ka8 = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)
    fuel_probe_before_6ka7 = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)

    fuel_pollutant_inlet_6ka5 = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)
    fuel_pollutant_outlet_6ka6 = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)

    fuel_main_pump_start = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)
    fuel_mixing_pump_start = Tag(NS_NAME, value_type=ValueType.type_bool, initial=False)

    fuel_pressure_before = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    fuel_pressure_after = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    fuel_pressure_delta = Tag(NS_NAME_VT, value_type=ValueType.type_float, log=False)
    fuel_temperature_before = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    fuel_temperature_after = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    fuel_moisture_before = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    fuel_moisture_after = Tag(NS_NAME, value_type=ValueType.type_float, log=False)
    fuel_flow_meter = Tag(NS_NAME, value_type=ValueType.type_float, log=False)

    fuel_heat_button = Tag(NS_NAME, value_type=ValueType.type_bool)

    fuel_pump_mode = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)
    fuel_pollutant_supply = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)
    fuel_clean_system = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)
    fuel_light = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool, initial=False)

    fuel_tank_temp_setpoint = Tag(NS_NAME_VT, value_type=ValueType.type_float)
    fuel_tank_temp = Tag(NS_NAME_VT, value_type=ValueType.type_float, log=False)

    fuel_pump_frequency_setpoint = Tag(NS_NAME_PUMPS, value_type=ValueType.type_float, initial=0.0)
    fuel_increment_freq = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)
    fuel_decrement_freq = Tag(NS_NAME_BUTTONS, value_type=ValueType.type_bool)

    fuel_flow_setpoint = Tag(NS_NAME_VT, value_type=ValueType.type_float)
    fuel_expected_flow = Tag(NS_NAME_VT, value_type=ValueType.type_float)


oil_stand_dict = OilStand.__dict__
fuel_stand_dict = FuelStand.__dict__

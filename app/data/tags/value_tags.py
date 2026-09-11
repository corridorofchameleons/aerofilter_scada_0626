from app.data.signals.values import value_signals
from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from core.models.tag import Tag


class ValueTags:
    units = {
        OilStand.set_tank_temperature: Tag(OilStand.set_tank_temperature, signal_fn=value_signals.oil_tank_temp),
        OilStand.set_pump_frequency: Tag(OilStand.set_pump_frequency, signal_fn=value_signals.oil_pump_freq),
        OilStand.set_flow: Tag(OilStand.set_flow, signal_fn=value_signals.oil_flow),

        FuelStand.set_tank_temperature: Tag(FuelStand.set_tank_temperature, signal_fn=value_signals.fuel_tank_temp),
        FuelStand.set_pump_frequency: Tag(FuelStand.set_pump_frequency, signal_fn=value_signals.fuel_pump_freq),
        FuelStand.set_flow: Tag(FuelStand.set_flow, signal_fn=value_signals.fuel_flow),
    }

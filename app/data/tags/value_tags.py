from app.data.signals.values import value_signals
from app.data.stands.fuel_stand import FuelStand
from app.data.stands.oil_stand import OilStand
from core.models.tag import Tag


class ValueTags:
    units = {
        OilStand.set_tank_temperature: Tag(OilStand.set_tank_temperature, signal_fn=value_signals.oil_tank_temp),
        FuelStand.set_tank_temperature: Tag(FuelStand.set_tank_temperature, signal_fn=value_signals.fuel_tank_temp),
    }

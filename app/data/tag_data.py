from app.instances.fuel_stand import FuelStand
from app.instances.oil_stand import OilStand

TAG_DATA = OilStand.__dict__ | FuelStand.__dict__

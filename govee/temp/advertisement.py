from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from govee.temp.const import GOVEE_OUI
from govee.temp.util import decode_temp, decode_humidity, c_to_f


class GoveeAdvertisement:
    def __init__(self, device: BLEDevice, advertisement: AdvertisementData):
        self._advertisement = advertisement
        self._device = device

        self._battery = None
        self._humidity = None
        self._temperature = None

        self._process_5075()

    def _process_5075(self):
        data_value = int(self._advertisement.manufacturer_data[60552][1:4].hex(), 16)
        self._battery = int(self._advertisement.manufacturer_data[60552][4])
        self._temperature = c_to_f(decode_temp(data_value))
        self._humidity = decode_humidity(data_value)

    def dict(self):
        return {
            'name': self._device.name,
            'address': self._device.address,
            'battery': self._battery,
            'humidity': self._humidity,
            'temperature': self._temperature,
        }

    def __repr__(self):
        return str(self.dict())


def process_advertisement(device: BLEDevice, advertisement: AdvertisementData):
    if not str(device.address).lower().startswith(GOVEE_OUI):
        return
    advertisement = GoveeAdvertisement(device, advertisement)
    return advertisement

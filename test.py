import asyncio
from bleak import BleakClient, BleakScanner, BleakError
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from govee.temp.util import decode_temp, decode_humidity, c_to_f


async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        if str(d.address).startswith('A4:C1:38'):
            print(d)
            async with BleakClient(d.address) as client:
                print(await client.get_services())
            break


GOVEE_OUI = "a4:c1:38"


def callback(device: BLEDevice, adv_data: AdvertisementData):
    if not str(device.address).lower().startswith(GOVEE_OUI):
        return
    print(device.address, "RSSI:", device.rssi, adv_data)
    data_value = int(adv_data.manufacturer_data[60552][1:4].hex(), 16)
    battery = int(adv_data.manufacturer_data[60552][4])
    temperature = c_to_f(decode_temp(data_value))
    humidity = decode_humidity(data_value)
    print(temperature, humidity, battery)


async def get():
    scanner = BleakScanner()
    scanner.register_detection_callback(callback)
    while True:
        await scanner.start()
        await asyncio.sleep(0.5)
        await scanner.stop()


def discover(timeout: float = 15.0):
    async def _discover_async():
        async with BleakScanner() as scanner:
            await asyncio.sleep(timeout)
            devices = await scanner.get_discovered_devices()
            devices = filter(lambda device: str(device.address).lower().startswith(GOVEE_OUI), devices)
            return list(devices)

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_discover_async())


def main():
    devices = discover(5)
    print(devices)


if __name__ == '__main__':
    main()

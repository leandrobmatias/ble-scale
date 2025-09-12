import asyncio
import os
from bleak import BleakScanner, BleakClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEVICE_NAME = os.getenv("BLE_DEVICE_NAME")
CHARACTERISTIC_UUID = os.getenv("BLE_DEVICE_MAC")  # Add this to your .env


class BLEDeviceReader:
    def __init__(self, device_name: str, characteristic_uuid: str):
        self.device_name = device_name
        self.characteristic_uuid = characteristic_uuid
        self.device_address = None

    async def find_device(self):
        devices = await BleakScanner.discover()
        for d in devices:
            if d.name == self.device_name:
                self.device_address = d.address
                print(f"Found device: {d.name} [{d.address}]")
                return d.address
        print(f"Device '{self.device_name}' not found.")
        return None

    async def read_value(self):
        if not self.device_address:
            await self.find_device()
        if not self.device_address:
            return None
        async with BleakClient(self.device_address) as client:
            if await client.is_connected():
                value = await client.read_gatt_char(self.characteristic_uuid)
                print(f"Read value: {value}")
                return value
            else:
                print("Failed to connect to device.")
                return None


async def main():
    if not DEVICE_NAME or not CHARACTERISTIC_UUID:
        print("Please set BLE_DEVICE_NAME and BLE_CHARACTERISTIC_UUID in your .env file.")
        return
    reader = BLEDeviceReader(DEVICE_NAME, CHARACTERISTIC_UUID)
    await reader.read_value()


if __name__ == "__main__":
    asyncio.run(main())

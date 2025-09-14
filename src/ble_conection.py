# ble_conection.py
# Defines BLE device configuration using environment variables.
# Author: Leandro
# Date: 2025-09-12

# File History:
# 2025-09-12: Initial creation by Leandro.
# 2025-09-14: Add PrintHandler and handler-based design.


import asyncio
from bleak import BleakScanner
from bleak.backends.scanner import AdvertisementData
from interfaces.interfaces import IAdvertisementHandler, IMiScaleSniffer


class MiScaleSniffer(IMiScaleSniffer):
    """
    MiScaleSniffer
    --------------
    Minimal BLE advertisement sniffer for Xiaomi Mi Body Composition Scale 2.

    BLE background:
    - BLE devices broadcast "advertisements" every few hundred ms.
    - Each advertisement can contain:
        • device address (MAC)
        • signal strength (RSSI)
        • advertised services (UUIDs)
        • optional "service_data" bytes (raw payload).
    - UUIDs (Universally Unique Identifiers) identify services or characteristics.
        • 0x181B (Body Composition Service) is the standard BLE service for scales.
        • In 128-bit form: 0000181b-0000-1000-8000-00805f9b34fb
        • Xiaomi scales include weight/impedance data in this service_data.

    This class listens for advertisements and delegates processing to a handler.
    It filters by:
    - Device MAC (optional, set in constructor or via ble_defines)
    """

    def __init__(self, handler: IAdvertisementHandler, scale_addr: str | None = None):
        """
        :param handler: something that knows how to handle an advertisement (prints, saves, decodes…)
        :param scale_addr: optional MAC filter (e.g. "88:22:B2:F2:74:12"). If None, accepts any device.
        """
        self.handler = handler
        self.scale_addr = scale_addr.upper() if scale_addr else None
        # Will hold the BleakScanner instance after start
        self._scanner: BleakScanner | None = None

    def _on_adv(self, device, adv: AdvertisementData):
        """
        Callback invoked by BleakScanner whenever an advertisement is received.

        :param device: BLE device object (includes MAC, name, etc.)
        :param adv: AdvertisementData (includes RSSI, service_uuids, service_data)
        """
        # (1) Optional MAC filter at the sniffer level
        if self.scale_addr and device.address.upper() != self.scale_addr:
            return
        # (2) Delegate the actual processing/printing to the handler
        self.handler.handle(device.address, adv)

    async def run(self):
        """
        Main loop:
        - Creates and starts a BleakScanner with _on_adv as callback.
        - Runs until Ctrl+C.
        """
        print("Listening for Mi Scale advertisements… (Ctrl+C to stop)")
        if self.scale_addr:
            print(f"  filter: {self.scale_addr}")

        self._scanner = BleakScanner(detection_callback=self._on_adv)
        await self._scanner.start()

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            await self._scanner.stop()
            print("Stopped.")

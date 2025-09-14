# print_handler.py
# Defines handler for BLE Readout.
# Author: Leandro
# Date: 2025-09-14

# File History:
# 2025-09-14: Initial creation by Leandro.

from datetime import datetime
from bleak.backends.scanner import AdvertisementData
from interfaces.interfaces import IAdvertisementHandler
import ble_defines as DEF

# ---------------------------
# Print handler implementation
# ---------------------------


class PrintHandler(IAdvertisementHandler):
    """
    PrintHandler
    ------------
    Responsible only for *printing* relevant advertisement data.

    It filters by the Body Composition Service UUID (0x181B) and prints:
    - PC timestamp
    - device address
    - RSSI
    - payload length
    - payload hex
    """

    def handle(self, addr: str, adv: AdvertisementData) -> None:
        # Filter for Body Composition Service service_data
        sd = adv.service_data.get(
            DEF.BCS_UUID
        )  # DEF.BCS_UUID should be "0000181b-0000-1000-8000-00805f9b34fb"
        if not sd:
            return

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts}] addr={addr} rssi={adv.rssi} len={len(sd)} payload_hex={sd.hex()}")

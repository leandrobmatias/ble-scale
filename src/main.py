# src/main.py
# main.py
# Defines module application main.
# Author: Leandro
# Date: 2025-09-14

# File History:
# 2025-09-14: Initial creation by Leandro.

import asyncio
from ble_conection import MiScaleSniffer
from print_handler import PrintHandler
import ble_defines as DEF


async def app_main():

    sniffer = MiScaleSniffer(
        handler=PrintHandler(), scale_addr=DEF.DEVICE_MAC
    )  # None = listen to all devices
    # Run the sniffer (blocking call)
    await sniffer.run()


def main():
    asyncio.run(app_main())

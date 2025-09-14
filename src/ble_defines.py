# ble_defines.py
# Defines BLE device configuration using environment variables.
# Author: Leandro
# Date: 2025-09-12

# File History:
# 2025-09-12: Initial creation by Leandro.

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

DEVICE_NAME = os.getenv("BLE_DEVICE_NAME")
DEVICE_MAC = os.getenv("BLE_DEVICE_MAC")
# -------------------------------------------------------------------
# BLE UUIDs — Assigned Numbers (Bluetooth SIG)
# 0x181B = Body Composition Service (BCS)
# In 128-bit form (what most libs use):
#   0000181b-0000-1000-8000-00805f9b34fb
# -------------------------------------------------------------------
BCS_UUID = os.getenv("BCS_UUID")  # Default to BCS UUID if not set

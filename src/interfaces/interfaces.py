# interfaces.py
# Defines interfaces for classes to use.
# Author: Leandro
# Date: 2025-09-12

# File History:
# 2025-09-12: Initial creation by Leandro.

# interfaces/interfaces.py
from abc import ABC, abstractmethod
from bleak.backends.scanner import AdvertisementData


class IMiScaleSniffer(ABC):
    """Contract for any Mi Scale BLE sniffer implementation."""

    @abstractmethod
    async def run(self) -> None:
        """Run the sniffer until stopped."""
        pass


class IAdvertisementHandler(ABC):
    @abstractmethod
    def handle(self, addr: str, adv: AdvertisementData) -> None: ...

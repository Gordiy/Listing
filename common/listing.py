"""Abstract class of listing."""
from abc import ABC, abstractmethod


class AbstractListing(ABC):
    """Abstract class of listing."""
    @abstractmethod
    def buy(self, symbol: str, count_of_usdt: int) -> None:
        """Buy."""
        pass

    @abstractmethod
    def sell(self, symbol: str, count_of_usdt: int) -> None:
        """Sell"""
        pass

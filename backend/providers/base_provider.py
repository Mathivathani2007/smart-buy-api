from abc import ABC, abstractmethod
from typing import List
from models.product import MarketplaceProduct


class MarketplaceProvider(ABC):
    platform: str

    @abstractmethod
    def search(self, keywords: List[str]) -> List[MarketplaceProduct]:
        raise NotImplementedError

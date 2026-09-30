from typing import List
from providers.base_provider import MarketplaceProvider
from services.product_matching import search_catalog


class AmazonProvider(MarketplaceProvider):
    platform = "Amazon"

    def search(self, keywords: List[str]):
        return search_catalog(self.platform, keywords)

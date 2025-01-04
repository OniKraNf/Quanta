import statistics
from models.item import Item

class PriceService:
    def __init__(self, poe_api_repository):
        self.poe_api_repository = poe_api_repository
        self.query = ''

    def get_average_price(self, query):
        search_result = self.poe_api_repository.search_item(query)
        item_ids = search_result.get("result", [])[:10]
        if not item_ids:
            return None

        price_data = self.poe_api_repository.fetch_prices(item_ids)
        items = price_data.get('result', [])

        prices = [
            item.get('listing', {}).get('price', {}).get('amount')
            for item in items if item.get("listing", {}).get("price")
        ]

        return statistics.mean(prices) if prices else None

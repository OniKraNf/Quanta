import requests

class PoeApiRepository:
    BASE_URL = "https://www.pathofexile.com/api/trade2"

    def __init__(self, league='Standard'):
        self.league = league

    def search_item(self, query: dict):
        url = f'{self.BASE_URL}/search/{self.league}'
        response = requests.post(url, json=query)
        response.raise_for_status()
        return response.json()

    def fetch_prices(self, ids):
        url = f'{self.BASE_URL}/fetch/{','.join(ids)}'
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

import requests, json
from models.item import Item

class PoeApiRepository:
    BASE_URL = "https://www.pathofexile.com/api/trade2"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://www.pathofexile.com",
        "Referer": "https://www.pathofexile.com/"
    }

    def __init__(self, league='Standard'):
        self.league = league
        self.query = None

    def search_item(self, query: dict):
        url = f'{self.BASE_URL}/search/{self.league}'

        response = requests.post(url, json=self.query, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {response.status_code} - {response.text}")
            raise e
        
        fetch_response = self.fetch_prices(response.json())

        return fetch_response

    def fetch_prices(self, response_data):
        ids = response_data['result']
        query_id = response_data['id']
        url = f'{self.BASE_URL}/fetch/{','.join(ids[:10])}?query={query_id}'
        print(url)
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
        
    def create_query(self, item_data: Item):
        
        self.query = {
            "query": {
                "status": {
                    "option": "online"
                },
                "type": "Ruby Ring",
                "stats": [{
                    "type": "and",
                    "filters": [
                        {
                            "id": "explicit.stat_4220027924", 
                            "value": {
                                "min": 20,  
                                "max": 40   
                            }
                        }
                    ]
                }]
            },
            "sort": {
                "price": "asc"
            }
        }

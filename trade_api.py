import requests
import pandas as pd

def search_poe_trade(item_data):
    url = 'https://www.pathofexile.com/api/trade2/search/Standard'

    {
        "query": {
            "status": {
                "option": "online"
            },
            "type": item_data['type'],
            "stats": [{
                "type": "and",
                "filters": [
                    {

                    }
                ]
            }]
        }
    }
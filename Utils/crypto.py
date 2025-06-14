import requests
from fake_headers import Headers
from decimal import Decimal


def get_crypto_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None




def getTopPairs(limit=20):
    header = Headers(
        browser="chrome",  
        os="win",  
        headers=True  
    )
    url = "https://api.binance.com/api/v3/ticker/24hr"

    response = requests.get(
        url=url,
        headers=header.generate()
    )
    data = response.json()

    filtered_data = [x for x in data if float(x['quoteVolume']) > 0]
    sorted_data = sorted(filtered_data, key=lambda x: float(x['quoteVolume']), reverse=True)

    return sorted_data[:limit]

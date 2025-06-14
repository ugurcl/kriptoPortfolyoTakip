import requests
from bs4 import BeautifulSoup as bs
from fake_headers import Headers
from Core import utils





def gold_prices():
    header = Headers(
        browser="chrome",  
        os="win",  
        headers=True  
    )
    r = requests.get('https://bigpara.hurriyet.com.tr/altin/', headers=header.generate(),timeout=10)
    parse = bs(r.content, "lxml").find_all("div", class_="tableBox")[0].find('div', class_="tBody").find_all('ul')

    gold_prices = []

    for ul in parse:
        title = ul.find('h3').get_text(strip=True)
        values = [li.get_text(strip=True) for li in ul.find_all('li')[1:]]
        gold_prices.append({
                'title': title,
                'values': values
            })
    return gold_prices



def get_gold_price(gold_name):
    from decimal import Decimal
    gold = gold_prices()
    for i in gold:
        if i['title'] == str(gold_name):
            
            return utils.convert_price(i['values'][0])
    


def getOneExchangeRates(symbol):
    header = Headers(
        browser="chrome",  
        os="win",  
        headers=True  
    )
    url = f"https://api.frankfurter.app/latest?from={symbol}&to=TRY"
    response = requests.get(
        url=url,
        headers=header.generate(),
        timeout=10

    )

    if response.status_code == 200:
        try:
            content = response.json()['rates']['TRY'] 
            return content
        except Exception:
            getOneExchangeRates(symbol)
    


def get_all_exchange_rates():
    currencies = {
        "USD": "Amerikan Doları",
        "EUR": "Euro",
        "GBP": "İngiliz Sterlini",
        "JPY": "Japon Yeni",
        "AUD": "Avustralya Doları",
        "CAD": "Kanada Doları",
        "CHF": "İsviçre Frangı",
        "INR": "Hindistan Rupisi",
        "CNY": "Çin Yuanı",
        "NZD": "Yeni Zelanda Doları",
        "SEK": "İsveç Kronu"
    }

    exchange_rates = {}

    for code, name in currencies.items():
        url = f"https://api.frankfurter.app/latest?from={code}&to=TRY"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rate = list(data['rates'].values())[0]
            exchange_rates[code] = {
                "name": name,
                "rate": round(rate, 2)
            }
        else:
            exchange_rates[code] = {
                "name": name,
                "rate": "Veri alınamadı"
            }

    return exchange_rates


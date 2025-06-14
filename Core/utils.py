
def convert_price(price_str):
  
    price_str = price_str.replace('.', '')  
    price_str = price_str.replace(',', '.')  
    return float(price_str)  
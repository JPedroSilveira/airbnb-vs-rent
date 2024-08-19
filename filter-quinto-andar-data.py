import json, csv, re
from datetime import date

today = date.today()
file_name = 'quinto-andar-data-' + str(today) + '.json'

def extract_rates(avaliation):
    pattern = r"(\d+,\d+)\s+\((\d+)\)"
    result = re.search(pattern, avaliation)
    if result:
        rate = result.group(1).replace(',', '.')
        qtd_rate = result.group(2)
    else:
        rate = None
        qtd_rate = None

    return rate, qtd_rate

with open(file_name, 'r') as file:
    json_data = json.load(file)

search_results = json_data
with open('filtered-quinto-andar-data.csv', 'a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    #writer.writerow(['id', 'search_date', 'type', 'area','bedrooms', 'bathrooms', 'parking_spaces', 'is_furnished', 'rent', 'iptu_plus_condominium', 'total_cost', 'sales_price', 'address', 'neighbourhood', 'region', 'city', 'for_rent', 'for_sale'])

    for result in search_results:
        id = result['_id']
        search_date = str(today)
        type = result['_source']['type']
        area = result['_source']['area']
        bedrooms = result['_source']['bedrooms']
        bathrooms = result['_source']['bathrooms']
        parking_spaces = result['_source']['parkingSpaces']
        is_furnished = result['_source']['isFurnished']
        rent = result['_source']['rent']
        iptu_plus_condominium = result['_source']['iptuPlusCondominium']
        total_cost = result['_source']['totalCost']
        sales_price = result['_source']['salePrice'] if 'salePrice' in result else ""
        address = result['_source']['address']
        neighbourhood = result['_source']['neighbourhood']
        region = result['_source']['regionName']
        city = result['_source']['city']
        for_rent = result['_source']['forRent']
        for_sale = result['_source']['forSale'] if 'forSale' in result else False
        
        writer.writerow([id, search_date, type, area, bedrooms, bathrooms, bathrooms, parking_spaces, is_furnished, rent, iptu_plus_condominium, total_cost, sales_price, address, neighbourhood, region, city, for_rent, for_sale])

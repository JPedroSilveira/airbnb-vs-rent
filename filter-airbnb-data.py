import json, csv, re

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

with open('airbnb-data.json', 'r') as file:
    json_data = json.load(file)

search_results = json_data['data']['presentation']['staysSearch']['results']['searchResults']
with open('filtered-airbnb-data.csv', 'w', newline='', encoding='utf-8') as arquivo_csv:
    writer = csv.writer(arquivo_csv)
    writer.writerow(['id', 'name', 'room_type_category', 'rate', 'qtd_rate', 'latitude', 'longitude', 'daily_price', 'total_price'])

    for result in search_results:
        id = result['listing']['id']
        name = result['listing']['name']
        room_type_category = result['listing']['roomTypeCategory'] # Não sei o quão útil será essa coluna, talvez remove-la posteriormente
        rate, qtd_rate = extract_rates(result['listing']['avgRatingLocalized'])
        latitude = result['listing']['coordinate']['latitude']
        longitude = result['listing']['coordinate']['longitude']

        daily_price = result['pricingQuote']['structuredStayDisplayPrice']['primaryLine']['accessibilityLabel']
        total_price = result['pricingQuote']['structuredStayDisplayPrice']['secondaryLine']['accessibilityLabel']

        writer.writerow([id, name, room_type_category, rate, qtd_rate, latitude, longitude, daily_price, total_price])

import json
import csv
import re
import argparse
import os



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='Path to input file')
    parser.add_argument('-o', dest='output_path', type=str, help='Output directory', default='.')

    args = parser.parse_args()
    args.input_path = os.path.abspath(args.input_path)
    args.output_path = os.path.abspath(args.output_path)
    assert os.path.isfile(args.input_path)
    assert os.path.isdir(args.output_path)

    return args

def extract_rates(evaluation):
    pattern = r"(\d+,\d+)\s+\((\d+)\)"
    if evaluation:
        result = re.search(pattern, evaluation)
        if result:
            rate = result.group(1).replace(',', '.')
            qtd_rate = result.group(2)
            return rate, qtd_rate
    
    return None, None

def filter_airbnb_data(input_path, output_path):

    with open(input_path, 'r') as file:
        json_data = json.load(file)

    search_results = json_data['data']['presentation']['staysSearch']['results']['searchResults']

    with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
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

if __name__ == '__main__':
    args = parse_args()

    input_path = args.input_path
    output_path = args.output_path
    output_path = os.path.join('filtered_airbnb_data_latest.csv')

    assert not os.path.exists(output_path)

    filter_airbnb_data(input_path=input_path, output_path=output_path)
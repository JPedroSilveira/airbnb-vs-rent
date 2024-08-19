import json
import re
import argparse
import os
import pandas as pd

# Keys are the columns to be filtered, values are new names for the columns

FILTERED_COLUMNS = {
    'listing.id' : 'id', 
    'listing.name' : 'name', 
    'listing.roomTypeCategory' : 'room_type_category', 
    'listing.avgRatingLocalized' : 'rate',
    'listing.coordinate.latitude' : 'latitude',
    'listing.coordinate.longitude' : 'longitude',
    'pricingQuote.structuredStayDisplayPrice.primaryLine.accessibilityLabel' : 'daily_price',
    'pricingQuote.structuredStayDisplayPrice.secondaryLine.accessibilityLabel' : 'total_price',
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='Path to input file')
    parser.add_argument('-o', dest='output_path', type=str, help='Output directory', default='.')
    parser.add_argument('-r', dest='raw', action='store_true', help='Get raw output')

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

def filter_airbnb_data(input_path, output_path, raw):

    with open(input_path, 'r') as file:
        json_data = json.load(file)

    search_results = json_data['data']['presentation']['staysSearch']['results']['searchResults']

    df = pd.json_normalize(search_results)

    if raw:
        raw_output_path = os.path.join(output_path, 'airbnb_search_results_raw_latest.csv')
        df.to_csv(raw_output_path)

    # Add missing columns
    for i in FILTERED_COLUMNS.keys():
        if i not in df.columns:
            df[i] = 0

    df = df[FILTERED_COLUMNS.keys()]
    df.rename(columns=FILTERED_COLUMNS, inplace=True)
    
    output_path = os.path.join(output_path, 'airbnb_search_results_latest.csv')
    df.to_csv(output_path)

if __name__ == '__main__':
    args = parse_args()

    input_path = args.input_path
    output_path = args.output_path
    raw = args.raw

    filter_airbnb_data(input_path=input_path, output_path=output_path, raw=raw)
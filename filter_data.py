import json
import re
import argparse
import os
import pandas as pd
from datetime import date

DATA_ORIGINS = ['airbnb', 'quintoandar']

# Keys are the columns to be filtered, values are new names for the columns

FILTERED_COLUMNS_AIRBNB = {
    'listing.id' : 'id', 
    'listing.name' : 'name', 
    'listing.roomTypeCategory' : 'room_type_category', 
    'listing.avgRatingLocalized' : 'rate',
    'listing.coordinate.latitude' : 'latitude',
    'listing.coordinate.longitude' : 'longitude',
    'pricingQuote.structuredStayDisplayPrice.primaryLine.accessibilityLabel' : 'daily_price',
    'pricingQuote.structuredStayDisplayPrice.secondaryLine.accessibilityLabel' : 'total_price',
}

FILTERED_COLUMNS_QUINTO_ANDAR = {
    '_id' : 'id',
    '_source.type' : 'type',
    '_source.area' : 'area',
    '_source.bedrooms' : 'bedrooms',
    '_source.bathrooms' : 'bathrooms',
    '_source.parkingSpaces' : 'parking_spaces',
    '_source.isFurnished' : 'is_furnished',
    '_source.rent' : 'rent',
    '_source.iptuPlusCondominum' : 'iptu_plus_condominum',
    '_source.totalCost' : 'total_cost',
    '_source.salePrice' : 'sale_price',
    '_source.address' : 'address',
    '_source.neighbourhood' : 'neighbourhood',
    '_source.regionName' : 'regionName',
    '_source.city' : 'city',
    '_source.forRent' : 'for_rent',
    '_source.forSale' : 'for_sale',
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', type=str, help='Path to input file')
    parser.add_argument('data_origin', type=str, choices=DATA_ORIGINS, help='Site from which the data originates')
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

def filter_data(input_path, output_path, origin, raw):

    with open(input_path, 'r') as file:
        json_data = json.load(file)

    if origin == 'airbnb':
        filtered_colums = FILTERED_COLUMNS_AIRBNB
    else:
        filtered_colums = FILTERED_COLUMNS_QUINTO_ANDAR


    df = pd.json_normalize(json_data)

    if raw:
        raw_output_path = os.path.join(output_path, f'{origin}_search_results_raw_latest.csv')
        df.to_csv(raw_output_path)


    # Add missing columns
    for i in filtered_colums.keys():
        if i not in df.columns:
            df[i] = 0

    df = df[filtered_colums.keys()]
    df.rename(columns=filtered_colums, inplace=True)
    
    today = date.today()
    df.insert(0, 'date', today)

    output_path = os.path.join(output_path, f'{origin}_search_results_latest.csv')
    df.to_csv(output_path)

if __name__ == '__main__':
    args = parse_args()

    input_path = args.input_path
    output_path = args.output_path
    origin = args.data_origin
    raw = args.raw

    filter_data(input_path=input_path, output_path=output_path, origin=origin, raw=raw)
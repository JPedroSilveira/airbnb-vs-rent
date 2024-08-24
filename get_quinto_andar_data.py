import time
import uuid
import requests
import json
import argparse
import os
from datetime import datetime
from geopy.geocoders import Photon

CITY_DICT =  {
	'rj' : 'rio-de-janeiro-rj-brasil',
	'sp' : 'sao-paulo-sp-brasil'
	}

STATE_DICT = {
    'Rio de Janeiro': 'RJ',
    'São Paulo': 'SP'
}

DATE_FORMAT = '%Y-%m-%d'

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('city', type=str, choices=CITY_DICT.keys(), help='City to scrape')
	parser.add_argument('-o', '--output_dir', type=str, default='.', help='Output directory')
	
	parser.add_argument('-f', dest='force', action='store_true', help='Force scraping even if output file already exists')
	
	args = parser.parse_args()

	assert args.city in CITY_DICT
	
	args.city_acronym = args.city
	args.city = CITY_DICT[args.city]

	path = os.path.abspath(args.output_dir)
	assert os.path.exists(path)
	args.output_dir = path

	return args

def get_coordinates_from_address(locations):
    user_agent = "airbnbvsrent_quintoandar_" + str(uuid.uuid4())
    geolocator = Photon(user_agent=user_agent)

    for location in locations:
        source = location['_source']
        city = source['city']
        address = source['address']
        neighbourhood = source['neighbourhood']
        address = address + " - " + neighbourhood + ", " + city + ' - ' + STATE_DICT[city]
        localization = geolocator.geocode(address)
        if localization is not None:
            source['latitude'] = localization.latitude
            source['longitude'] = localization.longitude
        time.sleep(1)
      

def scrape_quinto_andar(city, output_path, page_size=50):
    url = "https://apigw.prod.quintoandar.com.br/cached/house-listing-search/v1/search/list"

    locations = []
    lastPage = False
    currentOffset = 0
    currentPage = 0

    # Loop for each page on the request
    while not lastPage:
        print("Requesting page: ", str(currentPage + 1))

        # Create request body to fetch locations
        requestBody = {
            "context": {
                "mapShowing": True,
                "listShowing": True,
                "numPhotos": 0,
                "isSSR": False
            },
            "filters": {
                "businessContext": "RENT",
                "blocklist": [],
                "selectedHouses": [],
                "priceRange": [],
                "specialConditions": [],
                "excludedSpecialConditions": [],
                "houseSpecs": {
                    "area": {
                        "range": {}
                    },
                    "houseTypes": [],
                    "amenities": [],
                    "installations": [],
                    "bathrooms": {
                        "range": {}
                    },
                    "bedrooms": {
                        "range": {}
                    },
                    "parkingSpace": {
                        "range": {}
                    }
                },
                "availability": "ANY",
                "occupancy": "ANY",
                "partnerIds": [],
                "categories": []
            },
            "sorting": {
                "criteria": "RELEVANCE",
                "order": "DESC"
            },
            "pagination": {
                "pageSize": page_size,
                "offset": currentOffset
            },
            "slug": city,
            "fields": [
                "id",
                "coverImage",
                "rent",
                "totalCost",
                "salePrice",
                "iptuPlusCondominium",
                "area",
                "imageList",
                "imageCaptionList",
                "address",
                "regionName",
                "city",
                "visitStatus",
                "activeSpecialConditions",
                "type",
                "forRent",
                "forSale",
                "isPrimaryMarket",
                "bedrooms",
                "parkingSpaces",
                "listingTags",
                "yield",
                "yieldStrategy",
                "neighbourhood",
                "categories",
                "bathrooms",
                "isFurnished",
                "installations"
            ]
        }

        # Create request header
        headers = {
            "origin": "https://www.quintoandar.com.br",
            "referer": "https://www.quintoandar.com.br/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "content-type": "application/json"
        }

        # Send request to fetch locations
        response = requests.post(url, json=requestBody, headers=headers)

        # Extract found locations
        responseBody = response.json()
        requestLocations = responseBody["hits"]["hits"]

        # Add to external list
        locations.extend(requestLocations)

        # Verify if it is last page
        if len(requestLocations) < page_size:
            lastPage = True
        else:
            lastPage = True
            currentPage += 1
            currentOffset = currentPage * page_size
            time.sleep(5)

    print("Number of found locations: ", str(len(locations)))

    get_coordinates_from_address(locations)

    with open(output_path, "w+") as file:
        json.dump(locations, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
	args = parse_args()

	city_acronym = args.city_acronym
	city = args.city

	out_postfix = '_' + city_acronym.upper() + '_' + datetime.now().strftime(DATE_FORMAT)

	output_file = 'quintoandar_data' + out_postfix + '.json'
	output_file = os.path.join(args.output_dir, output_file)

	if not args.force and os.path.exists(output_file):
		print(f'Scraping output file {output_file} already exists, aborting!')
		exit()

	scrape_quinto_andar(
		city=city,
		output_path=output_file)
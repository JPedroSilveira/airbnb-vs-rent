import time
import requests
import json
import argparse
import os
from datetime import datetime

CITY_DICT =  {
	'rj' : 'rio-de-janeiro-rj-brasil',
    'sp' : 'sao-paulo-sp-brasil'
	}

DATE_FORMAT = '%Y-%m-%d'

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('city', type=str, choices=CITY_DICT.keys(), help='City to scrape')
	parser.add_argument('-o', '--output_dir', type=str, default='.', help='Output directory')

	args = parser.parse_args()

	assert args.city in CITY_DICT
	
	args.city_acronym = args.city
	args.city = CITY_DICT[args.city]

	path = os.path.abspath(args.output_dir)
	assert os.path.exists(path)
	args.output_dir = path

	return args


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
            currentPage += 1
            currentOffset = currentPage * page_size
            time.sleep(5)

    print("Number of found locations: ", str(len(locations)))

    with open(output_path, "w+") as file:
        json.dump(locations, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
	args = parse_args()

	city_acronym = args.city_acronym
	city = args.city

	out_postfix = '_' + city_acronym.upper() + '_' + datetime.now().strftime(DATE_FORMAT)

	output_file = 'quinto_andar_data' + out_postfix + '.json'
	output_file = os.path.join(args.output_dir, output_file)

	scrape_quinto_andar(
		city=city,
		output_path=output_file)
import time, requests, json
from datetime import date

CITY = "rio-de-janeiro-rj-brasil" # "sao-paulo-sp-brasil"
PAGE_SIZE = 200

today = date.today()

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
            "pageSize": PAGE_SIZE,
            "offset": currentOffset
        },
        "slug": "rio-de-janeiro-rj-brasil",
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
    if len(requestLocations) < PAGE_SIZE:
        lastPage = True
    else:
        currentPage += 1
        currentOffset = currentPage * PAGE_SIZE
        time.sleep(5)

print("Number of found locations: ", str(len(locations)))

with open("quinto-andar-data-"+str(today)+".json", "w+") as file:
    json.dump(locations, file, indent=4, ensure_ascii=False)
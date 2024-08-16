import requests, json

CITY = 'Rio-de-Janeiro-~-RJ'
# "Sao Paulo - São Paulo"
START_DATE = "2024-09-01"
END_DATE = "2024-09-07"
NUMBER_OF_NIGHTS = "6"
MONTHLY_LENGTH = "3"
MONTHLY_START_DATE = "2024-09-01"
MONTHLY_END_DATE = "2024-12-01"
ITEMS_PER_REQUEST = 50

scriptPrefix = "https://a0.muscache.com/airbnb/static/packages/web/common/frontend/stays-search/routes/StaysSearchRoute/StaysSearchRoute"
scriptExtension= ".js"

apiKeyPrefix = '"api_config":{"key":"'
apiKeySuffix = '"'

operationIdPrefix = "operationId:'"
operationIdSuffix = "'"

# Fetch main page
response = requests.get("https://www.airbnb.com.br/s/" + CITY + "/homes?refinement_paths%5B%5D=%2Fhomes&checkin="+START_DATE+"&checkout="+END_DATE+"&adults=1&tab_id=home_tab&query="+CITY+"&flexible_trip_lengths%5B%5D=one_week&monthly_start_date="+MONTHLY_START_DATE+"&monthly_length="+MONTHLY_LENGTH+"&monthly_end_date="+MONTHLY_END_DATE+"&search_mode=regular_search&price_filter_input_type=0&price_filter_num_nights="+NUMBER_OF_NIGHTS+"&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&zoom_level=15&place_id=ChIJW6AIkVXemwARTtIvZ2xC3FA&location_bb=wbX34MIsYzvBuKhowi8uJA%3D%3D");
responseBody = response.text

# Extract the script URL that can be used to get the operation id
scriptStartIndex = responseBody.find(scriptPrefix)
scriptUrl = responseBody[scriptStartIndex:]
scriptEndIndex = scriptUrl.find(scriptExtension)
scriptUrl = scriptUrl[:scriptEndIndex] + scriptExtension

# Extract the API key
apiKeyStartIndex = responseBody.find(apiKeyPrefix) + len(apiKeyPrefix)
apiKey = responseBody[apiKeyStartIndex:]
apiKeyEndIndex = apiKey.find(apiKeySuffix)
apiKey = apiKey[:apiKeyEndIndex]

# Fetch script
response = requests.get(scriptUrl)
responseBody = response.text

# Extract operation id from script
operationIdStartIndex = responseBody.find(operationIdPrefix) + len(operationIdPrefix)
operationId = responseBody[operationIdStartIndex:]
operationIdEndIndex = operationId.find(operationIdSuffix)
operationId = operationId[:operationIdEndIndex]

# Create request body to fetch locations
requestBody = {
	"operationName": "StaysSearch",
	"variables": {
		"staysSearchRequest": {
			"requestedPageType": "STAYS_SEARCH",
			"metadataOnly": False,
			"source": "structured_search_input_header",
			"searchType": "autocomplete_click",
			"treatmentFlags": [
				"feed_map_decouple_m11_treatment",
				"stays_search_rehydration_treatment_desktop",
				"stays_search_rehydration_treatment_moweb",
				"filter_redesign_2024_treatment",
				"recommended_amenities_2024_treatment_b",
				"m1_2024_monthly_stays_dial_treatment_flag",
				"filter_reordering_2024_roomtype_treatment"
			],
			"rawParams": [
				{
					"filterName": "adults",
					"filterValues": [
						"1"
					]
				},
				{
					"filterName": "cdnCacheSafe",
					"filterValues": [
						"false"
					]
				},
				{
					"filterName": "channel",
					"filterValues": [
						"EXPLORE"
					]
				},
				{
					"filterName": "checkin",
					"filterValues": [
						START_DATE
					]
				},
				{
					"filterName": "checkout",
					"filterValues": [
						END_DATE
					]
				},
				{
					"filterName": "datePickerType",
					"filterValues": [
						"calendar"
					]
				},
				{
					"filterName": "flexibleTripLengths",
					"filterValues": [
						"one_week"
					]
				},
				{
					"filterName": "itemsPerGrid",
					"filterValues": [
						ITEMS_PER_REQUEST
					]
				},
				{
					"filterName": "monthlyEndDate",
					"filterValues": [
						MONTHLY_END_DATE
					]
				},
				{
					"filterName": "monthlyLength",
					"filterValues": [
						MONTHLY_LENGTH
					]
				},
				{
					"filterName": "monthlyStartDate",
					"filterValues": [
						MONTHLY_START_DATE
					]
				},
				{
					"filterName": "placeId",
					"filterValues": [
						"ChIJ0WGkg4FEzpQRrlsz_whLqZs"
					]
				},
				{
					"filterName": "priceFilterInputType",
					"filterValues": [
						"0"
					]
				},
				{
					"filterName": "priceFilterNumNights",
					"filterValues": [
						NUMBER_OF_NIGHTS
					]
				},
				{
					"filterName": "query",
					"filterValues": [
						CITY
					]
				},
				{
					"filterName": "refinementPaths",
					"filterValues": [
						"/homes"
					]
				},
				{
					"filterName": "screenSize",
					"filterValues": [
						"large"
					]
				},
				{
					"filterName": "tabId",
					"filterValues": [
						"home_tab"
					]
				},
				{
					"filterName": "version",
					"filterValues": [
						"1.8.3"
					]
				},
				{
					"filterName": "zoomLevel",
					"filterValues": [
						"15"
					]
				}
			],
			"maxMapItems": 9999
		},
		"staysMapSearchRequestV2": {
			"requestedPageType": "STAYS_SEARCH",
			"metadataOnly": False,
			"source": "structured_search_input_header",
			"searchType": "autocomplete_click",
			"treatmentFlags": [
				"feed_map_decouple_m11_treatment",
				"stays_search_rehydration_treatment_desktop",
				"stays_search_rehydration_treatment_moweb",
				"filter_redesign_2024_treatment",
				"recommended_amenities_2024_treatment_b",
				"m1_2024_monthly_stays_dial_treatment_flag",
				"filter_reordering_2024_roomtype_treatment"
			],
			"rawParams": [
				{
					"filterName": "adults",
					"filterValues": [
						"1"
					]
				},
				{
					"filterName": "cdnCacheSafe",
					"filterValues": [
						"false"
					]
				},
				{
					"filterName": "channel",
					"filterValues": [
						"EXPLORE"
					]
				},
				{
					"filterName": "checkin",
					"filterValues": [
						START_DATE
					]
				},
				{
					"filterName": "checkout",
					"filterValues": [
						END_DATE
					]
				},
				{
					"filterName": "datePickerType",
					"filterValues": [
						"calendar"
					]
				},
				{
					"filterName": "flexibleTripLengths",
					"filterValues": [
						"one_week"
					]
				},
				{
					"filterName": "monthlyEndDate",
					"filterValues": [
						MONTHLY_END_DATE
					]
				},
				{
					"filterName": "monthlyLength",
					"filterValues": [
						MONTHLY_LENGTH
					]
				},
				{
					"filterName": "monthlyStartDate",
					"filterValues": [
						MONTHLY_START_DATE
					]
				},
				{
					"filterName": "placeId",
					"filterValues": [
						"ChIJ0WGkg4FEzpQRrlsz_whLqZs"
					]
				},
				{
					"filterName": "priceFilterInputType",
					"filterValues": [
						"0"
					]
				},
				{
					"filterName": "priceFilterNumNights",
					"filterValues": [
						NUMBER_OF_NIGHTS
					]
				},
				{
					"filterName": "query",
					"filterValues": [
						CITY
					]
				},
				{
					"filterName": "refinementPaths",
					"filterValues": [
						"/homes"
					]
				},
				{
					"filterName": "screenSize",
					"filterValues": [
						"large"
					]
				},
				{
					"filterName": "tabId",
					"filterValues": [
						"home_tab"
					]
				},
				{
					"filterName": "version",
					"filterValues": [
						"1.8.3"
					]
				},
				{
					"filterName": "zoomLevel",
					"filterValues": [
						"15"
					]
				}
			]
		},
		"includeMapResults": True,
		"isLeanTreatment": False
	},
	"extensions": {
		"persistedQuery": {
			"version": 1,
			"sha256Hash": operationId
		}
	}
}

# Create request header
headers = {
    "accept": "*/*",
    "accept-language": "pt-BR,pt;q=0.9",
    "content-type": "application/json",
    "device-memory": "8",
    "dpr": "2",
    "ect": "4g",
    "origin": "https://www.airbnb.com.br",
    "priority": "u=1, i",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-ch-ua-platform-version": '"14.4.1"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "viewport-width": "1032",
    "x-airbnb-api-key": apiKey,
    "x-airbnb-graphql-platform": "web",
    "x-airbnb-graphql-platform-client": "minimalist-niobe",
    "x-airbnb-supports-airlock-v2": "true",
    "x-csrf-token": "",
    "x-csrf-without-token": "1",
    "x-niobe-short-circuited": "true"
}

# Send request to fetch locations
response = requests.post("https://www.airbnb.com.br/api/v3/StaysSearch/" + operationId + "?operationName=StaysSearch&locale=pt&currency=BRL", json=requestBody, headers=headers)
responseBody = response.text
#print(responseBody)

json_data = json.loads(responseBody)

with open("airbnb-data.json", "w+") as arquivo:
    json.dump(json_data, arquivo, indent=4, ensure_ascii=False)

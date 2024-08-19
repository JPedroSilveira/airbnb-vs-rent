import requests
import json
import argparse
import os
from datetime import datetime
import dateutil

CITY_DICT =  {
	'rj' : 'Rio-de-Janeiro-~-RJ',
	}

DATE_FORMAT = '%Y-%m-%d'

def format_date_to_request(date_string):
	if date_string is None:
		return datetime.now().strftime(DATE_FORMAT)
	
	return dateutil.parser.parse(date_string).strftime(DATE_FORMAT)

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('city', type=str, choices=CITY_DICT.keys(), help='City to scrape')
	parser.add_argument('-s', '--start_date', type=str, required=False, help='Starting date')
	parser.add_argument('-e', '--end_date', type=str, required=False, help='End date')
	parser.add_argument('monthly_start_date', type=str, help='Monthly start date')
	parser.add_argument('monthly_end_date', type=str, help='Monthly end date')
	parser.add_argument('-o', '--output_dir', type=str, default='.', help='Output directory')

	args = parser.parse_args()

	assert args.city in CITY_DICT
	
	args.city_acronym = args.city
	args.city = CITY_DICT[args.city]
	args.start_date = format_date_to_request(args.start_date)
	args.end_date = format_date_to_request(args.end_date)
	args.monthly_start_date = format_date_to_request(args.monthly_start_date)
	args.monthly_end_date = format_date_to_request(args.monthly_end_date)

	path = os.path.abspath(args.output_dir)
	assert os.path.exists(path)
	args.output_dir = path

	return args

def scrape_airbnb(city, start_date, end_date, monthly_start_date, monthly_end_date, output_file, number_of_nights=6, monthly_length=3, items_per_request=50):
	number_of_nights = str(number_of_nights) 
	monthly_length= str(monthly_length) 
	items_per_request= str(items_per_request)
	
	scriptPrefix = "https://a0.muscache.com/airbnb/static/packages/web/common/frontend/stays-search/routes/StaysSearchRoute/StaysSearchRoute"
	scriptExtension= ".js"

	apiKeyPrefix = '"api_config":{"key":"'
	apiKeySuffix = '"'

	operationIdPrefix = "operationId:'"
	operationIdSuffix = "'"

	# Fetch main page
	response = requests.get("https://www.airbnb.com.br/s/" + city + "/homes?refinement_paths%5B%5D=%2Fhomes&checkin="+start_date+"&checkout="+end_date+"&adults=1&tab_id=home_tab&query="+city+"&flexible_trip_lengths%5B%5D=one_week&monthly_start_date="+monthly_start_date+"&monthly_length="+monthly_length+"&monthly_end_date="+monthly_end_date+"&search_mode=regular_search&price_filter_input_type=0&price_filter_num_nights="+number_of_nights+"&channel=EXPLORE&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click&zoom_level=15&place_id=ChIJW6AIkVXemwARTtIvZ2xC3FA&location_bb=wbX34MIsYzvBuKhowi8uJA%3D%3D");
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
							start_date
						]
					},
					{
						"filterName": "checkout",
						"filterValues": [
							end_date
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
							items_per_request
						]
					},
					{
						"filterName": "monthlyEndDate",
						"filterValues": [
							monthly_end_date
						]
					},
					{
						"filterName": "monthlyLength",
						"filterValues": [
							monthly_length
						]
					},
					{
						"filterName": "monthlyStartDate",
						"filterValues": [
							monthly_start_date
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
							number_of_nights
						]
					},
					{
						"filterName": "query",
						"filterValues": [
							city
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
							start_date
						]
					},
					{
						"filterName": "checkout",
						"filterValues": [
							end_date
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
							monthly_end_date
						]
					},
					{
						"filterName": "monthlyLength",
						"filterValues": [
							monthly_length
						]
					},
					{
						"filterName": "monthlyStartDate",
						"filterValues": [
							monthly_start_date
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
							number_of_nights
						]
					},
					{
						"filterName": "query",
						"filterValues": [
							city
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

	with open(output_file, "w+") as arquivo:
		json.dump(json_data, arquivo, indent=4, ensure_ascii=False)



if __name__ == '__main__':
	args = parse_args()

	city_acronym = args.city_acronym
	city = args.city
	start_date = args.start_date
	end_date = args.end_date
	monthly_start_date = args.monthly_start_date
	monthly_end_date = args.monthly_end_date

	out_postfix = '_' + city_acronym.upper()
	if start_date == end_date:
		out_postfix += f'_{start_date}'
	else:
		out_postfix += f'_{start_date}_{end_date}'

	output_file = 'airbnb_data' + out_postfix + '.json'
	output_file = os.path.join(args.output_dir, output_file)

	scrape_airbnb(
		city=city,
		start_date=start_date,
		end_date=end_date,
		monthly_start_date=monthly_start_date,
		monthly_end_date=monthly_end_date,
		output_file=output_file)
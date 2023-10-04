import requests
import os
from dotenv import load_dotenv, find_dotenv

# Get secrets
load_dotenv(find_dotenv())

ENDPOINT_TEQUILA ="https://api.tequila.kiwi.com/"
API_KEY_TEQUILA = os.getenv("api_key_tequila")

class AirportCode:
    #This class add IATA  code to city
    def get_code(self, city_name):
        '''Get airport code via Tequila API'''
        location_endpoint = f"{ENDPOINT_TEQUILA}/locations/query"
        headers = {"apikey": API_KEY_TEQUILA}
        query = {
            "term": city_name,
            "location_types": "city",
        }
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        test_code = "TESTING"
        return test_code






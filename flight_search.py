import requests
import os
from dotenv import load_dotenv, find_dotenv
from flight_data import FlightData

# Get secrets
load_dotenv(find_dotenv())

ENDPOINT_TEQUILA ="https://api.tequila.kiwi.com"
API_KEY_TEQUILA = os.getenv("api_key_tequila")

class TequilaAPIdata:
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
        airport_code = results[0]["code"]
        return airport_code
    
    def check_flights(self,  origin_airport_city_code, destination_airport_city_code, from_time, to_time):
        '''Make GET request - ask about cheapest flight from London to destination city.'''
        headers = {"apikey": API_KEY_TEQUILA}
        query = {
            "fly_from":origin_airport_city_code,
            "fly_to": destination_airport_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP",
        }

        response = requests.get(
            url=f"{ENDPOINT_TEQUILA}/v2/search",
            headers=headers,
            params=query,
        )

        #If no flight in this period of time
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_airport_city_code}.")
            return None

        #Create object Flight with attributes
        flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][0]["cityTo"],
                    destination_airport=data["route"][0]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][1]["local_departure"].split("T")[0]
                )
        #Print the cheapest price for flight to destination city
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data







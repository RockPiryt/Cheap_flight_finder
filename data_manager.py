import requests

SHEETY_PRICES_URL = "https://api.sheety.co/aac9513b17237b93b2436aac0a6a2dd6/myFlightDeals/prices"
# SHEETY_PRICES_URL_PUT = f"{SHEETY_PRICES_URL_GET}/row_id"

#Class to communicate with Google Sheet using Sheety API
class DataFromGoogleSheet:

    def __init__(self):
        self.sheet_data = {}
    
    def get_data(self):
        '''Get information from google sheet'''

        response = requests.get(url=SHEETY_PRICES_URL)
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data
    
    def update_IATA_code(self):
        '''Make PUT request - add TESTING to IATA code in Google sheet'''
        for row in self.sheet_data:
            IATA_code = {"price": {"iataCode": row["iataCode"]}} # name price is single version name of google sheet- Sheety API documentation add row

            response = requests.put(url=f"{SHEETY_PRICES_URL}/{row['id']}", json=IATA_code)
            print(response.text)




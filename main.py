#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import pprint

from data_manager import DataFromGoogleSheet
from flight_search import AirportCode

# Get infromation from Google sheet "prices"
datasheet = DataFromGoogleSheet()#instancja classy do zarządzania danymi z arkusza przez Sheety API
sheet_information = datasheet.get_data()#to jest lista
pp=pprint.PrettyPrinter(indent=4)
pp.pprint(f"Pierwotne dane z arkusza (lista):\n{sheet_information}")

# Write airport code IATA to city
if sheet_information[0]["iataCode"] == "":
    airport_code = AirportCode()
    for row in sheet_information:
        row["iataCode"] = airport_code.get_code(city_name=row["city"])
    pp=pprint.PrettyPrinter(indent=4)
    pp.pprint(f"Dane z arkusza z dodanym TESTING w iataCode:\n {sheet_information}")

    # Zaktualizowanie listy z danymi z arkusza na listę która zawiera TESTING w IATA code
    datasheet.sheet_data = sheet_information
    #Wywoałenie funkcji dla classy która jest odpowiedzialna za wykonanie PUT request- która dodaje TESTING do IATA code
    datasheet.update_IATA_code()
from datetime import datetime, timedelta
import pprint

from data_manager import DataFromGoogleSheet
from flight_search import TequilaAPIdata
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "LON"


#----------------- Get information from Google sheet "prices"
datasheet = DataFromGoogleSheet()#Class instance to manage data from Google sheet via Sheety API
sheet_information = datasheet.get_data()#This is list
pp=pprint.PrettyPrinter(indent=4)
pp.pprint(f"Pierwotne dane z arkusza (lista):\n{sheet_information}")

#-----------------------Write airport code IATA to city
if sheet_information[0]["iataCode"] == "":
    airport_code = TequilaAPIdata()
    for row in sheet_information:
        row["iataCode"] = airport_code.get_code(city_name=row["city"])
    pp=pprint.PrettyPrinter(indent=4)
    pp.pprint(f"Dane z arkusza z dodanym TESTING w iataCode:\n {sheet_information}")

    # Zaktualizowanie listy z danymi z arkusza na listę która zawiera TESTING w IATA code
    datasheet.sheet_data = sheet_information
    #Wywoałenie funkcji dla classy która jest odpowiedzialna za wykonanie PUT request- która dodaje TESTING do IATA code
    datasheet.update_IATA_code()

#-----------------------Check flights price from London to destination city

#Time period
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))


tequila_flight_search = TequilaAPIdata()
#Check flight price for destination from google sheet - destination["iataCode"]
for destination in sheet_information:
    flight = tequila_flight_search.check_flights(
        origin_airport_city_code=ORIGIN_CITY_IATA,
        destination_airport_city_code = destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
#-------Send sms if flight price from Tequila API is lower than our price in google sheet
    notification_manager = NotificationManager()

    if flight.price < destination["lowestPrice"]:
            notification_manager.send_sms(
                message=f"Low price alert! Only £{flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}."
            )